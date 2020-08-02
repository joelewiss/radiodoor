#!/bin/bash

ROOT='/home/joe/radiodoor'
RTL443="$ROOT/rtl_433/build/src/rtl_433"
PYDOOR="$ROOT/pyDoor.py"


$RTL443 -g 35 -f 433910000 -p 0 -X 'n=name,m=FSK_PCM,s=208,l=208,r=212992' -F json | python3 $PYDOOR
