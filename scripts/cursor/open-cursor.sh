#!/bin/bash

# and add below alias in ~/.bash_aliases
# alias cursor='/path-to-this-script/open-cursor.sh'

# Get the absolute path of the argument or use current directory if no argument
TARGET_DIR=$(realpath "${1:-.}")

# Store the Cursor AppRun directory
CURSOR_DIR="/opt/cursor"

# Export APPDIR for the AppRun script
export APPDIR="$CURSOR_DIR"

# Run AppRun with the target directory, redirect output to /dev/null, run in background and disown
"$CURSOR_DIR/AppRun" "$TARGET_DIR" >/dev/null 2>&1 & disown