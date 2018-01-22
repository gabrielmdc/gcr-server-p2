#!/usr/bin/env bash

# GPIO Control with Raspberry Pi

GPIOPORT=$1

echo $GPIOPORT > /sys/class/gpio/export
echo 'Creating file /sys/class/gpio/gpio'$GPIOPORT'/direction'
echo "out" > /sys/class/gpio/gpio$GPIOPORT/direction