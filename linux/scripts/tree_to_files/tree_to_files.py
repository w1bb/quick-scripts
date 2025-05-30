# Kindly contributed by Valentin-Ioan Vintilă
# under the MIT license.
# -------------------------------------------

# This script takes a tree-like file structure such as:
#
# .
# ├── docker-compose.yml
# ├── backend/
# │   ├── Dockerfile
# │   ├── requirements.txt
# │   └── app/
# │       ├── __init__.py
# │       └── main.py
# └── frontend/
#     ├── Dockerfile
#     └── src/
#
# And converts it to files.

from bigtree import Node
import re
from typing import Dict, List, Tuple, Optional

TAB_SIZE = 4

warnings: List[str] = []

def split_filenames(path_str: str) -> Dict[str, List[str] | bool]:
    segments = path_str.split("/")
    ok_filenames = []

    has_empty_segments_in_path = False 
    has_dot_dot_in_path = False        

    original_style_empty_directories = False
    for i in range(len(segments)):
        if segments[i] == "" and i != len(segments) - 1:
            original_style_empty_directories = True
            break 

    for segment_content in segments:
        stripped_segment = segment_content.strip()
        if stripped_segment == "" and len(segments) > 1: 
            has_empty_segments_in_path = True 
        
        if ".." in stripped_segment: 
            has_dot_dot_in_path = True
        
        ok_filenames.append(stripped_segment) 

    if original_style_empty_directories: 
        warnings.append(f"Input path '{path_str}' contains segments that are empty before stripping (e.g. '//').")
    if has_dot_dot_in_path: 
        warnings.append(f"Input path '{path_str}' contains '..'.")

    return {
        "filenames": ok_filenames, 
        "empty_directories": original_style_empty_directories, 
        "too_many_dots": has_dot_dot_in_path 
    }

def parse_branch(branch: str) -> Optional[Dict[str, List[str] | int | bool]]: # Added bool for potential new fields
    spaces = 0
    text_after_prefix = branch 

    spaces_pattern = re.compile(r"^[ \t├│─└]")
    filenames_pattern = re.compile(r"^[\w\-. \/]+") 

    while spaces_pattern.match(text_after_prefix):
        if text_after_prefix[0] == '\t':
            spaces += TAB_SIZE
        else:
            spaces += 1
        text_after_prefix = text_after_prefix[1:]
    
    filenames_match = filenames_pattern.match(text_after_prefix)
    if filenames_match is None:
        if not text_after_prefix.strip():
             return None 
        warnings.append(f"Line content '{text_after_prefix}' (from original: '{branch}') does not start with a valid filename/path pattern.")
        return None

    name_part_on_line = filenames_match.group(0).strip() 

    if not name_part_on_line: 
        warnings.append(f"Line content '{text_after_prefix}' (from original: '{branch}') yielded empty name part after stripping match.")
        return None
        
    if name_part_on_line == "/":
        # The boolean key 'is_last_segment_explicit_dir' is added here for consistency if needed later,
        # though the simple heuristic in main won't use it for now.
        # A root "/" typically implies a directory.
        return {
            "filenames": ["."], 
            "spaces": spaces,
            "is_last_segment_explicit_dir": True 
        }

    string_to_split = name_part_on_line
    is_explicit_dir_hint = name_part_on_line.endswith('/') # Check before stripping final slash

    if name_part_on_line.endswith('/') and len(name_part_on_line) > 1:
        string_to_split = name_part_on_line[:-1]
    
    path_analysis = split_filenames(string_to_split)
    final_filenames = path_analysis["filenames"]

    if not final_filenames and string_to_split: 
        warnings.append(f"Path '{string_to_split}' (from line '{branch}') resulted in an empty list of filename segments unexpectedly.")
        return None 

    return {
        "filenames": final_filenames,
        "spaces": spaces,
        "is_last_segment_explicit_dir": is_explicit_dir_hint # Pass the hint
    }

