import time
import board
import busio
from adafruit_pca9685 import PCA9685

# PCA controlling motors
ADDR = 0x60
FREQ = 1000

# Motor A mapping
PWMA = 7
AIN1 = 5
AIN2 = 6

# Motor B mapping
PWMB = 0
BIN1 = 2
BIN2 = 1

def set_digital(ch, on: bool):
    pca.channels[ch].duty_cycle = 0xFFFF if on else 0

def set_motor(a_speed: float, b_speed: float):
    """
    speed in [-1.0, 1.0]
    sign = direction, magnitude = PWM duty
    """
    def drive(pwm_ch, in1_ch, in2_ch, speed):
        speed = max(-1.0, min(1.0, speed))
        if speed > 0:
            set_digital(in1_ch, True)
            set_digital(in2_ch, False)
        elif speed < 0:
            set_digital(in1_ch, False)
            set_digital(in2_ch, True)
        else:
            # coast (both low). For brake, set both high.
            set_digital(in1_ch, False)
            set_digital(in2_ch, False)

        duty = int(abs(speed) * 65535)
        pca.channels[pwm_ch].duty_cycle = duty

    drive(PWMA, AIN1, AIN2, a_speed)
    drive(PWMB, BIN1, BIN2, b_speed)

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=ADDR)
pca.frequency = FREQ

# Ensure everything off initially
for ch in range(16):
    pca.channels[ch].duty_cycle = 0

print("Forward ramp...")
for s in [0.10, 0.15, 0.20, 0.25]:
    set_motor(s, s)
    time.sleep(1.0)

print("Stop...")
set_motor(0.0, 0.0)
time.sleep(1.5)

print("Reverse ramp...")
for s in [-0.10, -0.15, -0.20]:
    set_motor(s, s)
    time.sleep(1.0)

print("Stop...")
set_motor(0.0, 0.0)
time.sleep(0.5)

pca.deinit()
print("Done.")
