import time, board, busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x60)
pca.frequency = 1000

print("Toggling each channel ON for 1s, then OFF. Ctrl+C to stop.")
try:
    for ch in range(16):
        print("ch", ch)
        pca.channels[ch].duty_cycle = 0xFFFF
        time.sleep(1.0)
        pca.channels[ch].duty_cycle = 0
        time.sleep(0.2)
finally:
    pca.deinit()
