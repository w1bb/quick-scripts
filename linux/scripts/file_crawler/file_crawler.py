# Kindly contributed by Valentin-Ioan Vintilă
# under the MIT license.
# -------------------------------------------

# This script crawls a directory and its subdirectories,
# and prints the files' contents, along with their paths,
# filtered by a set of include and exclude rules.

import os
import sys
import fnmatch
import re

def expand_braces(pattern):
    """
    Expands brace patterns like 'a/*.{py,go}' into ['a/*.py', 'a/*.go'].
    If no braces are found, returns the original pattern in a list.
    """
    match = re.search(r'\{([^}]+)\}', pattern)
    if not match:
        return [pattern]

    prefix = pattern[:match.start()]
    suffix = pattern[match.end():]
    options = match.group(1).split(',')
    
    return [f"{prefix}{opt}{suffix}" for opt in options]

def print_file_content(file_path):
    """
    Prints the content of a single file with a header and separator.
    """
    print(f"Content of {file_path}:")
    try:
        # The 'with' statement ensures the file is automatically closed.
        # errors='ignore' prevents the script from crashing on binary files.
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip():
                print("[File is empty or contains only whitespace]")
            else:
                print(content)

    except IOError as e:
        print(f"--- Could not read file: {e} ---")
    
    print("\n" + "-" * 40 + "\n")

def crawl_and_print(root_dir, include_patterns, exclude_patterns):
    """
    Crawls a directory, filtering files by include/exclude patterns,
    and prints the content of matching files.

    Args:
        root_dir (str): The starting directory path.
        include_patterns (list): A list of glob patterns to include.
        exclude_patterns (list): A list of glob patterns to exclude.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Provided path '{root_dir}' is not a valid directory.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            # For matching, we need a consistent relative path.
            # We also normalize path separators to '/' for cross-platform pattern matching.
            relative_path = os.path.relpath(file_path, root_dir)
            relative_path = relative_path.replace(os.sep, '/')

            # 1. Check for exclusions first (highest priority).
            is_excluded = False
            for pattern in exclude_patterns:
                if fnmatch.fnmatch(relative_path, pattern):
                    is_excluded = True
                    break
            
            if is_excluded:
                continue

            # 2. Check for inclusions.
            # If no include patterns are given, everything not excluded is included.
            is_included = not include_patterns
            if not is_included:
                for pattern in include_patterns:
                    if fnmatch.fnmatch(relative_path, pattern):
                        is_included = True
                        break
            
            if is_included:
                print_file_content(file_path)

def main():
    """
    Main function to handle command-line arguments, parse patterns, and start the crawler.
    """
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <directory> [include/exclude patterns...]")
        print("\nExamples:")
        print(f"  python {sys.argv[0]} .")
        print(f"  python {sys.argv[0]} . '*.py'")
        print(f"  python {sys.argv[0]} . '*.{py,txt}' '!tests/'")
        print(f"  python {sys.argv[0]} my_project 'src/*.js' '!src/vendor/*'")
        sys.exit(1)

    root_dir = sys.argv[1]
    raw_patterns = sys.argv[2:]

    include_patterns = []
    exclude_patterns = []

    for p in raw_patterns:
        # Expand brace syntax like {py,go}
        expanded_patterns = expand_braces(p)
        
        for pattern in expanded_patterns:
            if pattern.startswith('!'):
                # This is an exclusion pattern
                clean_pattern = pattern[1:]
                exclude_patterns.append(clean_pattern)
                # If a user provides a directory like '!a/b', they mean everything inside it.
                # So we also add a pattern to match files within that directory.
                if not any(wildcard in clean_pattern for wildcard in '*?['):
                    exclude_patterns.append(os.path.join(clean_pattern, '*').replace(os.sep, '/'))
            else:
                # This is an inclusion pattern
                include_patterns.append(pattern)

    crawl_and_print(root_dir, include_patterns, exclude_patterns)

if __name__ == "__main__":
    main()