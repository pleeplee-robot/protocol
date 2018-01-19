[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# PleePlee Robot

![logo](https://github.com/pleeplee-robot/location/blob/master/resources/logo-pleeplee.png)

PleePlee is a proof of concept of a mobile gardener robot.
This repository is about the code for miscellaneous components of the robot.
It contains the code and documentation for:
- the camera
- the LEDs
- the motor driver
- the odometric captors

## Features

The PleePlee robot is able to:
- :seedling: :shower: Water plants.
- :car: Move in a straight line and turn in place.
- :bulb: :satellite: Localize itself in a small area delimited by luminous landmarks.
- :curly_loop: Avoid obstacles.
- :eyes: Log any changes to the garden. (Foreign object or person crossing).

## Protocol

The commucation protocol we designed to ease the communications and
set of instructrions from the rasperry pi to the arduino uno.
