# Keyboard Control for JetRacer

## Quick Start

Yes! You can now use keyboard control to drive your JetRacer.

### To run keyboard control:

```bash
cd /home/pi/jetracer
source .venv/bin/activate
python3 control/keyboard_drive.py
```

Or use the convenient launcher:

```bash
cd /home/pi/jetracer
./drive.sh
```

## Controls

```
╔═══════════════════════════════════════════════════════╗
║  Key     Action                                      ║
╠═══════════════════════════════════════════════════════╣
║  W       Increase throttle (+5% per press)           ║
║  S       Decrease throttle (-5% per press)           ║
║  A       Steer left                                  ║
║  D       Steer right                                 ║
║  SPACE   Emergency stop (throttle to 0, center)     ║
║  Q       Quit                                        ║
║  Ctrl+C  Emergency stop (anytime)                   ║
╚═══════════════════════════════════════════════════════╝
```

## Features

- **Incremental throttle**: Press W/S to gradually increase/decrease speed
- **Safety limits**: Max speed capped at ±50% (adjustable in code)
- **Live feedback**: See current throttle and steering on screen
- **Emergency stop**: Press SPACE or Ctrl+C anytime
- **Safe shutdown**: Always stops motors and cleans up properly

## Safety Notes

⚠️ **Before starting:**
1. Ensure robot is in a safe, open area
2. Clear obstacles from the path
3. Be ready to press SPACE or Ctrl+C for emergency stop
4. Start with small throttle adjustments (W/S)

⚠️ **While driving:**
- Start slow - build up speed gradually
- Test steering response at low speed first
- Keep line of sight to the robot
- Be prepared to emergency stop

## How It Works

The keyboard control uses the JetRacer library:

```python
from control import JetRacer

car = JetRacer()
car.set_throttle(0.3)       # 30% forward
car.set_steering_us(1700)   # Center
car.shutdown()              # Always cleanup
```

## Customization

You can adjust the behavior by editing `control/keyboard_drive.py`:

### Adjust steering range:
```python
STEER_CENTER = 1700  # Center position (microseconds)
STEER_LEFT   = 1400  # Full left
STEER_RIGHT  = 2000  # Full right
```

### Adjust speed limits:
```python
# Line 49, 51: Change 0.5 to adjust max speed
speed = min(speed + 0.05, 0.5)  # Max 50% forward
speed = max(speed - 0.05, -0.5) # Max 50% reverse
```

### Adjust throttle increment:
```python
# Line 49, 51: Change 0.05 to adjust step size
speed = min(speed + 0.05, 0.5)  # 5% per W press
speed = max(speed - 0.05, -0.5) # 5% per S press
```

## Troubleshooting

### Issue: "No module named 'control'"
**Solution**: Make sure you're in the correct directory and virtual environment is activated:
```bash
cd /home/pi/jetracer
source .venv/bin/activate
python3 control/keyboard_drive.py
```

### Issue: Keys not responding
**Possible causes**:
- Terminal not in focus
- Running over SSH without proper terminal
- Keyboard layout issue

**Solution**: Run from local terminal (not SSH) or use a proper SSH client

### Issue: Robot doesn't move
**Check**:
1. Battery is charged
2. Motors are connected
3. Test with `python3 quick_test.py` first
4. Try increasing throttle more (press W multiple times)

### Issue: Can't stop with SPACE
**Workaround**: Press Ctrl+C for emergency stop (always works)

## Before First Use

**IMPORTANT**: Test the motors first before driving!

```bash
# 1. Verify library works (no hardware)
python3 verify_library.py

# 2. Test with robot on blocks
python3 quick_test.py

# 3. Once tests pass, you can drive
python3 control/keyboard_drive.py
```

## Using with SSH

If connecting over SSH, make sure you have a proper terminal:

```bash
# From your computer:
ssh -t pi@your-robot-ip

# On the robot:
cd /home/pi/jetracer
source .venv/bin/activate
python3 control/keyboard_drive.py
```

The `-t` flag ensures proper terminal emulation for keyboard input.

## Tips for Smooth Driving

1. **Start slow**: Press W 2-3 times to start moving slowly
2. **Test steering**: At low speed, test A and D to see steering response
3. **Emergency stop ready**: Keep finger near SPACE bar
4. **Smooth inputs**: Avoid rapid key presses
5. **Center steering**: Press SPACE to both stop and center steering
6. **Build confidence**: Start in a small safe area before open space

## Example Drive Session

```
1. Start the program:
   ./drive.sh

2. Press W twice (10% throttle)
   → Robot starts moving slowly forward

3. Press A to steer left
   → Robot turns left

4. Press SPACE
   → Robot stops, steering centers

5. Press Q
   → Program exits safely
```

## Alternative: Run Directly

You can also run it directly without the launcher:

```bash
cd /home/pi/jetracer
source .venv/bin/activate
python3 control/keyboard_drive.py
```

## Next Steps

After you're comfortable with keyboard control:

- Try modifying the controls
- Add new features (cruise control, speed presets, etc.)
- Integrate with sensors
- Add autonomous modes

See `examples.py` for more ways to use the JetRacer library.
