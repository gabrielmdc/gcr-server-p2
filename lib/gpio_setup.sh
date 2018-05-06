#!/usr/bin/env bash

# GPIO Control with Raspberry Pi

GPIOPORT=$1
GPIOSTATE=$2

if [ ! -d "/sys/class/gpio/gpio$GPIOPORT" ]; then
    echo $GPIOPORT > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio$GPIOPORT/direction
    echo "$GPIOSTATE" > /sys/class/gpio/gpio$GPIOPORT/value
fi