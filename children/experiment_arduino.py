import numpy as np
import logging
import random
import serial
import json
import time
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

def f_set(X):
    """
    Set spectra first then brightness
    """
    
    if X!=None or X!="":    
        s = serial.Serial("/dev/ttyACM0",9600)
        s.write("manual_connect\r\n".encode("ascii"))
        s.write("set(brilho,100)\r\n".encode("ascii"))
        with open("../data/spectra/parameters.json") as f:
            param = json.load(f)
            param = sorted(param.items(), key= lambda x: x[0])

            for p,x in zip(param, X):
                time.sleep(2)
                string = f"set({p[0]},{int(100*x)})\r\n" 
                print(string)
               s.write(string.encode("ascii"))
        s.close()
    return 0

def f_read():
    """
    Read info from Arduino
    """
    s = serial.Serial("/dev/ttyACM0", 9600)
    s.write("log\r\n".encode("ascii"))#Change log by the actual read command
    y = s.readline().decode("ascii").strip("\n").strip("\r")
    y = y.split(" ")
    s.close()
    return y

def f_command(c):
    """
    Sends command to Arduino
    """
    s = serial.Serial("/dev/ttyACM0", 9600)
    s.write(f"{c}\r\n".encode("ascii"))
    s.close()
