#!/bin/bash

# Exit on any error
set -e

# Define layout paths
LAYOUTS_DIR="your-base-path/bash-scripts/zellij/layouts"
AIIO_LAYOUT="${LAYOUTS_DIR}/aiio-terminal-layout.kdl"

# Function to print usage
print_usage() {
    echo "Usage: ./open-zellij.sh [layout]"
    echo "Available layouts:"
    echo "  1. aiio - AI Development Layout"
}

# If no argument provided, show menu
if [ $# -eq 0 ]; then
    echo "Please select a layout:"
    echo "1) aiio - AI Development Layout"
    read -p "Enter your choice (1): " choice
else
    choice=$1
fi

# Convert choice to layout path
case "$choice" in
    "1"|"aiio")
        layout_path="$AIIO_LAYOUT"
        layout_name="aiio"
        ;;
    "-h"|"--help")
        print_usage
        exit 0
        ;;
    *)
        echo "Error: Invalid layout selection"
        print_usage
        exit 1
        ;;
esac

# Check if zellij is installed
if ! command -v zellij >/dev/null 2>&1; then
    echo "Error: Zellij is not installed"
    echo "Please install Zellij first using the install-zellij.sh script"
    exit 1
fi

# Check if layout file exists
if [ ! -f "$layout_path" ]; then
    echo "Error: Layout file not found at: $layout_path"
    exit 1
fi

# Launch zellij with the selected layout
echo "Opening Zellij with $layout_name layout..."
zellij --layout "$layout_path" 