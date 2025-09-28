# Panopticon

A high-performance real-time monitoring system built exclusively for NVIDIA Jetson Orin AGX 32GB platforms. This is an ARM64-only application optimized specifically for the Cortex-A78AE CPU architecture found in Jetson Orin modules.

## Features

- Real-time system state monitoring via Redis streams
- Health metrics tracking for distributed services
- TimescaleDB integration for historical data analysis
- WebSocket-based real-time updates
- Terminal UI built with Textual
- Optimized ARM64 binary with Nuitka compilation

## Architecture

Panopticon connects to multiple data sources:
- **Redis** - Real-time state and health metrics
- **TimescaleDB** - Historical logs and commands
- **WebSockets** - Real-time communication with Lighthouse backend

## Prerequisites

### Build Requirements
- Python 3.x (latest stable version, managed via pyenv)
- Clang 21 compiler (latest stable for optimal ARM64 performance, falls back to system clang)
- Nuitka 2.4.11+ (for binary compilation)
- pyenv (will be installed automatically if missing)

### Runtime Requirements
- **Platform**: NVIDIA Jetson Orin AGX 32GB (ARM64/aarch64 only)
- **OS**: Ubuntu 22.04 LTS (L4T/JetPack)
- Redis server(s) (ports 8084, 8085)
- TimescaleDB/PostgreSQL (port 8094)

## Configuration

### Credentials Management

The system uses a TOML configuration file for credentials. The `make setup` command automatically creates a template.

```toml
[redis.main]
host = "127.0.0.1"
port = 8084
db = 1
username = "your_redis_username"
password = "your_redis_password"

[redis.health]
host = "127.0.0.1"
port = 8084
db = 2
username = "your_health_username"
password = "your_health_password"

[database]
host = "localhost"
port = 8094
database = "your_database"
user = "your_db_user"
password = "your_db_password"
```

### Environment Variables

Alternatively, use environment variables (useful for containerized deployments):

#### Redis Configuration
- `REDIS_MAIN_HOST`, `REDIS_MAIN_PORT`, `REDIS_MAIN_DB`
- `REDIS_MAIN_USERNAME`, `REDIS_MAIN_PASSWORD`
- `REDIS_HEALTH_HOST`, `REDIS_HEALTH_PORT`, `REDIS_HEALTH_DB`
- `REDIS_HEALTH_USERNAME`, `REDIS_HEALTH_PASSWORD`

#### Database Configuration
- `DB_HOST`, `DB_PORT`, `DB_NAME`
- `DB_USER`, `DB_PASSWORD`

### Configuration Priority
1. Environment variables (highest priority)
2. `credentials.toml` in current directory
3. `~/.config/panopticon/credentials.toml`
4. `/etc/panopticon/credentials.toml`
5. Default values (lowest priority)

## Usage

### Running the compiled binary:
```bash
./dist/panopticon
```

### Running in development mode:
```bash
make run-dev
```

## Build System

The project uses a Makefile with Nuitka to create highly optimized ARM64 binaries specifically for NVIDIA Jetson Orin AGX.

### Automatic Binding Updates

The build system automatically checks for updates to the Python bindings submodule before each build:
- **Local builds**: Prompts to update if newer bindings are available
- **CI builds**: Automatically commits and pushes updates, then restarts the build
- This ensures you always build with the latest C structure bindings

### Available Make Targets

```bash
make           # Shows help (default)
make help      # Display all available targets
make setup     # Complete initial setup (pyenv, venv, deps, credentials)
make build     # Build Jetson ARM64 production binary (checks for binding updates)
make build-ci  # Build in CI environment (ARM64 runners only)
make run-dev   # Run development version without compilation
make test      # Test the built binary
make clean     # Remove build artifacts
make distclean # Remove everything including virtual environment
make info      # Show build configuration and optimizations
make check-bindings  # Manually check for binding updates
```

### CI/CD

GitHub Actions automatically builds Jetson ARM64 binaries on:
- Push to main/master/develop branches
- Pull requests
- Git tags (triggers releases)

**Important**: The CI requires Ubuntu 22.04 ARM64 runners. x86_64 runners are not supported as this is a Jetson-specific build.

## Optimization Details

The build system produces highly optimized binaries for NVIDIA Jetson Orin AGX 32GB:

### Compiler Optimizations
- **Compiler**: Clang 21 with thin LTO (Link Time Optimization)
- **Architecture**: ARM64 Cortex-A78AE specific optimizations
  - Native: `-mcpu=native` (when building on target)
  - Cross-compile: `-march=armv8.2-a+crypto+fp16+rcpc+dotprod`
- **Optimization Flags**:
  - `-O3` - Maximum optimization level
  - `-flto=thin` - Thin link-time optimization
  - `-ffast-math` - Aggressive floating-point optimizations
  - `-funroll-loops` - Loop unrolling
  - `-ftree-vectorize` - Auto-vectorization
  - `-fomit-frame-pointer` - Omit frame pointers
  - `-finline-functions` - Aggressive inlining
  - `-fprefetch-loop-arrays` - Prefetch arrays in loops

### Nuitka Optimizations
- Standalone single-file executable
- Python optimizations (no site packages, no asserts, no docstrings)
- Static linking where possible
- Removed debug symbols for smaller binary

## Development

### Initial Setup
```bash
# Complete setup with pyenv, latest Python, and dependencies
make setup
```

### Development Workflow
```bash
# Run without compilation for rapid iteration
make run-dev

# Check current build configuration
make info

# Clean and rebuild
make clean
make build

# Test the built binary
make test
```

### Cleanup Options
```bash
make clean      # Remove build artifacts only
make distclean  # Remove everything (venv, pyenv config, builds)
```

## Submodules

This project includes C structure Python bindings as a submodule:
- `c_data_python_bindings` - Auto-generated ctypes bindings for C data structures

### Submodule Management
```bash
# Initial clone with submodules
git clone --recursive https://github.com/yourusername/panopticon.git

# Update submodules after pull
git submodule update --init --recursive

# Update to latest submodule commits
git submodule update --remote --merge
```

## Troubleshooting

### Build Issues

**pyenv not found**: The Makefile will attempt to install pyenv automatically. If this fails:
```bash
curl https://pyenv.run | bash
# Add pyenv to your PATH as instructed, then restart your shell
```

**Python installation fails**: Ensure build dependencies are installed:
```bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev \
    libffi-dev liblzma-dev python3-openssl
```

**Nuitka compilation errors**: Ensure clang is installed:
```bash
sudo apt-get install clang lld
```

### Runtime Issues

**Connection refused errors**: Verify Redis and PostgreSQL are running:
```bash
# Check Redis
redis-cli -p 8084 ping

# Check PostgreSQL/TimescaleDB
psql -h localhost -p 8094 -U your_user -d your_database -c "SELECT 1"
```

**Missing credentials**: Ensure `credentials.toml` exists and is properly configured:
```bash
ls -la credentials.toml
# Should show the file exists and is readable
```
