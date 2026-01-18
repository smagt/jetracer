import time
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x60)
pca.frequency = 1000

for ch in (5, 6, 7, 8):
    print(f"Pulse ch {ch}")
    pca.channels[ch].duty_cycle = 0x9000
    time.sleep(1.0)
    pca.channels[ch].duty_cycle = 0
    time.sleep(0.5)

pca.deinit()
