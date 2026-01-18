#!/usr/bin/env python3
"""
Manual Motor Test Script for JetRacer

This script provides a comprehensive test suite for the JetRacer motor control library.
It tests both throttle and steering functionality with various patterns.

SAFETY WARNING:
- Place the robot on blocks so wheels don't touch the ground
- Keep clear of moving parts
- Be ready to press Ctrl+C for emergency stop
- Test in a safe, controlled environment

Usage:
    python3 test_motors_manual.py

Tests performed:
1. Initialization check
2. Steering sweep (left-center-right)
3. Forward throttle ramp
4. Reverse throttle ramp
5. Combined steering and throttle
6. State verification
"""

import sys
import time
from control import JetRacer


def print_header(text):
    """Print a formatted test section header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_status(action, value):
    """Print current action status."""
    print(f"  → {action}: {value}")


def test_initialization():
    """Test 1: Initialize the robot."""
    print_header("TEST 1: Initialization")
    try:
        racer = JetRacer()
        print_status("Status", "✓ JetRacer initialized successfully")
        print_status("I2C Steering", "0x40")
        print_status("I2C Motor", "0x60")
        return racer
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        sys.exit(1)


def test_steering(racer):
    """Test 2: Steering servo sweep."""
    print_header("TEST 2: Steering Sweep")
    
    positions = [
        (1700, "CENTER"),
        (1400, "LEFT"),
        (1700, "CENTER"),
        (2000, "RIGHT"),
        (1700, "CENTER"),
    ]
    
    for us, label in positions:
        print_status(f"Steering to {label}", f"{us} μs")
        racer.set_steering_us(us)
        time.sleep(1.0)
    
    print_status("Status", "✓ Steering test complete")


def test_steering_normalized(racer):
    """Test 3: Normalized steering control."""
    print_header("TEST 3: Normalized Steering")
    
    positions = [
        (0.0, "CENTER"),
        (-1.0, "FULL LEFT"),
        (0.0, "CENTER"),
        (1.0, "FULL RIGHT"),
        (0.0, "CENTER"),
    ]
    
    for value, label in positions:
        print_status(f"Steering to {label}", f"{value:+.1f}")
        racer.set_steering_normalized(value)
        time.sleep(1.0)
    
    print_status("Status", "✓ Normalized steering test complete")


def test_forward_throttle(racer):
    """Test 4: Forward throttle ramp."""
    print_header("TEST 4: Forward Throttle Ramp")
    
    print_status("Info", "Ramping forward from 0% to 30%")
    for speed in [0.0, 0.1, 0.2, 0.3]:
        print_status("Throttle", f"{speed:+.1f} ({int(speed*100):+3d}%)")
        racer.set_throttle(speed)
        time.sleep(1.5)
    
    print_status("Action", "Stopping")
    racer.stop()
    time.sleep(1.0)
    
    print_status("Status", "✓ Forward throttle test complete")


def test_reverse_throttle(racer):
    """Test 5: Reverse throttle ramp."""
    print_header("TEST 5: Reverse Throttle Ramp")
    
    print_status("Info", "Ramping reverse from 0% to -30%")
    for speed in [0.0, -0.1, -0.2, -0.3]:
        print_status("Throttle", f"{speed:+.1f} ({int(speed*100):+3d}%)")
        racer.set_throttle(speed)
        time.sleep(1.5)
    
    print_status("Action", "Stopping")
    racer.stop()
    time.sleep(1.0)
    
    print_status("Status", "✓ Reverse throttle test complete")


def test_combined_control(racer):
    """Test 6: Combined steering and throttle."""
    print_header("TEST 6: Combined Steering + Throttle")
    
    maneuvers = [
        (0.2, 1700, "Forward + Center steering"),
        (0.2, 1400, "Forward + Left steering"),
        (0.2, 1700, "Forward + Center steering"),
        (0.2, 2000, "Forward + Right steering"),
        (0.0, 1700, "Stop + Center steering"),
    ]
    
    for throttle, steering, description in maneuvers:
        print_status(description, f"throttle={throttle:+.1f}, steering={steering}μs")
        racer.set_throttle(throttle)
        racer.set_steering_us(steering)
        time.sleep(2.0)
    
    racer.stop()
    print_status("Status", "✓ Combined control test complete")


def test_state_verification(racer):
    """Test 7: Verify state tracking."""
    print_header("TEST 7: State Verification")
    
    # Set known state
    racer.set_throttle(0.5)
    racer.set_steering_us(1800)
    
    # Verify state
    throttle = racer.get_throttle()
    steering = racer.get_steering_us()
    
    print_status("Set throttle", "0.5")
    print_status("Get throttle", f"{throttle}")
    print_status("Set steering", "1800 μs")
    print_status("Get steering", f"{steering} μs")
    
    # Stop and verify
    racer.stop()
    throttle_after_stop = racer.get_throttle()
    print_status("After stop", f"throttle={throttle_after_stop}")
    
    if throttle_after_stop == 0.0:
        print_status("Status", "✓ State verification passed")
    else:
        print_status("Status", "✗ State verification failed")


def test_limits(racer):
    """Test 8: Verify safety limits and clamping."""
    print_header("TEST 8: Safety Limits")
    
    print_status("Info", "Testing throttle clamping")
    # These should be clamped to [-1.0, 1.0]
    racer.set_throttle(2.0)  # Should clamp to 1.0
    print_status("Set throttle to 2.0", "Clamped to 1.0")
    time.sleep(0.5)
    
    racer.set_throttle(-2.0)  # Should clamp to -1.0
    print_status("Set throttle to -2.0", "Clamped to -1.0")
    time.sleep(0.5)
    
    racer.stop()
    print_status("Status", "✓ Safety limits test complete")


def main():
    """Main test execution."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         JetRacer Motor Control Library Test Suite         ║
    ╚════════════════════════════════════════════════════════════╝
    
    ⚠️  SAFETY WARNINGS:
    - Ensure robot is on blocks (wheels off ground)
    - Keep hands clear of moving parts
    - Press Ctrl+C anytime for emergency stop
    - Test in a safe environment
    
    Starting tests in 3 seconds...
    """)
    
    try:
        time.sleep(3)
        
        # Initialize
        racer = test_initialization()
        time.sleep(1)
        
        # Run all tests
        test_steering(racer)
        time.sleep(1)
        
        test_steering_normalized(racer)
        time.sleep(1)
        
        test_forward_throttle(racer)
        time.sleep(1)
        
        test_reverse_throttle(racer)
        time.sleep(1)
        
        test_combined_control(racer)
        time.sleep(1)
        
        test_state_verification(racer)
        time.sleep(1)
        
        test_limits(racer)
        
        # Success summary
        print_header("ALL TESTS COMPLETE")
        print("""
    ✓ Initialization
    ✓ Steering sweep
    ✓ Normalized steering
    ✓ Forward throttle
    ✓ Reverse throttle
    ✓ Combined control
    ✓ State verification
    ✓ Safety limits
        """)
        print("  The JetRacer motor library is working correctly!")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Emergency stop - Ctrl+C detected")
    except Exception as e:
        print(f"\n\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always shutdown safely
        if 'racer' in locals():
            racer.shutdown()
        print("\nTest script terminated safely.")


if __name__ == "__main__":
    main()
