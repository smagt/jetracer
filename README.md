# JetRacer (Raspberry Pi + Waveshare) – Motor Control

This repository contains a fully working motor and steering control stack
for a JetRacer / Waveshare chassis using a Raspberry Pi 4.

Motor control does NOT use Raspberry Pi GPIO directly.
All motor and steering signals are driven via I2C using PCA9685 controllers.

## Quick Start

```python
from control import JetRacer
import time

racer = JetRacer()
try:
    racer.set_throttle(0.5)      # 50% forward
    racer.set_steering_us(1700)  # Center
    time.sleep(2)
finally:
    racer.shutdown()
```

**See `control/README.md` for complete API documentation.**

------------------------------------------------------------

TESTING THE LIBRARY

The motor control library has been converted into a reusable Python package.

Quick validation:
```bash
cd /home/pi/jetracer
python3 quick_test.py
```

Full test suite:
```bash
python3 test_motors_manual.py
```

⚠️ **SAFETY**: Always place the robot on blocks before testing!

------------------------------------------------------------

HARDWARE ARCHITECTURE

Two PCA9685 PWM controllers are present on the board:

- I2C address 0x40 : steering servo
- I2C address 0x60 : DC motor control (via TB6612FNG)

The TB6612FNG motor driver is always enabled (STBY tied high).

------------------------------------------------------------

DISCOVERED MOTOR PIN MAPPING

Motor A:
- PWMA  (TB6612 pin 23) -> PCA9685 channel 7
- AIN1  (TB6612 pin 21) -> PCA9685 channel 5
- AIN2  (TB6612 pin 22) -> PCA9685 channel 6

Motor B:
- PWMB  (TB6612 pin 15) -> PCA9685 channel 0
- BIN1  (TB6612 pin 17) -> PCA9685 channel 2
- BIN2  (TB6612 pin 16) -> PCA9685 channel 1

Steering:
- PCA9685 address 0x40
- channel 0
- centre approximately 1700 microseconds

------------------------------------------------------------

REPOSITORY STRUCTURE

.
|-- control/
|   |-- motors.py          unified steering + throttle driver
|   |-- keyboard_drive.py  keyboard teleoperation (WASD)
|   |-- estop.py           emergency stop helper
|
|-- tests/
|   |-- throttle_test.py   final validated motor test
|   |-- pca60_pulse.py     PCA9685 discovery at 0x60
|   |-- pca60_pwma_find.py find PWMA channel
|   |-- pca60_dir_find.py  find direction pins
|   |-- pca60_dir_scan.py  full direction scan
|   |-- gpio_pulse_scan.sh early GPIO sanity check
|
|-- main.py
|-- steer_hold.py
|-- pyproject.toml
|-- README.md

------------------------------------------------------------

FILE DESCRIPTIONS

tests/pca60_pulse.py
- Pulses all PCA9685 channels on address 0x60
- Used with a multimeter to confirm motor control is via PCA9685
- Confirms usable PWM frequency (~1000 Hz)

tests/pca60_pwma_find.py
- Identifies the PWM channel for motor A speed
- Result: PWMA = channel 7

tests/pca60_dir_find.py
- Identifies direction pins for both motors
- Results:
  AIN1 = ch 5
  AIN2 = ch 6
  BIN1 = ch 2
  BIN2 = ch 1

tests/throttle_test.py
- Final validated motor test
- Forward ramp
- Stop
- Reverse ramp
- Stop
- Confirms full motor control path works

------------------------------------------------------------

control/motors.py

Unified low-level driver responsible for:
- Initialising both PCA9685 controllers
- Converting throttle values in range [-1.0, 1.0] to:
  - direction pins
  - PWM duty cycle
- Steering control via pulse width in microseconds

This file is the single source of truth for hardware mapping.

------------------------------------------------------------

control/keyboard_drive.py

Keyboard teleoperation.

Controls:
- W / S : throttle forward / reverse
- A / D : steering left / right
- SPACE : immediate stop
- Q : quit

Uses motors.py exclusively.

------------------------------------------------------------

control/estop.py

Emergency stop helper.
Placeholder for:
- watchdog
- WiFi heartbeat
- ROS integration

------------------------------------------------------------

CONTROL MODEL

Throttle:
- range: -1.0 to 1.0
- sign controls direction
- magnitude controls speed
- both motors driven symmetrically

Steering:
- servo pulse width in microseconds
- typical values:
  left   ~1400
  centre ~1700
  right  ~2000

------------------------------------------------------------

NOTES / LESSONS LEARNED

- Motors are not connected to Raspberry Pi GPIO
- All TB6612 pins are driven via PCA9685
- Two independent PCA9685 controllers are present
- Direction pins are driven digitally
- PWM frequency around 1000 Hz works well
- Multimeter-based debugging was essential

------------------------------------------------------------

NEXT STEPS (OPTIONAL)

- ROS2 node
- gamepad / joystick input
- acceleration limiting
- watchdog / failsafe
- wiring schematic

This repository represents a fully reverse-engineered,
reproducible, and working JetRacer motor control setup.
