import time
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x60)

# try both: servo-like and motor-like
for freq in (50, 1000):
    pca.frequency = freq
    print(f"\nPulsing PCA9685 @ 0x60, freq={freq}Hz")

    # pulse each channel briefly at a moderate duty
    for ch in range(16):
        print(f"ch {ch}")
        pca.channels[ch].duty_cycle = 0x8000
        time.sleep(0.4)
        pca.channels[ch].duty_cycle = 0
        time.sleep(0.1)

pca.deinit()
print("Done.")
