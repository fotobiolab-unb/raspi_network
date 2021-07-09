import numpy as np
import random
import serial
import json
import time
import glob
import sys

"""
This library is responsible to establish communication with the experiment. In this case we're using an Arduino board as microcontroller.
"""

def decode(lines):
    """
    Converts Arduino response to a string.
    """
    return list(map(lambda x: x.decode().strip(),lines))

class arduino:
    def __init__(self):
        """
        At start it will look for a serial device on /dev. Only works for GNU/Linux or some other Unix based system.
        In the case of Windows, you have to replace the paths below with the proper path.
        """
        self.g = glob.glob("/dev/ttyACM*")
        if len(self.g) == 0:
            self.g = glob.glob("/dev/ttyUSB*")
        self.g = sorted(self.g)[0]
        self.timeout = 10
        self.baud = 9600
        self.serial = None
        sys.stdout.flush()
    def send(self,command,returns=True):
        """
        Sends a command to Arduino and waits for a response.
        If `returns` is set to `True`, it will return the response.
        
        Args:
            command (str): Command to send to Arduino.
            returns (bool): Whether or not to return a response.
        """
        t1 = time.time()
        self.serial.write((command+"\r\n").encode("ascii"))
        time.sleep(self.timeout)
        response = decode(self.serial.readlines())
        print("[ARDUINO_RESPONSE]", response)
        print("Connection Established.","TIME",time.time()-t1)
        sys.stdout.flush()
        if returns:
            return response
    def connect(self):
        """
        Starts a connection to Arduino and keeps it awake.
        """
        self.serial = serial.Serial(self.g,self.baud)
        self.serial.timeout = self.timeout
        time.sleep(self.timeout)
        header = decode(self.serial.readlines())
        self.columns = header[2].split(" ")
        response = self.send("manual_connect")
        self.send("quiet_connect")
        sys.stdout.flush()
        return header + response
    def set(X):
        """
        Sends a parameter tuple to Arduino.
        """
        if X!=[None]:
            with open("../data/spectra/parameters.json") as f:
                param = json.load(f)
                try:
                    del param["header"]
                except KeyError:
                    pass
                param = sorted(param.items(), key= lambda x: x[0])

                for p,x in zip(param, X):
                    string = f"set({p[0]},{int(100*x)})"
                    print(string)
                    response = self.send(string)
                    print(response)
        sys.stdout.flush()
    def read(self):
        """
        Reads info from Arduino
        """
        response = self.send("dados")
        
        y = response
        y = y[0]
        y = y.split(" ")
        y = dict(zip(self.columns,y))
        print(f"READ RESPONSE: {y}")
        sys.stdout.flush()
        return y