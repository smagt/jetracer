# JetRacer Control Library - API Reference

Complete API documentation for the JetRacer motor control library.

---

## JetRacer Class

### Initialization

```python
from control import JetRacer

racer = JetRacer()
```

**Parameters:**
- `steering_addr` (int, optional): I2C address for steering controller (default: `0x40`)
- `motor_addr` (int, optional): I2C address for motor controller (default: `0x60`)

**Raises:**
- `RuntimeError`: If I2C communication fails

---

## Methods

### set_throttle(speed)

Set throttle for both motors (synchronized drive).

**Parameters:**
- `speed` (float): Throttle value from -1.0 (full reverse) to 1.0 (full forward)
  - `0.0`: Stop
  - `0.5`: Half speed forward
  - `-0.3`: 30% reverse

Values are automatically clamped to the valid range.

**Example:**
```python
racer.set_throttle(0.5)   # Half speed forward
racer.set_throttle(-0.3)  # 30% reverse
racer.set_throttle(0.0)   # Stop
```

---

### set_steering_us(us)

Set steering servo position using pulse width in microseconds.

**Parameters:**
- `us` (int): Pulse width in microseconds (typically 1000-2400)
  - `1400`: Full left
  - `1700`: Center
  - `2000`: Full right

Values are automatically clamped to safe range (1000-2400).

**Example:**
```python
racer.set_steering_us(1700)  # Center
racer.set_steering_us(1400)  # Left
racer.set_steering_us(2000)  # Right
```

---

### set_steering_normalized(value)

Set steering using normalized value.

**Parameters:**
- `value` (float): Steering value from -1.0 (full left) to 1.0 (full right)
  - `-1.0`: Full left
  - `0.0`: Center
  - `1.0`: Full right

**Example:**
```python
racer.set_steering_normalized(0.0)   # Center
racer.set_steering_normalized(-0.5)  # Slight left
racer.set_steering_normalized(1.0)   # Full right
```

---

### stop()

Emergency stop - immediately stops all motors. Steering position is maintained.

**Example:**
```python
racer.stop()  # Motors stop immediately
```

---

### shutdown()

Safe shutdown - stops motors and releases hardware resources. Always call this before exiting your program.

**Example:**
```python
try:
    racer.set_throttle(0.5)
finally:
    racer.shutdown()  # Always cleanup
```

---

### get_throttle()

Get current throttle setting.

**Returns:** 
- `float`: Current throttle value (-1.0 to 1.0)

**Example:**
```python
current = racer.get_throttle()
print(f"Current throttle: {current}")
```

---

### get_steering_us()

Get current steering pulse width in microseconds.

**Returns:**
- `int`: Current steering position in microseconds

**Example:**
```python
position = racer.get_steering_us()
print(f"Steering: {position}μs")
```

---

## Complete Example

```python
from control import JetRacer
import time

# Initialize
racer = JetRacer()

try:
    # Drive forward with center steering
    racer.set_throttle(0.3)
    racer.set_steering_us(1700)
    time.sleep(2)
    
    # Turn right while moving
    racer.set_steering_normalized(0.5)
    time.sleep(1)
    
    # Stop
    racer.stop()
    
    # Check state
    print(f"Throttle: {racer.get_throttle()}")
    print(f"Steering: {racer.get_steering_us()}μs")
    
except KeyboardInterrupt:
    print("Interrupted!")
finally:
    racer.shutdown()
```

---

## Constants

Available in `control.motors` module:

```python
STEERING_ADDR = 0x40    # I2C address for steering
MOTOR_ADDR = 0x60       # I2C address for motors

STEERING_FREQ = 50      # Hz - standard for RC servos
MOTOR_FREQ = 1000       # Hz - for DC motor control

DEFAULT_STEERING_CENTER = 1700  # Microseconds
STEERING_MIN = 1000             # Minimum pulse width
STEERING_MAX = 2400             # Maximum pulse width
```

---

## Safety Features

- **Automatic clamping**: All values constrained to safe ranges
- **Safe initialization**: Robot starts in stopped state
- **Emergency stop**: `stop()` method for immediate halt
- **Clean shutdown**: `shutdown()` releases all resources
- **Error handling**: Initialization failures are caught and reported

---

## Hardware Details

### Motor Control

Motors are controlled via TB6612FNG dual motor driver:
- **Direction**: Set via digital pins (IN1/IN2)
- **Speed**: Set via PWM duty cycle (0-100%)
- **Brake mode**: Both direction pins low

### Steering Control

Steering uses standard RC servo control:
- **Frequency**: 50Hz (20ms period)
- **Pulse width**: 1000-2400μs typical range
- **Center**: ~1700μs (adjust for your servo)

### Pin Mapping

See main README.md for complete pin mapping details.

---

## Customization

### Adjusting Steering Range

Edit `control/motors.py`:

```python
DEFAULT_STEERING_CENTER = 1700  # Your servo's center
STEERING_MIN = 1000             # Your servo's minimum
STEERING_MAX = 2400             # Your servo's maximum
```

Test different values:
```python
racer.set_steering_us(1600)  # Try different values
```

---

## Error Handling

The library raises exceptions for initialization errors:

```python
try:
    racer = JetRacer()
except RuntimeError as e:
    print(f"Failed to initialize: {e}")
    # Check I2C connections
```

---

## Thread Safety

The library is not thread-safe. If using multiple threads:
- Use locks when accessing the JetRacer object
- Or create separate instances (not recommended)

---

## Performance

- **I2C speed**: Standard 100kHz (sufficient for motor control)
- **Update rate**: Limited by I2C bus speed
- **Latency**: ~1-2ms typical

---

## Best Practices

1. **Always use try/finally**:
   ```python
   racer = JetRacer()
   try:
       # Your code
   finally:
       racer.shutdown()
   ```

2. **Start with low speeds**:
   ```python
   racer.set_throttle(0.2)  # 20% to start
   ```

3. **Check state when needed**:
   ```python
   if racer.get_throttle() > 0.5:
       racer.stop()  # Safety limit
   ```

4. **Handle interrupts**:
   ```python
   try:
       # Your code
   except KeyboardInterrupt:
       print("Stopped by user")
   finally:
       racer.shutdown()
   ```

---

For usage examples, see `examples.py` in the main directory.
