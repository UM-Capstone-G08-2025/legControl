# legControl

This is the submodule for controlling the quadrupedal system in our capstone project.

## Hardware used
PCA9685 servo driver board<br>
12 servo motors, 3 for each leg<br>
Raspberry Pi

## Wiring the servo driver board
<b>VCC</b> - connects to the 3V3 pin on the Pi<br>
<b>GND</b> - connects to the GND pin on the Pi<br>
<b>SDA</b> and <b>SCL</b> - This is for I2C. The Pi automatically configures pins for it,
so check the pinout of the specific model you are using.

## Software configuration
The following guide was used to setup the Raspberry Pi with the servo driver board:<br>
https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi

I2C must be enabled, go to:<br>
&emsp; Start Menu -> Preferences -> Raspberry Pi Configuration -> Interfaces<br>
&emsp; turn on I2C, click OK

The following library must be installed, this can be done with requirements.txt or by using pip install directly:<br>
&emsp; adafruit-circuitpython-servokit<br><br>
&emsp; I did this by creating a Python virtual environment (Raspberry Pi gives an error otherwise). I followed this Stack Overflow post:<br>
&emsp; https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3

<br><br>
Noah Stieler, 2025
