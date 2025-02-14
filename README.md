# legControl

This is the submodule for controlling the quadrupedal system in our capstone project.

<b>This module is still a work in progress.</b>

<b>Note</b> the current version of this code is untested. As of now, 
only motor angles can be set and interpolated between. The next version of this
code will use inverse kinematics to control the leg, so the motor interpolation aspect of this
code will be removed.

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

## Nomenclature of leg components and coordinate system
This is the naming scheme used for each component in the leg design, along with location
of the coordinate origin, which the end-effector is referenced to.

<br><br>
Noah Stieler, 2025