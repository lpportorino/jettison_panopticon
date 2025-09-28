# Panopticon Production Build Makefile
# Optimized for NVIDIA Orin AGX 32 (Cortex-A78AE)

# Project configuration
PROJECT_NAME := panopticon
SRC_DIR := src
BUILD_DIR := build
DIST_DIR := dist
VENV_NAME := .venv

# Python version - automatically use latest stable
PYTHON_VERSION := $(shell pyenv install --list 2>/dev/null | grep -E "^\s*3\.[0-9]+\.[0-9]+$$" | grep -v "dev\|rc\|a\|b" | tail -1 | xargs)

# Check if pyenv is installed
PYENV_EXISTS := $(shell command -v pyenv 2> /dev/null)

# Compiler and optimization flags
CC := clang
CXX := clang++

# ARM64 optimization flags for NVIDIA Jetson Orin AGX (Cortex-A78AE)
# Always optimize for ARM64 - this is a Jetson-specific build
CPU_FLAGS := -march=armv8.2-a+crypto+fp16+rcpc+dotprod
# Use -mcpu=native when building directly on Jetson
ifeq ($(shell uname -m),aarch64)
    CPU_FLAGS := -mcpu=native
endif

# Maximum optimization flags
OPT_FLAGS := -O3 \
             -flto=thin \
             -ffast-math \
             -funroll-loops \
             -ftree-vectorize \
             -fomit-frame-pointer \
             -finline-functions \
             -fprefetch-loop-arrays

# Nuitka flags for production build
NUITKA_FLAGS := --standalone \
                --onefile \
                --lto=yes \
                --clang \
                --static-libpython=no \
                --assume-yes-for-downloads \
                --remove-output \
                --disable-ccache \
                --show-progress \
                --show-memory \
                --include-package=websockets \
                --include-package=redis \
                --include-package=asyncpg \
                --include-package=textual \
                --include-package=rich \
                --include-data-dir="$(SRC_DIR)=src" \
                --output-dir="$(BUILD_DIR)" \
                --output-filename="$(PROJECT_NAME)"

# Additional Nuitka optimization flags
NUITKA_OPT_FLAGS := --python-flag=no_site \
                    --python-flag=no_asserts \
                    --python-flag=no_docstrings \
                    --python-flag=-O

# Environment variables for compilation
export CC
export CXX
export CFLAGS=$(CPU_FLAGS) $(OPT_FLAGS)
export CXXFLAGS=$(CPU_FLAGS) $(OPT_FLAGS)
export LDFLAGS=-flto=thin

# Default target
.PHONY: all
all: help

# Setup pyenv and Python version
.PHONY: setup-pyenv
setup-pyenv:
ifndef PYENV_EXISTS
	@echo "Installing pyenv..."
	curl https://pyenv.run | bash
	@echo "Please add pyenv to your PATH and restart your shell, then run make again"
	@exit 1
else
	@echo "pyenv is installed"
endif
	@# Get latest Python version if not already set
	@if [ -z "$(PYTHON_VERSION)" ]; then \
		echo "Fetching latest Python version..."; \
		LATEST_PYTHON=$$(pyenv install --list | grep -E "^\s*3\.[0-9]+\.[0-9]+$$" | grep -v "dev\|rc\|a\|b" | tail -1 | xargs); \
		echo "Latest stable Python version: $$LATEST_PYTHON"; \
	else \
		LATEST_PYTHON=$(PYTHON_VERSION); \
		echo "Using Python version: $$LATEST_PYTHON"; \
	fi; \
	if ! pyenv versions | grep -q $$LATEST_PYTHON; then \
		echo "Installing Python $$LATEST_PYTHON..."; \
		pyenv install $$LATEST_PYTHON; \
	fi; \
	pyenv local $$LATEST_PYTHON

# Create virtual environment with pyenv Python
.PHONY: venv
venv: setup-pyenv
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
	python -m venv $(VENV_NAME)
	@echo "Virtual environment created"

# Install dependencies
.PHONY: deps
deps: venv
	@echo "Installing dependencies..."
	$(VENV_NAME)/bin/pip install --upgrade pip setuptools wheel
	$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "Dependencies installed"

