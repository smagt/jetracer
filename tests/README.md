# JetRacer Hardware Discovery Tests

This directory contains the hardware discovery and testing scripts used to reverse-engineer the JetRacer motor control system.

These tests were used to identify the correct PCA9685 channels and pin mappings for the TB6612FNG motor driver and steering servo.

---

## Overview

The JetRacer motor control does NOT use Raspberry Pi GPIO directly. Instead, it uses two PCA9685 PWM controllers:
- **0x40**: Steering servo control
- **0x60**: Motor control (via TB6612FNG dual motor driver)

These tests document the discovery process and can be used for troubleshooting or verifying hardware connections.

---

## Test Files

### Motor Discovery Tests (PCA9685 @ 0x60)

#### `pca60_pulse.py`
**Purpose:** Initial hardware discovery - pulse all 16 channels on PCA9685 at 0x60

**What it does:**
- Tests both 50Hz (servo) and 1000Hz (motor) frequencies
- Pulses each channel for 0.4 seconds
- Used to confirm motor control is via PCA9685, not GPIO

**When to use:**
- Initial hardware verification
- Confirm PCA9685 at 0x60 is connected
- Find which channels are connected to motor driver

**Usage:**
```bash
cd tests
python3 pca60_pulse.py
# Watch motor driver pins with multimeter
```

---

#### `pca60_pwma_find.py`
**Purpose:** Find the PWM channel for Motor A speed control

**What it does:**
- Pulses channels 5, 6, 7, 8 individually
- Each channel pulses for 1 second at ~56% duty cycle
- Used with multimeter on TB6612FNG PWMA pin

**Result:** Found PWMA = channel 7

**Usage:**
```bash
python3 pca60_pwma_find.py
# Watch TB6612FNG pin 23 (PWMA) with multimeter
```

---

#### `pca60_dir_find.py`
**Purpose:** Find direction pins (AIN1, AIN2, BIN1, BIN2) for both motors

**What it does:**
- Keeps PWM channels off for safety
- Pulses each candidate channel high for 1 second
- Used with multimeter on TB6612FNG direction pins

**Results found:**
- AIN1 = channel 5
- AIN2 = channel 6
- BIN1 = channel 2
- BIN2 = channel 1
- PWMB = channel 0

**Usage:**
```bash
python3 pca60_dir_find.py
# Watch TB6612FNG pins 21,22 (AIN1/2) and 17,16 (BIN1/2)
```

---

#### `pca60_dir_scan.py`
**Purpose:** Systematic scan of all 16 PCA9685 channels

**What it does:**
- Toggles each channel high for 1 second
- Comprehensive scan to map all connections
- Used for initial hardware exploration

**Usage:**
```bash
python3 pca60_dir_scan.py
# Monitor all TB6612FNG pins with multimeter
```

---

#### `throttle_test.py`
**Purpose:** Final validation test using discovered pin mappings

**What it does:**
- Forward ramp: 10%, 15%, 20%, 25%
- Stop
- Reverse ramp: -10%, -15%, -20%
- Stop

**This test confirms:**
- Motor A mapping: PWMA=7, AIN1=5, AIN2=6
- Motor B mapping: PWMB=0, BIN1=2, BIN2=1
- Direction control works correctly
- Both motors run synchronously

**⚠️ Place robot on blocks!**

**Usage:**
```bash
python3 throttle_test.py
# Watch wheels - should move forward, stop, reverse, stop
```

---

### Steering Discovery Tests (PCA9685 @ 0x40)

#### `steer_hold.py`
**Purpose:** Interactive steering servo calibration tool

**What it does:**
- Allows manual adjustment of servo position
- Commands: `+`/`-` (±50μs), `++`/`--` (±10μs), or enter value directly
- Calibrates left, right, and center positions
- Holds center position after calibration

**Interactive commands:**
```
+      Add 50μs
-      Subtract 50μs
++     Add 10μs
--     Subtract 10μs
1700   Set exact value
ok     Confirm and move to next position
```

**Results found:**
- Left: ~1400μs
- Right: ~2000μs  
- Center: ~1700μs
- PCA9685 address: 0x40
- Channel: 0

**Usage:**
```bash
python3 steer_hold.py
# Follow prompts to calibrate left, right positions
# Script calculates center and holds it
```

---

### GPIO Discovery Tests

#### `gpio_pulse_scan.sh`
**Purpose:** Early test to check if motors are controlled via Raspberry Pi GPIO

**What it does:**
- Pulses common GPIO pins (4, 5, 6, 12, 13, 16-27)
- Each pin goes high for 1 second
- Requires `libgpiod-dev` and `gpiod` tools

**Result:** No motor response - confirmed motors are NOT controlled via GPIO

**Usage:**
```bash
sudo apt install gpiod
./gpio_pulse_scan.sh
# Press Enter at each prompt to pulse next GPIO
```

---

## Hardware Architecture Discovery Summary

### What These Tests Revealed

