#!/bin/bash
# JetRacer Keyboard Drive Launcher
# Convenient script to launch keyboard control from anywhere

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Launching keyboard control..."
python3 control/keyboard_drive.py
