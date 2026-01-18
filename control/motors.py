"""
JetRacer Motor Control Library

Provides unified control for a JetRacer chassis using:
- Two PCA9685 PWM controllers (I2C addresses 0x40 and 0x60)
- TB6612FNG dual motor driver
- Standard RC servo for steering

Hardware Architecture:
- I2C address 0x40: Steering servo control
- I2C address 0x60: DC motor control via TB6612FNG

Motor Pin Mapping (discovered through testing):
Motor A: PWMA=ch7, AIN1=ch5, AIN2=ch6
Motor B: PWMB=ch0, BIN1=ch2, BIN2=ch1
"""

import board
import busio
import time
from adafruit_pca9685 import PCA9685

# I2C addresses
STEERING_ADDR = 0x40
MOTOR_ADDR    = 0x60

# Frequencies
STEERING_FREQ = 50    # Hz - standard for RC servos
MOTOR_FREQ    = 1000  # Hz - suitable for DC motor control

# Motor mapping (discovered through hardware testing)
PWMA, AIN1, AIN2 = 7, 5, 6  # Motor A channels
PWMB, BIN1, BIN2 = 0, 2, 1  # Motor B channels

# Steering defaults
DEFAULT_STEERING_CENTER = 1700  # microseconds
STEERING_MIN = 1000
STEERING_MAX = 2400


class JetRacer:
    """
    Main control interface for JetRacer robot.
    
    Provides methods for:
    - Throttle control (both motors synchronized)
    - Steering control (servo position)
    - Emergency stop
    - Safe shutdown
    
    Usage:
        racer = JetRacer()
        try:
            racer.set_throttle(0.5)  # 50% forward
            racer.set_steering_us(1700)  # center
            time.sleep(1)
        finally:
            racer.shutdown()
    """
    
    def __init__(self, steering_addr=STEERING_ADDR, motor_addr=MOTOR_ADDR):
        """
        Initialize the JetRacer motor control system.
        
        Args:
            steering_addr: I2C address for steering PCA9685 (default: 0x40)
            motor_addr: I2C address for motor PCA9685 (default: 0x60)
        
        Raises:
            RuntimeError: If I2C communication fails
            ValueError: If PCA9685 controllers not found at specified addresses
        """
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            
            self.steer = PCA9685(i2c, address=steering_addr)
            self.motor = PCA9685(i2c, address=motor_addr)
            
            self.steer.frequency = STEERING_FREQ
            self.motor.frequency = MOTOR_FREQ
            
            # Track current state
            self._current_throttle = 0.0
            self._current_steering_us = DEFAULT_STEERING_CENTER
            
            # Initialize to safe state
            self.stop()
            print(f"JetRacer initialized - Steering: 0x{steering_addr:02x}, Motor: 0x{motor_addr:02x}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize JetRacer: {e}")

    
    def _digital(self, ch, on):
        """
        Set a PCA9685 channel to digital high or low.
        
        Args:
            ch: Channel number (0-15)
            on: True for high (3.3V), False for low (0V)
        """
        self.motor.channels[ch].duty_cycle = 0xFFFF if on else 0

    def _drive_motor(self, pwm, in1, in2, speed):
        """
        Drive a single motor with specified speed and direction.
        
        Args:
            pwm: PWM channel number
            in1: Direction pin 1 channel number
            in2: Direction pin 2 channel number
            speed: Speed value from -1.0 (full reverse) to 1.0 (full forward)
        """
        # Clamp speed to valid range
        speed = max(-1.0, min(1.0, speed))
        
        # Set direction pins
        if speed > 0:
            self._digital(in1, True)
            self._digital(in2, False)
        elif speed < 0:
            self._digital(in1, False)
            self._digital(in2, True)
        else:
            # Brake mode - both low
            self._digital(in1, False)
            self._digital(in2, False)

        # Set PWM duty cycle for speed
        self.motor.channels[pwm].duty_cycle = int(abs(speed) * 65535)

    def set_throttle(self, speed):
        """
        Set throttle for both motors (synchronized drive).
        
        Args:
            speed: Throttle value from -1.0 (full reverse) to 1.0 (full forward)
                   0.0 stops the motors
        
        Example:
            racer.set_throttle(0.5)   # Half speed forward
            racer.set_throttle(-0.3)  # 30% reverse
            racer.set_throttle(0.0)   # Stop
        """
        self._drive_motor(PWMA, AIN1, AIN2, speed)
        self._drive_motor(PWMB, BIN1, BIN2, speed)
        self._current_throttle = speed

    def set_steering_us(self, us):
        """
        Set steering servo position using pulse width in microseconds.
        
        Args:
            us: Pulse width in microseconds (typically 1000-2000)
                Typical values:
                - 1400: Full left
                - 1700: Center
                - 2000: Full right
        
        Note:
            The servo expects a 50Hz PWM signal (20ms period).
            Pulse width determines servo position.
        """
        # Clamp to safe range
        us = max(STEERING_MIN, min(STEERING_MAX, us))
        
        # Convert microseconds to duty cycle
        # 20000 us = 20 ms = full period at 50Hz
        duty = int((us / 20000) * 65535)
        self.steer.channels[0].duty_cycle = duty
        self._current_steering_us = us
    
    def set_steering_normalized(self, value):
        """
        Set steering using normalized value.
        
        Args:
            value: Steering value from -1.0 (full left) to 1.0 (full right)
                   0.0 is center
        """
        # Map -1.0..1.0 to typical servo range
        us = int(DEFAULT_STEERING_CENTER + (value * 300))
        self.set_steering_us(us)
    
    def get_throttle(self):
        """Get current throttle setting."""
        return self._current_throttle
    
    def get_steering_us(self):
        """Get current steering pulse width in microseconds."""
        return self._current_steering_us

    def stop(self):
        """
        Emergency stop - immediately stops all motors.
        Steering position is maintained.
        """
        self.set_throttle(0.0)

    def shutdown(self):
        """
        Safe shutdown - stops motors and releases hardware resources.
        Call this before exiting your program.
        """
        print("Shutting down JetRacer...")
        self.stop()
        self.steer.deinit()
        self.motor.deinit()
        print("JetRacer shutdown complete")
