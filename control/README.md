# JetRacer Control Library

A reusable Python library for controlling JetRacer robots using PCA9685 PWM controllers.

## Overview

This library provides a clean, well-documented interface for controlling:
- **Dual DC motors** (synchronized throttle control)
- **Steering servo** (RC-style PWM control)
- **Emergency stop** functionality
- **Safe shutdown** procedures

## Hardware Requirements

- Raspberry Pi (tested on Pi 4)
- Two PCA9685 PWM controllers:
  - Address 0x40: Steering servo
  - Address 0x60: Motor control (via TB6612FNG driver)
- Waveshare JetRacer chassis (or compatible)

## Installation

From the jetracer project directory:

```bash
# Install dependencies
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```python
from control import JetRacer
import time

# Initialize the robot
racer = JetRacer()

try:
    # Drive forward at 50% speed
    racer.set_throttle(0.5)
    racer.set_steering_us(1700)  # Center steering
    time.sleep(2)
    
    # Stop
    racer.stop()
    
finally:
    # Always cleanup
    racer.shutdown()
```

## API Reference

### JetRacer Class

#### `__init__(steering_addr=0x40, motor_addr=0x60)`
Initialize the motor control system.

**Parameters:**
- `steering_addr`: I2C address for steering controller (default: 0x40)
- `motor_addr`: I2C address for motor controller (default: 0x60)

**Raises:**
- `RuntimeError`: If I2C communication fails

---

#### `set_throttle(speed)`
Set throttle for both motors (synchronized).

**Parameters:**
- `speed` (float): Value from -1.0 (full reverse) to 1.0 (full forward)
  - `0.0`: Stop
  - `0.5`: Half speed forward
  - `-0.3`: 30% reverse

Values are automatically clamped to the valid range.

---

#### `set_steering_us(us)`
Set steering position using pulse width.

**Parameters:**
- `us` (int): Pulse width in microseconds (1000-2400)
  - `1400`: Full left
  - `1700`: Center
  - `2000`: Full right

---

#### `set_steering_normalized(value)`
Set steering using normalized value.

**Parameters:**
- `value` (float): Steering value from -1.0 (left) to 1.0 (right)

---

#### `stop()`
Emergency stop - immediately stops all motors. Steering position is maintained.

---

#### `shutdown()`
Safe shutdown - stops motors and releases hardware resources. Always call before program exit.

---

#### `get_throttle()` / `get_steering_us()`
Get current throttle or steering values.

## Testing

### Comprehensive Test Suite

Run the full test suite to validate all functionality:

```bash
cd /home/pi/jetracer
python3 test_motors_manual.py
```

**Tests include:**
1. Initialization check
2. Steering sweep
3. Normalized steering
4. Forward throttle ramp
5. Reverse throttle ramp
6. Combined steering + throttle
7. State verification
8. Safety limits

⚠️ **SAFETY**: Place robot on blocks before running tests!

### Quick Test

For rapid validation:

```bash
python3 quick_test.py
```

This runs a minimal test sequence (30 seconds).

## Safety Features

- Automatic value clamping (throttle: ±1.0, steering: 1000-2400μs)
- Emergency stop method
- Safe initialization (starts stopped)
- Graceful shutdown with resource cleanup
- Brake mode when throttle = 0

## Example Programs

See the `control/` directory for examples:
- `keyboard_drive.py`: WASD keyboard control
- `estop.py`: Emergency stop utilities

## Hardware Details

### Motor Pin Mapping

Discovered through hardware testing:

**Motor A:**
- PWMA: PCA9685 channel 7
- AIN1: PCA9685 channel 5
- AIN2: PCA9685 channel 6

**Motor B:**
- PWMB: PCA9685 channel 0
- BIN1: PCA9685 channel 2
- BIN2: PCA9685 channel 1

**Steering:**
- PCA9685 address 0x40, channel 0
- 50Hz PWM frequency
- Center: ~1700μs

### PWM Frequencies

- Steering: 50Hz (standard RC servo)
- Motors: 1000Hz (suitable for DC motor control)

## Troubleshooting

**Problem**: "Failed to initialize JetRacer"
- Check I2C connections
- Verify PCA9685 addresses with `i2cdetect -y 1`
- Ensure power supply is adequate

**Problem**: Motors don't move
- Check TB6612FNG STBY pin (should be high)
- Verify motor power supply
- Check motor wiring

**Problem**: Erratic steering
- Check servo power supply
- Verify 50Hz frequency setting
- Adjust pulse width range for your servo

## License

Part of the JetRacer project.

## Contributing

When modifying the library:
1. Update docstrings
2. Run test suite
3. Update this README if API changes
4. Test on actual hardware
