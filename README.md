# JetRacer Motor Control

Motor control library for JetRacer/Waveshare chassis using Raspberry Pi 4.

Motor control does NOT use Raspberry Pi GPIO directly. All motor and steering signals are driven via I2C using PCA9685 controllers.

---

## Quick Start

```bash
./drive.sh          # Drive with keyboard (WASD)
```

---

## Setup

### 1. Install Raspberry Pi OS

Install a normal Raspberry Pi 64-bit image on your Raspberry Pi 4.

### 2. Enable I2C

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
sudo reboot
```

### 3. Clone and Install

```bash
git clone https://github.com/smagt/jetracer
cd jetracer

# Install dependencies
uv sync

# Activate environment
source .venv/bin/activate
```

### 4. Verify Installation

```bash
# Check I2C devices (should see 0x40 and 0x60)
i2cdetect -y 1

# Verify library (no hardware needed)
python3 verify_library.py
```

---

## Testing

**⚠️ Place robot on blocks before testing!**

```bash
# Quick test (30 seconds)
python3 quick_test.py

# Full test suite (2-3 minutes)
python3 test_motors_manual.py

# Interactive test menu
./run_tests.sh
```

---

## Keyboard Control

Drive your JetRacer with WASD keys:

```bash
./drive.sh
```

### Controls

| Key | Action |
|-----|--------|
| **W/Z** | Throttle up/down (±5% per press) |
| **A/S** | Steer left/right |
| **SPACE** | Emergency stop |
| **Q** | Quit |
| **Ctrl+C** | Emergency stop (anytime) |

### Speed Presets

| Key | Speed | Description |
|-----|-------|-------------|
| **1** | 25% | Slow/Careful (recommended start) |
| **2** | 50% | Medium speed |
| **3** | 75% | Fast |
| **4** | 100% | Full power |
| **0** | 0% | Stop |

**Tip:** Start with key `1` (25%) in new areas, then increase speed when comfortable.

---

## Using the Library

```python
from control import JetRacer
import time

racer = JetRacer()
try:
    # Drive forward at 50%
    racer.set_throttle(0.5)
    racer.set_steering_us(1700)  # Center
    time.sleep(2)
    
    # Stop
    racer.stop()
finally:
    racer.shutdown()
```

### API Quick Reference

```python
racer.set_throttle(speed)        # -1.0 to 1.0
racer.set_steering_us(us)        # 1000-2400 microseconds
racer.set_steering_normalized(v) # -1.0 to 1.0
racer.stop()                     # Emergency stop
racer.shutdown()                 # Clean shutdown
```

**Full API documentation:** [`control/README.md`](control/README.md)

---

## Project Structure

```
jetracer/
├── control/
│   ├── motors.py           # Motor control library
│   ├── keyboard_drive.py   # Keyboard control
│   └── README.md           # Full API documentation
├── tests/                  # Hardware discovery tests
├── quick_test.py           # Quick validation (30s)
├── test_motors_manual.py   # Full test suite (3min)
├── examples.py             # Usage examples
├── verify_library.py       # Pre-hardware verification
├── drive.sh                # Keyboard control launcher
└── run_tests.sh            # Interactive test menu
```

---

## Hardware

### Components
- Raspberry Pi 4
- Two PCA9685 PWM controllers
  - **0x40**: Steering servo
  - **0x60**: DC motor control (via TB6612FNG)
- Waveshare JetRacer chassis

### Motor Pin Mapping

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
- Center: ~1700μs

---

## Troubleshooting

### "No module named 'control'"
```bash
# Make sure you're in the right directory
cd /home/pi/jetracer
source .venv/bin/activate
```

### "Failed to initialize JetRacer"
- Check I2C is enabled: `i2cdetect -y 1`
- Should show devices at 0x40 and 0x60
- Check power supply and connections

### Motors don't move
- Check battery is charged
- Verify motor power supply is connected
- Test with `python3 quick_test.py` first

### Steering doesn't respond
- Check servo power supply
- Verify pulse width range (adjust in `control/motors.py` if needed)

---

## Common Commands

```bash
# Verify setup (no hardware)
python3 verify_library.py

# Test motors (robot on blocks!)
python3 quick_test.py

# Drive with keyboard
./drive.sh

# Test menu
./run_tests.sh

# Check library import
python3 -c "from control import JetRacer; print('OK')"
```

---

## Safety

- Always place robot on blocks for initial testing
- Start with low speed (key `1` = 25%)
- Keep emergency stop ready (SPACE or Ctrl+C)
- Test in safe, open areas
- Check battery level before driving

---

## Development

### Dependencies
- Python 3.13+
- adafruit-blinka
- adafruit-circuitpython-pca9685

### Install for development
```bash
uv sync
source .venv/bin/activate
```

### Run tests
```bash
python3 test_motors_manual.py
```

---

## License

MIT License - Part of the JetRacer project.

See [LICENSE](LICENSE) file for details.
