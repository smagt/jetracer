import time, board, busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x60)
pca.frequency = 1000

# keep speed pins off so motors don't jump
for ch in range(16):
    pca.channels[ch].duty_cycle = 0
pca.channels[0].duty_cycle = 0   # PWMB
pca.channels[7].duty_cycle = 0   # PWMA

candidates = [1,2,3,4,5,6,8,9,10,11,12,13,14,15]

print("Pulsing candidates high for 1s each. Watch your TB pin.")
for ch in candidates:
    print(f"ch {ch}")
    pca.channels[ch].duty_cycle = 0xFFFF
    time.sleep(1.0)
    pca.channels[ch].duty_cycle = 0
    time.sleep(0.2)

pca.deinit()
