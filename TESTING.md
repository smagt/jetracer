# Testing the JetRacer Motor Library

This directory contains a comprehensive test suite for the JetRacer motor control library.

## Quick Start

**⚠️ SAFETY FIRST: Place robot on blocks before testing!**

### Option 1: Interactive Menu (Recommended)

```bash
cd /home/pi/jetracer
./run_tests.sh
```

This launches an interactive menu with all testing options.

### Option 2: Direct Test Execution

```bash
cd /home/pi/jetracer
source .venv/bin/activate

# Quick validation (30 seconds)
python3 quick_test.py

# Full test suite (2-3 minutes)
python3 test_motors_manual.py

# Usage examples
python3 examples.py
```

## Available Test Scripts

### 1. `quick_test.py` - Fast Validation

**Purpose**: Quickly verify basic functionality
**Duration**: ~30 seconds
**Tests**:
- Initialization
- Steering center position
- Forward motion (20%)
- Reverse motion (20%)
- Shutdown

**When to use**: After hardware changes, library updates, or as a sanity check

```bash
python3 quick_test.py
```

### 2. `test_motors_manual.py` - Comprehensive Suite

**Purpose**: Thorough validation of all features
**Duration**: ~2-3 minutes
**Tests**:
1. Initialization check
2. Steering sweep (microsecond control)
3. Normalized steering (-1.0 to 1.0)
4. Forward throttle ramp (0% to 30%)
5. Reverse throttle ramp (0% to -30%)
6. Combined steering + throttle
7. State verification (getters)
8. Safety limits and clamping

**When to use**: First-time hardware validation, after major changes, or debugging

```bash
python3 test_motors_manual.py
```

### 3. `examples.py` - Usage Demonstrations

**Purpose**: Show common usage patterns
**Duration**: Variable (interactive)
**Examples**:
1. Basic movement (forward/reverse)
2. Steering control (both methods)
3. Combined steering + throttle
4. State tracking (reading values)
5. Safety features
6. Custom control loops

**When to use**: Learning the API, reference for your own code

```bash
python3 examples.py
```

### 4. `run_tests.sh` - Interactive Menu

**Purpose**: Convenient access to all tests
**Features**:
- Interactive menu
- Library structure check
- File listing
- Virtual environment activation

```bash
./run_tests.sh
```

## Test Output Examples

### Successful Quick Test
```
[1/5] Initializing...
JetRacer initialized - Steering: 0x40, Motor: 0x60
[2/5] Testing steering center...
[3/5] Testing forward (20%)...
[4/5] Testing reverse (20%)...
[5/5] Shutting down...

✓ Quick test passed!
  - Initialization: OK
  - Steering: OK
  - Forward: OK
  - Reverse: OK
```

### Successful Full Test
```
════════════════════════════════════════════════════════
  TEST 1: Initialization
════════════════════════════════════════════════════════
  → Status: ✓ JetRacer initialized successfully

[... more tests ...]

════════════════════════════════════════════════════════
  ALL TESTS COMPLETE
════════════════════════════════════════════════════════

    ✓ Initialization
    ✓ Steering sweep
    ✓ Forward throttle
    ✓ Reverse throttle
    [... etc ...]
```

## Interpreting Results

### Success Indicators
- ✓ checkmarks for passed tests
- "OK" status messages
- Clean shutdown message
- No error tracebacks

### Failure Indicators
- ✗ marks or error messages
- Python tracebacks
- "Failed" status messages
- Unexpected behavior (motors not moving, etc.)

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'board'"
**Solution**: Activate the virtual environment first
```bash
source .venv/bin/activate
```

### Issue: "Failed to initialize JetRacer"
**Possible causes**:
- I2C not enabled (check `raspi-config`)
- PCA9685 controllers not connected
- Wrong I2C addresses
- Power supply issues

**Debug steps**:
```bash
# Check if I2C devices are detected
i2cdetect -y 1

# Should show devices at 0x40 and 0x60
```

### Issue: Motors don't move during test
**Possible causes**:
- Motor power supply not connected
- TB6612FNG STBY pin issue
- Motor connections loose
- Battery discharged

### Issue: Steering doesn't respond
**Possible causes**:
- Servo power supply issue
- Wrong pulse width range for your servo
- Servo connection loose

## Safety Notes

### Before Testing
1. ✅ Place robot on blocks (wheels off ground)
2. ✅ Check all connections
3. ✅ Verify power supply
4. ✅ Keep hands clear of moving parts
5. ✅ Have Ctrl+C ready for emergency stop

### During Testing
- Watch for unexpected behavior
- Listen for unusual motor sounds
- Monitor for overheating
- Stop immediately if something seems wrong

### After Testing
- Tests automatically shutdown safely
- Motors will be stopped
- Hardware resources released
- Safe to disconnect power

## Emergency Stop

Press **Ctrl+C** at any time during testing:
- All scripts handle KeyboardInterrupt
- Motors will be stopped
- Clean shutdown performed
- Safe to restart tests

## Calibration

If steering or motors behave incorrectly, you may need to adjust constants in `control/motors.py`:

```python
# Steering defaults
DEFAULT_STEERING_CENTER = 1700  # Adjust for your servo
STEERING_MIN = 1000             # Minimum pulse width
STEERING_MAX = 2400             # Maximum pulse width
```

Test different values with:
```python
racer.set_steering_us(1600)  # Try different values
```

## Next Steps After Testing

Once all tests pass:

1. **Integrate into your application**:
   ```python
   from control import JetRacer
   
   racer = JetRacer()
   try:
       # Your code here
       racer.set_throttle(0.5)
   finally:
       racer.shutdown()
   ```

2. **Explore examples**: See `examples.py` for patterns

3. **Read API docs**: See `control/README.md` for complete reference

4. **Build your application**: Use keyboard_drive.py as inspiration

## Documentation

- **API Reference**: `control/README.md`
- **Library Summary**: `LIBRARY_SUMMARY.md`
- **Hardware Details**: Main `README.md`
- **Usage Examples**: `examples.py`

## Questions or Issues?

If tests fail or you encounter problems:

1. Check this testing guide
2. Review `control/README.md` troubleshooting section
3. Verify hardware connections
4. Check power supply
5. Run `i2cdetect -y 1` to verify I2C devices

## Test Development

To add your own tests:

1. Use existing test scripts as templates
2. Follow the safety patterns (try/finally, shutdown)
3. Include clear output messages
4. Handle KeyboardInterrupt for emergency stop
5. Test on actual hardware before committing

Example template:
```python
from control import JetRacer
import time

def my_test():
    racer = JetRacer()
    try:
        # Your test code
        racer.set_throttle(0.3)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted!")
    finally:
        racer.shutdown()

if __name__ == "__main__":
    my_test()
```
