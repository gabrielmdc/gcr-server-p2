<img alt="Gpio Control Relay" title="Gpio Control Relay service" src="resources/images/icon.png" width="100" height="100">

# Gpio Control Relay service
This program allows you to turn on/off a relay connected to a Raspberry Pi by a gpio port.
To configure and communicate with the service and use the relays, 
it is necessary a client program. Here is a [list of clients](#clients).

## Requirements
- Raspberry Pi or compatible
- A Gnu/Linux system installed ([LibreELEC OS](https://libreelec.tv/)
 recommended, if you want to install this in a 
different OS, please check the Gpio path in [the notes](#gpio-path))
    - Python 2.7

## Run
Just download the [ZIP](https://github.com/nearlg/script.service.relay/archive/master.zip), 
and run _/service.py_:

```bash
python service.py
```

## Configuration
It is necessary a client to add relays and configure their gpio ports.

## Clients
<!--
TODO
-->

## Notes
### Socket port
Used by the socket for the communication with the app.</br>
*By default: 10000*
You can change it from _SOCKET_PORT_ in _/service.py_
### GPIO path
It depends on the system, it has the LibreELEC path by default.</br>
*By default: /sys/class/gpio*
You can change it from _GPIO_DIRECTORY_NAME_ in _/lib/repository/gpio.py_
