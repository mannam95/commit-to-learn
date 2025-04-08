#!/bin/bash

# Exit on any error
set -e

# Get the architecture of the machine
arch=$(uname -m)
os=$(uname -s)

# Print the architecture and OS
echo "Architecture: $arch"
echo "OS: $os"

# constants
zellij_url="https://github.com/zellij-org/zellij/releases/latest/download"

# standard location for user-installed programs
install_dir="/usr/local/bin"

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

# Download the Zellij binary
case "$os" in
    "Darwin")
        filename="zellij-${arch}-apple-darwin.tar.gz"
        echo "Downloading Zellij binary for macOS..."
        ;;
    "Linux")
        filename="zellij-${arch}-unknown-linux-musl.tar.gz"
        echo "Downloading Zellij binary for Linux..."
        ;;
    *)
        echo "Unsupported OS: $os"
        exit 1
        ;;
esac

url="${zellij_url}/${filename}"
if ! curl -LO "$url"; then
    echo "Failed to download Zellij"
    exit 1
fi

# Uncompress the Zellij binary
echo "Uncompressing Zellij binary..."
if ! tar -xf "$filename"; then
    echo "Failed to extract archive"
    rm "$filename"
    exit 1
fi

# Move the Zellij binary to the install directory
echo "Moving Zellij binary to $install_dir directory..."
if ! mv "./zellij" "$install_dir/zellij"; then
    echo "Failed to move binary to $install_dir"
    rm "$filename" "./zellij"
    exit 1
fi

# Set correct permissions
chmod 755 "$install_dir/zellij"

# Remove the .tar.gz file
echo "Removing .tar.gz file..."
rm "$filename"

# Check if the Zellij binary exists and is executable
if [ -x "$install_dir/zellij" ]; then
    echo "Zellij binary installed successfully!"
    echo "You can now run 'zellij' to start using it"
else
    echo "Zellij binary not installed successfully!"
    exit 1
fi