**Two PCA9685 Controllers:**
```
0x40 → Steering Servo (channel 0, 50Hz)
0x60 → Motor Control via TB6612FNG (1000Hz)
```

**Motor A (discovered via pca60_pwma_find.py + pca60_dir_find.py):**
```
PWMA (TB6612 pin 23) → PCA9685 channel 7
AIN1 (TB6612 pin 21) → PCA9685 channel 5
AIN2 (TB6612 pin 22) → PCA9685 channel 6
```

**Motor B (discovered via pca60_dir_find.py):**
```
PWMB (TB6612 pin 15) → PCA9685 channel 0
BIN1 (TB6612 pin 17) → PCA9685 channel 2
BIN2 (TB6612 pin 16) → PCA9685 channel 1
```

**Steering (discovered via steer_hold.py):**
```
PCA9685 address 0x40, channel 0
Frequency: 50Hz (standard RC servo)
Center: ~1700μs
```

**Key Findings:**
- ✅ Motors controlled via PCA9685, NOT GPIO
- ✅ Two separate PCA9685 controllers
- ✅ TB6612FNG STBY pin tied high (always enabled)
- ✅ 1000Hz PWM frequency works well for motors
- ✅ Direction pins driven digitally (0x0000 or 0xFFFF)

---

## Discovery Process Timeline

1. **gpio_pulse_scan.sh** - Ruled out GPIO control
2. **pca60_pulse.py** - Confirmed PCA9685 @ 0x60 controls motors
3. **pca60_dir_scan.py** - Mapped all 16 channels
4. **pca60_pwma_find.py** - Found PWMA = channel 7
5. **pca60_dir_find.py** - Found all direction pins
6. **throttle_test.py** - Validated complete motor control
7. **steer_hold.py** - Calibrated steering servo

---

## Running Tests

### Prerequisites
```bash
# Make sure you're in virtual environment
source ../.venv/bin/activate

# Or install dependencies
cd ..
uv sync
```

### Safety
⚠️ **Always place robot on blocks before running motor tests!**

### Example Session
```bash
cd tests

# 1. Verify PCA9685 @ 0x60 responds
python3 pca60_pulse.py

# 2. Test motor control with discovered mappings
python3 throttle_test.py

# 3. Calibrate steering
python3 steer_hold.py
```

---

## Troubleshooting

### "No module named 'board'"
```bash
cd ..
source .venv/bin/activate
cd tests
```

### "Failed to initialize I2C"
```bash
# Check I2C is enabled
sudo raspi-config
# Interface Options → I2C → Enable

# Check devices are detected
i2cdetect -y 1
# Should show 0x40 and 0x60
```

### "Motors don't move in throttle_test.py"
- Check battery is charged
- Verify motor power supply connected
- Check TB6612FNG STBY pin is high
- Verify motor wiring

### "Steering doesn't respond in steer_hold.py"
- Check servo power supply
- Verify PCA9685 at 0x40 is detected
- Try different pulse width values

---

## For New Hardware

If you have similar hardware and need to discover pin mappings:

1. **Start with `pca60_pulse.py`**
   - Confirm PCA9685 responds
   - Note which frequency works (50Hz vs 1000Hz)

2. **Use `pca60_dir_scan.py`**
   - Map all channels with multimeter
   - Note which pins show voltage changes

3. **Find PWM channels**
   - For each motor, pulse suspected PWM pins
   - Use `pca60_pwma_find.py` as template

4. **Find direction pins**
   - Use `pca60_dir_find.py` with PWM off
   - Map AIN1/2, BIN1/2 pins

5. **Validate with test**
   - Create test similar to `throttle_test.py`
   - Verify forward/reverse work correctly

6. **Calibrate steering**
   - Use `steer_hold.py` for servo
   - Find left, right, center positions

---

## Using Discovered Values

The final pin mappings from these tests are used in the main library:

```python
# From control/motors.py
PWMA, AIN1, AIN2 = 7, 5, 6  # Motor A
PWMB, BIN1, BIN2 = 0, 2, 1  # Motor B

STEERING_ADDR = 0x40
MOTOR_ADDR = 0x60

STEERING_FREQ = 50
MOTOR_FREQ = 1000

DEFAULT_STEERING_CENTER = 1700
```

---

## Notes

- These are one-time discovery tests, not needed for normal operation
- Use the main library (`control/motors.py`) for actual robot control
- Keep these tests for reference and hardware troubleshooting
- The TB6612FNG has STBY tied high (cannot be controlled via software)

---

## Tools Used

**Hardware:**
- Multimeter (essential for tracing pins)
- Oscilloscope (optional, helpful for frequency verification)

**Software:**
- `i2cdetect` - Detect I2C devices
- `gpiod` tools - Test GPIO pins
- Python with Adafruit libraries

---

## References

- TB6612FNG Datasheet
- PCA9685 Datasheet  
- Adafruit CircuitPython PCA9685 library documentation
- Raspberry Pi GPIO pinout

---

For using the finalized motor control system, see the main [README.md](../README.md).
