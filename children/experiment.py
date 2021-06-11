import numpy as np
import logging
import random
import serial
import json
import time
import glob
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

path = ""
g = glob.glob("/dev/ttyACM*")
if len(g)==0:
    g=glob.glob("/dev/ttyUSB*")
try:
    timeout=10
    path = sorted(g)[0] #Attept to auto find available Arduino (assuming that there is just one)
    """
    Initiating communications
    """
    s = serial.Serial(path,9600)
    s.timeout = 10
    time.sleep(4)
    header = s.readlines()
    header = list(map(lambda x: x.decode().rstrip(),header))
    print(*header)
    columns = header[2].split(" ")
    print("COLUMN ARRANGEMENT", *columns)
    time.sleep(4)
    s.write("manual_connect\r\n".encode("ascii"))
    time.sleep(4)
    print(*s.readlines())
    print("Arduino ready (apparently...)")

    def f_set(X):
        """
        Set spectra first then brightness
        """
        #s = serial.Serial(path,9600)
        #s.timeout = 4
        #s.readlines()
        #s.write("manual_connect\r\n".encode("ascii"))
        #s.timeout = 1
        #s.readlines()
        if X!=[None] and X[0]!="":
            #s.write("set(brilho,100)\r\n".encode("ascii"))
            #s.timeout = 1
            #s.readlines()
            with open("../data/spectra/parameters.json") as f:
                param = json.load(f)
                param = sorted(param.items(), key= lambda x: x[0])

                for p,x in zip(param, X):
                    #time.sleep(2)
                    string = f"set({p[0]},{int(100*x)})\r\n"
                    print(string)
                    s.write(string.encode("ascii"))
                    time.sleep(2)
                    print("RESPONSE", *s.readlines())
        #s.close()
        return 0

    def f_read():
        """
        Read info from Arduino
        """
        #s = serial.Serial(path,9600)
        #s.timeout = 4
        #print(*s.readlines())
        #s.write("manual_connect\r\n".encode("ascii"))
        #s.timeout = 4
        #s.readlines()
        s.write("dados\r\n".encode("ascii"))
        s.timeout = 10
        time.sleep(10)
        #y = s.read_until(b'\n').decode("ascii").strip("\n").strip("\r")
        y = list(map(lambda x: x.decode("ascii").strip(),s.readlines()))
        y = y[0]
        y = y.split(" ")
        y = dict(zip(columns,y))
        print(f"READ RESPONSE: {y}")
        #s.close()
        return y

    def f_command(c):
        """
        Sends command to Arduino
        """
        #s = serial.Serial(path,9600)
        #s.timeout = 4
        #print(*s.readlines())
        #s.write("manual_connect\r\n".encode("ascii"))
        #s.timeout = 1
        #s.readlines()
        s.timeout = 10
        print("COMMAND", c)
        s.write(f"{c}\r\n".encode("ascii"))
        time.sleep(10)
        r = s.readlines()
        print("RESPONSE", *r)
        return r

except:
    print("=================")
    print("ARDUINO NOT FOUND")
    print("=================")