# Build production binary
.PHONY: build
build: deps
	@echo "Building production binary for NVIDIA Jetson Orin AGX (ARM64)..."
	@echo "Target: Cortex-A78AE"
	@echo "CPU Flags: $(CPU_FLAGS)"
	@echo "Optimization Flags: $(OPT_FLAGS)"
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(DIST_DIR)

	# Run Nuitka compilation for ARM64
	$(VENV_NAME)/bin/python -m nuitka \
		$(NUITKA_FLAGS) \
		$(NUITKA_OPT_FLAGS) \
		$(SRC_DIR)/run.py

	# Move binary to dist
	@mv $(BUILD_DIR)/$(PROJECT_NAME) $(DIST_DIR)/
	@echo "Build complete: $(DIST_DIR)/$(PROJECT_NAME)"
	@echo "Optimized for NVIDIA Jetson Orin AGX 32GB"

# Build for GitHub Actions (ARM64 runners only)
.PHONY: build-ci
build-ci:
	@echo "Building in CI environment for NVIDIA Jetson Orin AGX..."
	@echo "Architecture: ARM64 (aarch64)"
	@echo "Target: Cortex-A78AE"
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(DIST_DIR)

	# Install dependencies
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

	# Run Nuitka compilation for ARM64
	python -m nuitka \
		$(NUITKA_FLAGS) \
		$(NUITKA_OPT_FLAGS) \
		$(SRC_DIR)/run.py

	# Move binary to dist
	@mv $(BUILD_DIR)/$(PROJECT_NAME) $(DIST_DIR)/
	@echo "Build complete: $(DIST_DIR)/$(PROJECT_NAME)"
	@echo "Optimized for NVIDIA Jetson Orin AGX 32GB"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)
	rm -rf $(DIST_DIR)
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf $(SRC_DIR)/**/__pycache__
	rm -rf $(SRC_DIR)/**/**/__pycache__
	rm -rf *.build
	rm -rf *.dist
	rm -rf *.onefile-build
	@echo "Clean complete"

# Clean everything including virtual environment
.PHONY: distclean
distclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV_NAME)
	rm -f .python-version
	@echo "Distclean complete"

# Run development version (not compiled)
.PHONY: run-dev
run-dev: deps
	@echo "Running development version..."
	$(VENV_NAME)/bin/python $(SRC_DIR)/run.py

# Test the build
.PHONY: test
test: build
	@echo "Testing built binary..."
	$(DIST_DIR)/$(PROJECT_NAME) --version
	@echo "Binary test successful"

# Show build information
.PHONY: info
info:
	@echo "=== Build Information ==="
	@echo "Project: $(PROJECT_NAME)"
	@if [ -z "$(PYTHON_VERSION)" ]; then \
		echo "Python Version: Latest stable (will be determined at setup)"; \
	else \
		echo "Python Version: $(PYTHON_VERSION)"; \
	fi
	@echo "Architecture: $(shell uname -m)"
	@echo "Compiler: $(CC)"
	@echo "CPU Flags: $(CPU_FLAGS)"
	@echo "Optimization Flags: $(OPT_FLAGS)"
	@echo "========================="

# Install credentials template
.PHONY: setup-credentials
setup-credentials:
	@if [ ! -f credentials.toml ]; then \
		echo "Creating credentials.toml from template..."; \
		cp credentials.toml.example credentials.toml; \
		echo "Please edit credentials.toml with your actual credentials"; \
	else \
		echo "credentials.toml already exists"; \
	fi

# Initial setup
.PHONY: setup
setup: setup-credentials setup-pyenv venv deps
	@echo "Setup complete. Run 'make build' to create production binary."

# Help target
.PHONY: help
help:
	@echo "Panopticon - NVIDIA Jetson Orin AGX Build System"
	@echo "================================================="
	@echo ""
	@echo "Target Platform: NVIDIA Jetson Orin AGX 32GB (ARM64 only)"
	@echo "CPU: Cortex-A78AE with NEON/Crypto extensions"
	@echo ""
	@echo "Targets:"
	@echo "  setup           - Initial setup (pyenv, venv, dependencies)"
	@echo "  build           - Build ARM64 production binary for Jetson"
	@echo "  build-ci        - Build in CI environment (ARM64 runners)"
	@echo "  clean           - Remove build artifacts"
	@echo "  distclean       - Remove everything including venv"
	@echo "  run-dev         - Run development version (uncompiled)"
	@echo "  test            - Test the built binary"
	@echo "  info            - Show build configuration"
	@echo "  help            - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - ARM64 architecture (aarch64) or ARM64 cross-compilation"
	@echo "  - clang compiler"
	@echo "  - pyenv (will be installed if missing)"
	@echo "  - Python 3.x (latest stable version)"
	@echo ""
	@echo "Optimizations:"
	@echo "  - Compiler: Clang with thin LTO"
	@echo "  - Flags: -O3 -march=armv8.2-a+crypto+fp16+rcpc+dotprod"
	@echo "  - Nuitka: Standalone single-file binary"