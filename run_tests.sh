#!/bin/bash
# JetRacer Test Runner
# Quick helper script to run various tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

show_menu() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║         JetRacer Test Menu                           ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    echo "Available tests:"
    echo ""
    echo "  1) Quick Test         - Fast validation (~30 seconds)"
    echo "  2) Full Test Suite    - Comprehensive tests (~3 minutes)"
    echo "  3) Examples           - Usage demonstrations"
    echo "  4) Library Check      - Verify import and structure"
    echo "  5) List Files         - Show project structure"
    echo ""
    echo "  q) Quit"
    echo ""
}

run_quick_test() {
    echo ""
    echo "Running Quick Test..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 quick_test.py
}

run_full_test() {
    echo ""
    echo "Running Full Test Suite..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 test_motors_manual.py
}

run_examples() {
    echo ""
    echo "Running Examples..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 examples.py
}

check_library() {
    echo ""
    echo "Checking Library..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 -c "
from control import JetRacer
import inspect

print('✓ Import successful')
print(f'✓ Class: {JetRacer.__name__}')
print(f'✓ Module: {JetRacer.__module__}')
print('')
print('Available methods:')
methods = [m for m in dir(JetRacer) if not m.startswith('_')]
for m in methods:
    method = getattr(JetRacer, m)
    if callable(method):
        sig = inspect.signature(method)
        print(f'  - {m}{sig}')
    else:
        print(f'  - {m}')
print('')
print('✓ Library structure verified')
"
}

list_files() {
    echo ""
    echo "Project Structure:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Test Scripts:"
    ls -lh quick_test.py test_motors_manual.py examples.py 2>/dev/null || echo "  (none found)"
    echo ""
    echo "Library Files:"
    ls -lh control/*.py 2>/dev/null || echo "  (none found)"
    echo ""
    echo "Documentation:"
    ls -lh README.md control/README.md LIBRARY_SUMMARY.md 2>/dev/null || echo "  (none found)"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Select option: " choice
    
    case $choice in
        1)
            run_quick_test
            ;;
        2)
            run_full_test
            ;;
        3)
            run_examples
            ;;
        4)
            check_library
            ;;
        5)
            list_files
            ;;
        q|Q)
            echo ""
            echo "Goodbye!"
            echo ""
            exit 0
            ;;
        *)
            echo ""
            echo "Invalid option: $choice"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