def parse_tree(tree: str) -> Optional[Node]:
    lines = tree.strip().split("\n")
    if not lines or not lines[0].strip():
        warnings.append("Input tree string is empty or contains only whitespace.")
        return None

    parsed_branches_list: List[Dict[str, List[str] | int | bool]] = []
    for line_str in lines:
        if not line_str.strip():
            continue
        parsed_branch_data = parse_branch(line_str)
        if parsed_branch_data:
            if not parsed_branch_data["filenames"]: 
                 warnings.append(f"Branch parsing for line '{line_str}' resulted in no filenames, skipping.")
                 continue
            parsed_branches_list.append(parsed_branch_data)

    if not parsed_branches_list:
        warnings.append("No valid branches found in the tree string.")
        return None

    virtual_root = Node("virtual_root_for_parsing")
    ancestor_stack: List[Tuple[Node, int]] = []
    
    for p_branch_data in parsed_branches_list:
        branch_filenames = p_branch_data["filenames"] # type: ignore 
        branch_spaces = p_branch_data["spaces"] # type: ignore

        while ancestor_stack and branch_spaces <= ancestor_stack[-1][1]:
            ancestor_stack.pop()

        parent_for_current_path = virtual_root if not ancestor_stack else ancestor_stack[-1][0]
        
        current_segment_parent = parent_for_current_path
        final_node_of_line: Optional[Node] = None

        for i, name_segment in enumerate(branch_filenames):
            if not name_segment:
                warnings.append(f"Skipping empty path segment in '{'/'.join(branch_filenames)}' under parent '{current_segment_parent.name}'.") # type: ignore
                continue 

            existing_child_node: Optional[Node] = None
            for child in current_segment_parent.children:
                if child.name == name_segment:
                    existing_child_node = child
                    break
            
            current_node: Node
            if existing_child_node:
                current_node = existing_child_node
            else:
                current_node = Node(name_segment, parent=current_segment_parent)
            
            current_segment_parent = current_node
            final_node_of_line = current_node 

        if final_node_of_line: 
            # If the problem statement were relaxed to allow Node attribute modification:
            # if p_branch_data.get("is_last_segment_explicit_dir", False):
            #    final_node_of_line.attr["is_explicit_dir_hint"] = True
            ancestor_stack.append((final_node_of_line, branch_spaces))

    if not virtual_root.children:
        warnings.append("Tree parsing did not result in any nodes.")
        return None
        
    if len(virtual_root.children) == 1:
        actual_root = virtual_root.children[0]
        actual_root.parent = None 
        return actual_root
    else:
        virtual_root.name = "root" 
        return virtual_root

# --- Helper functions for main functionality ---
def is_node_a_directory_simple(node: Node) -> bool:
    """
    Determines if a node should be treated as a directory for creation.
    Heuristic:
    - Nodes named "." are considered directories.
    - Nodes with children are considered directories.
    - Leaf nodes (not named ".") are considered files.
    Limitation: This heuristic means that an empty directory represented as a leaf node
    (e.g., from "emptydir/" in the input if it has no children under it)
    will be treated as a file. This is due to the constraint of not modifying
    parsing functions to pass detailed type hints for each node.
    """
    if node.name == ".":
        return True
    return not node.is_leaf

def create_file_structure_recursive(node: Node, current_base_path: str, dry_run: bool):
    """
    Recursively prints or creates files and directories based on the node structure.
    """
    node_name = node.name
    if not node_name:
        print(f"Warning: Attempting to process a node with an empty name under '{current_base_path}'. Skipping.")
        return

    item_path = os.path.join(current_base_path, node_name)

    if is_node_a_directory_simple(node):
        print(f"Directory: {item_path}")
        if not dry_run:
            try:
                os.makedirs(item_path, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory {item_path}: {e}", file=sys.stderr)
                # warnings.append(f"Error creating directory {item_path}: {e}") # Optional
                return 
        
        for child_node in node.children:
            create_file_structure_recursive(child_node, item_path, dry_run)
    else: # It's a file
        print(f"File: {item_path}")
        if not dry_run:
            try:
                parent_dir = os.path.dirname(item_path)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)
                
                with open(item_path, 'a') as f: 
                    pass
            except OSError as e:
                print(f"Error creating file {item_path}: {e}", file=sys.stderr)
                # warnings.append(f"Error creating file {item_path}: {e}") # Optional

