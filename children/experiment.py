import numpy as np
import logging
import random
import serial
import json
import time
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

path = "/dev/ttyUSB0"
timeout = 10

def f_set(X):
    """
    Set spectra first then brightness
    """
    s = serial.Serial(path,9600)
    s.timeout = 4
    s.readlines()
    s.write("manual_connect\r\n".encode("ascii"))
    s.timeout = 1
    s.readlines()
    if X!=None and X[0]!="":
        s.write("set(brilho,100)\r\n".encode("ascii"))
        s.timeout = 1
        s.readlines()
        with open("../data/spectra/parameters.json") as f:
            param = json.load(f)
            param = sorted(param.items(), key= lambda x: x[0])

            for p,x in zip(param, X):
                time.sleep(2)
                string = f"set({p[0]},{int(100*x)})\r\n"
                print(string)
                s.write(string.encode("ascii"))
                s.readlines()
    s.close()
    return 0

def f_read():
    """
    Read info from Arduino
    """
    s = serial.Serial(path,9600)
    s.timeout = 4
    s.readlines()
    s.write("manual_connect\r\n".encode("ascii"))
    s.timeout = 1
    s.readlines()
    s.write("dados\r\n".encode("ascii"))
    s.timeout = 10
    y = s.read_until(b'\n').decode("ascii").strip("\n").strip("\r")
    y = y.split(" ")
    print(f"RESPONSE: {y}")
    s.close()
    return y

def f_command(c):
    """
    Sends command to Arduino
    """
    s = serial.Serial(path,9600)
    s.timeout = 4
    s.readlines()
    s.write("manual_connect\r\n".encode("ascii"))
    s.timeout = 1
    s.readlines()
    s.timeout = 1
    s.write(f"{c}\r\n".encode("ascii"))
