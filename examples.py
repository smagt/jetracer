#!/usr/bin/env python3
"""
Example: Basic JetRacer Usage

This demonstrates the most common usage patterns for the JetRacer library.
Use this as a template for your own programs.
"""

import time
from control import JetRacer


def example_basic_movement():
    """Example 1: Basic forward/reverse movement."""
    print("\n=== Example 1: Basic Movement ===")
    
    racer = JetRacer()
    
    try:
        # Move forward
        print("Moving forward...")
        racer.set_throttle(0.3)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        racer.stop()
        time.sleep(1)
        
        # Move backward
        print("Moving backward...")
        racer.set_throttle(-0.3)
        time.sleep(2)
        
        # Stop
        racer.stop()
        
    finally:
        racer.shutdown()


def example_steering():
    """Example 2: Steering control."""
    print("\n=== Example 2: Steering ===")
    
    racer = JetRacer()
    
    try:
        # Center
        print("Center steering...")
        racer.set_steering_us(1700)
        time.sleep(1)
        
        # Turn left (using microseconds)
        print("Turn left...")
        racer.set_steering_us(1400)
        time.sleep(1)
        
        # Turn right (using normalized values)
        print("Turn right...")
        racer.set_steering_normalized(1.0)  # -1.0 to 1.0
        time.sleep(1)
        
        # Center
        racer.set_steering_normalized(0.0)
        
    finally:
        racer.shutdown()


def example_combined():
    """Example 3: Combined steering and throttle."""
    print("\n=== Example 3: Combined Control ===")
    
    racer = JetRacer()
    
    try:
        # Drive forward while turning
        print("Forward + turning...")
        racer.set_throttle(0.3)
        racer.set_steering_normalized(-0.5)  # Slight left
        time.sleep(2)
        
        racer.set_steering_normalized(0.5)   # Slight right
        time.sleep(2)
        
        racer.stop()
        racer.set_steering_normalized(0.0)
        
    finally:
        racer.shutdown()


def example_state_tracking():
    """Example 4: Reading current state."""
    print("\n=== Example 4: State Tracking ===")
    
    racer = JetRacer()
    
    try:
        # Set some values
        racer.set_throttle(0.5)
        racer.set_steering_us(1800)
        
        # Read them back
        current_throttle = racer.get_throttle()
        current_steering = racer.get_steering_us()
        
        print(f"Current throttle: {current_throttle}")
        print(f"Current steering: {current_steering} μs")
        
        racer.stop()
        
    finally:
        racer.shutdown()


def example_safety():
    """Example 5: Safety features."""
    print("\n=== Example 5: Safety Features ===")
    
    racer = JetRacer()
    
    try:
        # Values are automatically clamped
        print("Testing automatic clamping...")
        racer.set_throttle(2.0)   # Will be clamped to 1.0
        print(f"Set 2.0, got: {racer.get_throttle()}")
        
        racer.set_throttle(-2.0)  # Will be clamped to -1.0
        print(f"Set -2.0, got: {racer.get_throttle()}")
        
        # Emergency stop
        racer.set_throttle(0.5)
        print("Running...")
        time.sleep(0.5)
        racer.stop()  # Emergency stop!
        print("Emergency stopped!")
        
    finally:
        racer.shutdown()


def example_custom_loop():
    """Example 6: Custom control loop."""
    print("\n=== Example 6: Custom Control Loop ===")
    
    racer = JetRacer()
    
    try:
        print("Running custom control loop for 5 seconds...")
        print("Press Ctrl+C to stop early")
        
        start_time = time.time()
        while time.time() - start_time < 5.0:
            # Example: Sinusoidal steering
            elapsed = time.time() - start_time
            steering = 0.5 * (1.0 if (elapsed % 2) < 1 else -1.0)
            
            racer.set_throttle(0.2)
            racer.set_steering_normalized(steering)
            
            time.sleep(0.1)
        
        racer.stop()
        
    except KeyboardInterrupt:
        print("\nInterrupted!")
    finally:
        racer.shutdown()


def main():
    """Run all examples."""
    print("""
╔═══════════════════════════════════════════════════════╗
║         JetRacer Library Usage Examples              ║
╚═══════════════════════════════════════════════════════╝

⚠️  SAFETY: Ensure robot is on blocks!

Press Ctrl+C at any time to stop.
    """)
    
    try:
        input("Press Enter to start examples (or Ctrl+C to cancel)...")
        
        example_basic_movement()
        time.sleep(1)
        
        example_steering()
        time.sleep(1)
        
        example_combined()
        time.sleep(1)
        
        example_state_tracking()
        time.sleep(1)
        
        example_safety()
        time.sleep(1)
        
        # Uncomment to run the custom loop example
        # example_custom_loop()
        
        print("\n" + "="*55)
        print("  All examples completed successfully!")
        print("="*55 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")


if __name__ == "__main__":
    main()
