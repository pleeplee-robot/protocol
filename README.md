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

The used protocol is quite basic and as follow:
A client is identified both by its socket (identity to the server) and a public name (set through a setname packet).
Packets are composed of three parts, separated by slashes:
- `type`, that identifies which handler should handle the packet (for instance, setname or sendToSerial)
- `ID`, which could be use if bidirectionnal communication must occur to identify which packet a response is related to. Implementation for such a followup system should be implemented by an higher layer protocol.
- the message (which can contain slashes) accompanying the packet.Provided types are as follow:
- `setname` (sets the name of the client to the content of the message)
- `sendserial` (sends the message to the serial)
- `send` (message is dst:msg. Sends msg to the client identified by dst)
- `release` (message is the name of the module) release possession of the module whose name is the message. Messages from this device will not be received anymore Responded with OK or an error message.
- `take` (message is priority:name with priority a number and name the name of the module to tke ownership of). Responded with OK or an error. If OK, messages from this Arduino module will be forwarded to the client with type "from name".
