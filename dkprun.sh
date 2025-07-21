#!/bin/bash

# Usage: ./install.sh <repo_url>
# Example: ./install.sh https://github.com/user/repo.git

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <repo_url>"
    exit 1
fi

REPO_URL="$1"
TARGET_DIR="/opt/dkprun"

echo "Cloning repo $REPO_URL into $TARGET_DIR"
if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"
fi

sudo git clone "$REPO_URL" "$TARGET_DIR"

if [ ! -f "$TARGET_DIR/dkprun.py" ]; then
    echo "dkprun.py not found in the repo." >&2
    exit 1
fi

if [ ! -f "$TARGET_DIR/dkprun.bat" ]; then
    echo "dkprun.bat not found in the repo." >&2
    exit 2
fi

echo "Files found in $TARGET_DIR"

# Add the folder to the system PATH (for all users)
if ! echo "$PATH" | grep -q "$TARGET_DIR" ; then
    PROFILE_FILE="/etc/profile.d/dkprun.sh"
    echo "Adding $TARGET_DIR to system PATH via $PROFILE_FILE..."
    echo "export PATH=\$PATH:$TARGET_DIR" | sudo tee "$PROFILE_FILE" > /dev/null
    echo "PATH updated (system). Restart your terminal or log out/in to apply the changes."
else
    echo "$TARGET_DIR is already in PATH."
fi

echo "Installation complete!"
