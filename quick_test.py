#!/usr/bin/env python3
"""
Quick Motor Test - Simple validation of basic functionality

This is a minimal test to verify the motor library works.
Use this for quick checks after hardware changes or library updates.

SAFETY: Place robot on blocks before running!

Usage:
    python3 quick_test.py
"""

import time
from control import JetRacer


def main():
    print("\n" + "="*50)
    print("  JetRacer Quick Motor Test")
    print("="*50)
    print("\n⚠️  Ensure robot is on blocks!")
    print("Starting in 2 seconds...\n")
    time.sleep(2)
    
    try:
        # Initialize
        print("[1/5] Initializing...")
        racer = JetRacer()
        time.sleep(0.5)
        
        # Test steering
        print("[2/5] Testing steering center...")
        racer.set_steering_us(1700)
        time.sleep(1)
        
        # Test forward
        print("[3/5] Testing forward (20%)...")
        racer.set_throttle(0.2)
        time.sleep(2)
        racer.stop()
        time.sleep(1)
        
        # Test reverse
        print("[4/5] Testing reverse (20%)...")
        racer.set_throttle(-0.2)
        time.sleep(2)
        racer.stop()
        time.sleep(1)
        
        # Cleanup
        print("[5/5] Shutting down...")
        racer.shutdown()
        
        print("\n✓ Quick test passed!")
        print("  - Initialization: OK")
        print("  - Steering: OK")
        print("  - Forward: OK")
        print("  - Reverse: OK")
        print("="*50 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if 'racer' in locals():
            racer.shutdown()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        if 'racer' in locals():
            racer.shutdown()
        raise


if __name__ == "__main__":
    main()
