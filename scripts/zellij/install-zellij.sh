#!/bin/bash

# Exit on any error
set -e

# Constants
ZELLIJ_URL="https://github.com/zellij-org/zellij/releases/latest/download"
INSTALL_DIR="/usr/local/bin"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

show_usage() {
    echo "Usage: $0 [OPTION]"
    echo "Install or manage Zellij terminal multiplexer"
    echo ""
    echo "Options:"
    echo "  install    Install or update Zellij (default)"
    echo "  uninstall  Remove Zellij from the system"
    echo "  --help     Show this help message"
}

get_installed_version() {
    if command -v zellij &> /dev/null; then
        zellij --version 2>/dev/null | awk '{print $2}'
    else
        echo "not installed"
    fi
}

uninstall_zellij() {
    if [ "$EUID" -ne 0 ]; then
        error "Please run with sudo"
    fi

    if [ -f "$INSTALL_DIR/zellij" ]; then
        info "Removing Zellij from $INSTALL_DIR..."
        rm -f "$INSTALL_DIR/zellij"
        info "Zellij has been uninstalled successfully!"
    else
        warn "Zellij is not installed at $INSTALL_DIR"
    fi
}

install_zellij() {
    # Check if running with sudo
    if [ "$EUID" -ne 0 ]; then
        error "Please run with sudo"
    fi

    # Get the architecture of the machine
    arch=$(uname -m)
    os=$(uname -s)

    info "Architecture: $arch"
    info "OS: $os"

    # Check for existing installation
    current_version=$(get_installed_version)
    if [ "$current_version" != "not installed" ]; then
        warn "Zellij is already installed (version: $current_version)"
        warn "This will update/reinstall Zellij"
    fi

    # Create temporary directory for download
    tmp_dir=$(mktemp -d)
    trap 'rm -rf "$tmp_dir"' EXIT

    # Determine the correct binary filename
    case "$os" in
        "Darwin")
            filename="zellij-${arch}-apple-darwin.tar.gz"
            info "Downloading Zellij binary for macOS..."
            ;;
        "Linux")
            filename="zellij-${arch}-unknown-linux-musl.tar.gz"
            info "Downloading Zellij binary for Linux..."
            ;;
        *)
            error "Unsupported OS: $os"
            ;;
    esac

    url="${ZELLIJ_URL}/${filename}"
    info "Download URL: $url"

    # Download to temporary directory
    if ! curl -fsSL -o "$tmp_dir/$filename" "$url"; then
        error "Failed to download Zellij"
    fi

    # Uncompress the Zellij binary
    info "Extracting Zellij binary..."
    if ! tar -xf "$tmp_dir/$filename" -C "$tmp_dir"; then
        error "Failed to extract archive"
    fi

    # Backup existing binary if it exists
    if [ -f "$INSTALL_DIR/zellij" ]; then
        info "Backing up existing Zellij binary..."
        mv "$INSTALL_DIR/zellij" "$INSTALL_DIR/zellij.backup"
    fi

    # Move the Zellij binary to the install directory
    info "Installing Zellij to $INSTALL_DIR..."
    if ! mv "$tmp_dir/zellij" "$INSTALL_DIR/zellij"; then
        # Restore backup if move fails
        if [ -f "$INSTALL_DIR/zellij.backup" ]; then
            mv "$INSTALL_DIR/zellij.backup" "$INSTALL_DIR/zellij"
        fi
        error "Failed to move binary to $INSTALL_DIR"
    fi

    # Set correct permissions
    chmod 755 "$INSTALL_DIR/zellij"

    # Remove backup after successful install
    rm -f "$INSTALL_DIR/zellij.backup"

    # Verify installation
    if [ -x "$INSTALL_DIR/zellij" ]; then
        new_version=$("$INSTALL_DIR/zellij" --version 2>/dev/null | awk '{print $2}')
        info "Zellij $new_version installed successfully!"
        if [ "$current_version" != "not installed" ]; then
            info "Updated from $current_version to $new_version"
        fi
        info "Run 'zellij' to start using it"
    else
        error "Zellij binary not installed successfully!"
    fi
}

# Main script logic
case "${1:-install}" in
    install)
        install_zellij
        ;;
    uninstall)
        uninstall_zellij
        ;;
    --help|-h)
        show_usage
        ;;
    *)
        error "Unknown option: $1. Use --help for usage information."
        ;;
esac
