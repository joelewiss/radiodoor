#!/bin/bash

RTL443='/home/pi/RadioDoor/rtl_433/build/src/rtl_433'
PYDOOR='/home/pi/RadioDoor/pyDoor.py'


$RTL443 -g 40 -f 433910000 -p 0 -X 'n=name,m=FSK_PCM,s=208,l=208,r=212992' -F json | python3 $PYDOOR