if __name__ == '__main__':
    import argparse
    import os
    import sys

    cli_description = (
        "Convert a tree-like text structure to actual files and directories.\n\n"
        "Note on directory/file creation (due to constraint of not altering parsing logic):\n"
        "- Nodes with children are treated as directories.\n"
        "- Nodes named '.' are treated as directories.\n"
        "- Leaf nodes (nodes without children, not named '.') are treated as files.\n"
        "This means an empty directory defined with a trailing slash in the input\n"
        "(e.g., 'emptydir/') will be created as a file if it's a leaf in the parsed tree."
    )

    parser = argparse.ArgumentParser(
        description=cli_description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("tree_file", help="Path to the file containing the tree structure definition.")
    parser.add_argument("starting_path", nargs='?', default=".",
                        help="The base directory where the file structure will be created. Defaults to the current directory ('.').")
    parser.add_argument("-o", "--output-only", "--only-output", action="store_true", # Added alias
                        help="Only display the parsed tree structure and proposed operations/warnings; do not create any files or directories.")

    args = parser.parse_args()
    warnings.clear()

    try:
        with open(args.tree_file, "r", encoding="utf-8") as f:
            tree_string = f.read()
    except FileNotFoundError:
        print(f"Error: Input tree file '{args.tree_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading tree file '{args.tree_file}': {e}", file=sys.stderr)
        sys.exit(1)

    root_node = parse_tree(tree_string)

    if not root_node:
        print("Error: Failed to parse the tree or the tree definition was empty.", file=sys.stderr)
        if warnings:
            print("\nWarnings generated during parsing:", file=sys.stderr)
            for warning_msg in warnings:
                print(f"- {warning_msg}", file=sys.stderr)
        sys.exit(1)

    print("Parsed tree structure overview:")
    root_node.show()

    print("\nProposed operations (files/directories to be created/checked):")
    effective_base_path = os.path.abspath(args.starting_path)
    synthetic_root_names = {".", "root", "virtual_root_for_parsing"}

    if root_node.name in synthetic_root_names:
        if not root_node.children:
            print(f"(No operations for '{root_node.name}' as it has no children to create in '{effective_base_path}')")
        for child_node in root_node.children:
            create_file_structure_recursive(child_node, effective_base_path, dry_run=True)
    else:
        create_file_structure_recursive(root_node, effective_base_path, dry_run=True)
    
    if warnings:
        print("\nWarnings from parsing stage:")
        for warning_msg in warnings:
            print(f"- {warning_msg}")

    if args.output_only:
        print("\n--- Output-only mode ---")
        print("No files or directories will be created.")
        sys.exit(0)

    print(f"\nThe file structure will be created relative to: {effective_base_path}")
    
    user_confirmation = ""
    while user_confirmation not in ["yes", "y", "no", "n"]:
        try:
            user_confirmation = input("Do you want to proceed with creating this file structure? (yes/no): ").strip().lower()
            if user_confirmation not in ["yes", "y", "no", "n"]:
                print("Please answer 'yes' or 'no'.")
        except EOFError:
            print("\nConfirmation aborted (EOF).")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nConfirmation aborted by user (Ctrl+C).")
            sys.exit(1)

    if user_confirmation in ["no", "n"]:
        print("Operation aborted by user.")
        sys.exit(0)

    print("\nProceeding with creation...")
    
    if not os.path.exists(args.starting_path) and args.starting_path != ".":
        try:
            os.makedirs(args.starting_path, exist_ok=True)
            print(f"Created base directory: {effective_base_path}")
        except OSError as e:
            print(f"Error: Could not create base directory '{effective_base_path}': {e}", file=sys.stderr)
            sys.exit(1)
    
    if root_node.name in synthetic_root_names:
        for child_node in root_node.children:
            create_file_structure_recursive(child_node, args.starting_path, dry_run=False)
    else:
        create_file_structure_recursive(root_node, args.starting_path, dry_run=False)

    print("\nFile structure creation process complete.")