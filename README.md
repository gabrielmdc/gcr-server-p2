<img alt="RKAS" title="Gpio Control Relay service" src="resources/images/icon.png" width="100" height="100">

# Gpio Control Relay service

This program allows you to turn on/off a relay connected to a Raspberry Pi.
To communicate with the service, it is necessary a client application like [Android app](https://github.com/nearlg/kodi-relay-remote)
both connected under the same **local net**.

Requirements
==============
- Raspberry Pi or compatible
- A Gnu/Linux system installed (Libreelec OS recomended, if you want to install it in a 
different OS, please check the Gpio path in [the notes](###gpio-path))

Installation
==============

<!-- Just download the [ZIP](https://github.com/nearlg/script.service.relay/archive/master.zip) , and install it using Kodi add-on installer.
-->

Configuration
==============
A client is required to add/modify or delete relays.
Some clients:

Notes
==============
### Socket port
Used by the socket for the comunication with the app.</br>
*By default: 10000*
You can change it from _SOCKET_PORT_ in _/service.py_
### GPIO path
It depends on the system, it has the OPENElec path by default.</br>
*By default: /sys/class/gpio*
You can change it from _GPIO_DIRECTORY_NAME_ in _/lib/repository/gpio.py_