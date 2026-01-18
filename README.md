# Jetracer software

Initially, the following needs to be run:
```
sudo raspi-config nonint do_i2c 0
```

## Overview

This repository contains low-level bring-up and test scripts for a JetRacer / Waveshare car chassis using a Raspberry Pi 4 and TB6612FNG motor driver, where:
	•	Steering is controlled via a PCA9685 at 0x40
	•	Throttle (DC motors) is controlled via a second PCA9685 at 0x60
	•	Motors are driven through a TB6612FNG (not directly via GPIO)

The scripts below were created to identify hardware mappings and then validate motor control.


## File descriptions

### pca60_pulse.py

Purpose:
Discovery script to determine whether the I2C device at address 0x60 is a PCA9685 and whether it drives the motor controller.

What it does:
	•	Connects to PCA9685 at 0x60
	•	Pulses all 16 channels at two different frequencies (50 Hz and 1000 Hz)
	•	Allows probing of TB6612FNG pins with a multimeter to detect activity

Used to discover:
	•	That motor PWM signals come from PCA9685 at 0x60
	•	Approximate channel numbers for PWMA / PWMB


### pca60_pwma_find.py

Purpose:
Identify the exact PCA9685 channel connected to PWMA (motor A speed).

What it does:
	•	Pulses channels 5–8 individually
	•	Allows monitoring of TB6612FNG pin 23 (PWMA)

Result:
	•	PWMA = channel 7


### pca60_pwmb_find.py

Purpose:
Identify the exact PCA9685 channel connected to PWMB (motor B speed).

What it does:
	•	Pulses all 16 channels briefly
	•	Allows monitoring of TB6612FNG pin 15 (PWMB)

Result:
	•	PWMB = channel 0


### pca60_dir_find.py

Purpose:
Identify which PCA9685 channels drive the direction pins of the TB6612FNG.

What it does:
	•	Turns each PCA9685 channel fully on (digital high) one at a time
	•	Allows probing of TB6612FNG direction pins

Used to map:
	•	AIN1 (pin 21) → channel 5
	•	AIN2 (pin 22) → channel 6
	•	BIN1 (pin 17) → channel 2
	•	BIN2 (pin 16) → channel 1


### throttle_test.py

Purpose:
Final validated motor control test for both rear motors.

What it does:
	•	Uses PCA9685 at 0x60
	•	Correctly sets:
	•	direction pins (AIN/BIN)
	•	PWM speed pins (PWMA/PWMB)
	•	Performs:
	•	forward ramp
	•	stop
	•	reverse ramp
	•	stop

Motor mapping used:

Motor A:
	•	PWMA = ch 7
	•	AIN1 = ch 5
	•	AIN2 = ch 6

Motor B:
	•	PWMB = ch 0
	•	BIN1 = ch 2
	•	BIN2 = ch 1

Expected behaviour:
	•	Both motors spin forward
	•	Stop cleanly
	•	Reverse
	•	Stop

This script confirms the entire motor power and control path is correct.


### Notes / lessons learned
	•	The Waveshare JetRacer board uses two PCA9685 chips
	•	0x40: steering servo
	•	0x60: motor control
	•	TB6612FNG STBY must be high (it is, on this board)
	•	Motor PWM is not on Raspberry Pi GPIO
	•	Direction pins are driven as digital signals via PCA9685 channels
	•	High PWM frequency (~1000 Hz) works well for motor speed control

