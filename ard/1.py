#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
import numpy as np

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    Gas_val = arduino.readline()
                    if Gas_val != b'':
                        # print("{}".format(Gas_val))
                        print(Gas_val.decode('utf-8').rstrip())
                        
                    else:
                        print("Error NO Detect")
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")