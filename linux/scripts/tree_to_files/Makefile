# Kindly contributed by Valentin-Ioan Vintilă
# under the MIT license.
# -------------------------------------------

# Makefile for tree_to_files utility

# Variables
PYTHON ?= python3
PIP = $(PYTHON) -m pip
VENV_DIR = .venv

# Path to Python interpreter and pip within the virtual environment
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip
PYINSTALLER = $(VENV_DIR)/bin/pyinstaller

SCRIPT_NAME = tree_to_files.py
EXECUTABLE_NAME = tree_to_files
DIST_DIR = dist

# Sentinel file to track if dependencies are installed/updated in venv
VENV_SENTINEL = $(VENV_DIR)/.deps_installed

.PHONY: all build install_deps venv clean run run_compiled help

# Default target
all: build

help:
	@echo "Makefile for the tree_to_files utility"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all               Build the standalone executable (default)."
	@echo "  build             Build the standalone executable."
	@echo "  venv              Create virtual environment and install dependencies."
	@echo "  install_deps      Install/update dependencies in the virtual environment."
	@echo "  clean             Remove build artifacts (dist/, build/, *.spec) and optionally the virtual environment."
	@echo "  run               Run the script using the Python interpreter from the virtual environment."
	@echo "  run_compiled      Run the compiled executable (after 'make build')."
	@echo ""
	@echo "Example: make build"

# Virtual environment setup and dependency installation
$(VENV_SENTINEL): requirements.txt
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment in $(VENV_DIR)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "Installing/updating dependencies from requirements.txt into $(VENV_DIR)..."
	@$(VENV_PIP) install -r requirements.txt
	@touch $@

venv: $(VENV_SENTINEL) ## Alias to setup venv and install dependencies

install_deps: $(VENV_SENTINEL) ## Alias to install/update dependencies

# Build the standalone executable
# Depends on the script and having the venv with PyInstaller ready.
build: $(SCRIPT_NAME) $(VENV_SENTINEL)
	@echo "Building standalone executable '$(EXECUTABLE_NAME)' from '$(SCRIPT_NAME)'..."
	@$(PYINSTALLER) --onefile --name $(EXECUTABLE_NAME) --distpath $(DIST_DIR) $(SCRIPT_NAME)
	@echo "Build complete. Executable created at: $(DIST_DIR)/$(EXECUTABLE_NAME)"

# Run targets
run: $(VENV_SENTINEL)
	@echo "Running script with interpreter: $(VENV_PYTHON) $(SCRIPT_NAME) --help"
	@$(VENV_PYTHON) $(SCRIPT_NAME) --help

run_compiled: build
	@echo "Running compiled executable: $(DIST_DIR)/$(EXECUTABLE_NAME) --help"
	@if [ -f "$(DIST_DIR)/$(EXECUTABLE_NAME)" ]; then \
		$(DIST_DIR)/$(EXECUTABLE_NAME) --help; \
	else \
		echo "Error: Compiled executable not found at $(DIST_DIR)/$(EXECUTABLE_NAME). Run 'make build' first."; \
		exit 1; \
	fi

# Clean up build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	@rm -rf build $(DIST_DIR) *.spec
	@if [ -d "$(VENV_DIR)" ]; then \
		printf "Remove virtual environment directory '$(VENV_DIR)'? (y/N) "; \
		read -r choice; \
		case "$$choice" in \
			[yY]|[yY][eE][sS]) \
				echo "Removing virtual environment $(VENV_DIR)..."; \
				rm -rf $(VENV_DIR); \
				;; \
			*) \
				echo "Skipping removal of $(VENV_DIR)."; \
				;; \
		esac; \
	fi
	@echo "Clean complete."