#!/usr/bin/env python3
"""
JetRacer Library Verification Script

This script verifies the library installation without requiring hardware.
Run this before attempting hardware tests to ensure everything is set up correctly.

Usage:
    python3 verify_library.py
"""

import sys
import importlib.util
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def check_result(condition, success_msg, failure_msg):
    """Print check result."""
    if condition:
        print(f"  ✓ {success_msg}")
        return True
    else:
        print(f"  ✗ {failure_msg}")
        return False


def verify_python_version():
    """Check Python version."""
    print_section("Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"  Python {version_str}")
    
    if version.major == 3 and version.minor >= 7:
        print("  ✓ Version is compatible")
        return True
    else:
        print("  ✗ Python 3.7+ required")
        return False


def verify_dependencies():
    """Check required dependencies."""
    print_section("Dependencies")
    
    deps = [
        ('board', 'Adafruit Blinka'),
        ('busio', 'Adafruit BusIO'),
        ('adafruit_pca9685', 'PCA9685 Driver'),
    ]
    
    all_ok = True
    for module_name, display_name in deps:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"  ✓ {display_name:<20} (installed)")
        else:
            print(f"  ✗ {display_name:<20} (missing)")
            all_ok = False
    
    return all_ok


def verify_library_structure():
    """Check library file structure."""
    print_section("Library Structure")
    
    base = Path(__file__).parent
    
    files = [
        ('control/__init__.py', 'Package init'),
        ('control/motors.py', 'Motor control'),
        ('control/README.md', 'API documentation'),
        ('quick_test.py', 'Quick test'),
        ('test_motors_manual.py', 'Full test suite'),
        ('examples.py', 'Usage examples'),
        ('run_tests.sh', 'Test runner'),
        ('TESTING.md', 'Test documentation'),
        ('LIBRARY_SUMMARY.md', 'Library summary'),
    ]
    
    all_ok = True
    for filepath, description in files:
        full_path = base / filepath
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✓ {description:<25} ({size:>6} bytes)")
        else:
            print(f"  ✗ {description:<25} (missing)")
            all_ok = False
    
    return all_ok


def verify_library_import():
    """Check if library can be imported."""
    print_section("Library Import")
    
    try:
        from control import JetRacer
        print("  ✓ Control module imported")
        print(f"  ✓ JetRacer class: {JetRacer.__name__}")
        
        # Check methods
        expected_methods = [
            'set_throttle',
            'set_steering_us',
            'set_steering_normalized',
            'stop',
            'shutdown',
            'get_throttle',
            'get_steering_us',
        ]
        
        methods = [m for m in dir(JetRacer) if not m.startswith('_')]
        
        print("\n  Available methods:")
        for method in expected_methods:
            if method in methods:
                print(f"    ✓ {method}")
            else:
                print(f"    ✗ {method} (missing)")
                return False
        
        return True
        
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False


def verify_syntax():
    """Check Python syntax of all files."""
    print_section("Syntax Validation")
    
    import py_compile
    base = Path(__file__).parent
    
    files = [
        'control/__init__.py',
        'control/motors.py',
        'quick_test.py',
        'test_motors_manual.py',
        'examples.py',
        'verify_library.py',
    ]
    
    all_ok = True
    for filepath in files:
        full_path = base / filepath
        if not full_path.exists():
            continue
            
        try:
            py_compile.compile(str(full_path), doraise=True)
            print(f"  ✓ {filepath:<30} (valid syntax)")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {filepath:<30} (syntax error)")
            print(f"    {e}")
            all_ok = False
    
    return all_ok


def verify_permissions():
    """Check file permissions."""
    print_section("File Permissions")
    
    base = Path(__file__).parent
    
    executable_files = [
        'quick_test.py',
        'test_motors_manual.py',
        'examples.py',
        'run_tests.sh',
    ]
    
    all_ok = True
    for filepath in executable_files:
        full_path = base / filepath
        if full_path.exists():
            is_executable = full_path.stat().st_mode & 0o111
            if is_executable:
                print(f"  ✓ {filepath:<25} (executable)")
            else:
                print(f"  ⚠ {filepath:<25} (not executable)")
                # Not critical, just a warning
        else:
            print(f"  ✗ {filepath:<25} (missing)")
            all_ok = False
    
    return all_ok


def main():
    """Run all verification checks."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║      JetRacer Library Verification                       ║
╚═══════════════════════════════════════════════════════════╝

This script verifies the library installation without hardware.
    """)
    
    checks = [
        ("Python Version", verify_python_version),
        ("Dependencies", verify_dependencies),
        ("Library Structure", verify_library_structure),
        ("Syntax Validation", verify_syntax),
        ("Library Import", verify_library_import),
        ("File Permissions", verify_permissions),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ✗ Check failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print_section("Verification Summary")
    print()
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"  {symbol} {name:<25} [{status}]")
        if not passed:
            all_passed = False
    
    print()
    print("="*60)
    
    if all_passed:
        print("""
✓ All checks passed!

The library is properly installed and ready for testing.

Next steps:
  1. Place robot on blocks
  2. Run: python3 quick_test.py
  3. If successful, run: python3 test_motors_manual.py

See TESTING.md for detailed testing instructions.
""")
        return 0
    else:
        print("""
✗ Some checks failed.

Please fix the issues above before running hardware tests.

Common fixes:
  - Install dependencies: uv sync
  - Activate venv: source .venv/bin/activate
  - Make files executable: chmod +x *.py *.sh

See README.md for setup instructions.
""")
        return 1


if __name__ == "__main__":
    sys.exit(main())
