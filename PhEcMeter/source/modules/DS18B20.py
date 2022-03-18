#!/usr/bin/python3
# 参考https://blog.csdn.net/qq_46476163/article/details/116534840
import os
import time
device_file ='/sys/bus/w1/devices/28-3c01f09637ad/w1_slave'

def _read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = _read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = _read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
    return temp_c