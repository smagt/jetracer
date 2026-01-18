import time
import board
import busio
from adafruit_pca9685 import PCA9685

FREQ = 50
CH = 0
CENTRE_US = 1700

def us_to_duty(us):
    period_us = 1_000_000 / FREQ
    return int(us / period_us * 65535)

def calibrate_position(ch, name, start_us=1500):
    """Interactively calibrate a servo position"""
    current_us = start_us
    print(f"\n--- Calibrating {name} position ---")
    print("Commands: +/- (adjust by 50us), ++/-- (adjust by 10us), 'ok' when done")
    
    ch.duty_cycle = us_to_duty(current_us)
    
    while True:
        cmd = input(f"Current: {current_us}us > ").strip().lower()
        
        if cmd == 'ok':
            print(f"{name} position set to {current_us}us")
            return current_us
        elif cmd == '+':
            current_us += 50
        elif cmd == '-':
            current_us -= 50
        elif cmd == '++':
            current_us += 10
        elif cmd == '--':
            current_us -= 10
        else:
            try:
                current_us = int(cmd)
            except ValueError:
                print("Invalid command. Use +, -, ++, --, a number, or 'ok'")
                continue
        
        current_us = max(500, min(2500, current_us))
        ch.duty_cycle = us_to_duty(current_us)
        print(f"Set to {current_us}us")

# Initialize I2C and PCA9685
# Use the standard I2C pins on Raspberry Pi
from board import SCL, SDA
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x40)
pca.frequency = FREQ
ch = pca.channels[CH]

try:
    # Calibrate left and right positions
    left_us = calibrate_position(ch, "LEFT", 1000)
    right_us = calibrate_position(ch, "RIGHT", 2000)
    
    # Calculate center
    centre_us = (left_us + right_us) // 2
    print(f"\nCalculated centre: {centre_us}us (average of {left_us}us and {right_us}us)")
    
    # Set to center and hold
    ch.duty_cycle = us_to_duty(centre_us)
    print(f"\nHolding centre at {centre_us}us. Ctrl+C to stop.")
    
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    pca.deinit()
