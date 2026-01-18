#!/usr/bin/env python3
"""
Keyboard Teleoperation for JetRacer

Controls:
- W/S: Increase/decrease throttle (incremental)
- A/D: Steer left/right
- SPACE: Emergency stop (set throttle to 0)
- Q: Quit

SAFETY: Ensure robot is in a safe area before driving!
"""

import sys
import termios
import tty
from pathlib import Path

# Add parent directory to path so we can import control module
sys.path.insert(0, str(Path(__file__).parent.parent))

from control import JetRacer

car = JetRacer()
STEER_CENTER = 1700
STEER_LEFT   = 1400
STEER_RIGHT  = 2000
speed = 0.0


def getch():
    """Get a single character from stdin without echo."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


print("""
╔═══════════════════════════════════════════════════════╗
║         JetRacer Keyboard Control                    ║
╚═══════════════════════════════════════════════════════╝

Controls:
  W/S  - Throttle up/down (±5% per press, max ±50%)
  A/D  - Steer left/right
  SPACE - Emergency stop
  Q    - Quit

⚠️  SAFETY: Ensure robot is in a safe area!
Press Ctrl+C anytime for emergency stop.

Starting...
""")

try:
    car.set_steering_us(STEER_CENTER)
    
    while True:
        c = getch()
        
        if c == 'w':
            speed = min(speed + 0.05, 0.5)
            print(f"\r  Throttle: {speed:+.2f} ({int(speed*100):+3d}%)  ", end='', flush=True)
        elif c == 's':
            speed = max(speed - 0.05, -0.5)
            print(f"\r  Throttle: {speed:+.2f} ({int(speed*100):+3d}%)  ", end='', flush=True)
        elif c == 'a':
            car.set_steering_us(STEER_LEFT)
            print(f"\r  Steering: LEFT    Throttle: {speed:+.2f}  ", end='', flush=True)
        elif c == 'd':
            car.set_steering_us(STEER_RIGHT)
            print(f"\r  Steering: RIGHT   Throttle: {speed:+.2f}  ", end='', flush=True)
        elif c == ' ':
            speed = 0.0
            car.set_steering_us(STEER_CENTER)
            print(f"\r  ⚠️  EMERGENCY STOP                  ", end='', flush=True)
        elif c == 'q':
            print("\r\nQuitting...                            ")
            break

        car.set_throttle(speed)

except KeyboardInterrupt:
    print("\n\n⚠️  Emergency stop - Ctrl+C detected")
finally:
    car.shutdown()
    print("Keyboard control terminated safely.\n")
