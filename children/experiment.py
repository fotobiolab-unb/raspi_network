import numpy as np
import logging
import random
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

"""
Wrapper for function used on the raspberries. Called on hanashi/static_set
"""

# def f(X):
#     X = np.array(X)
#     return 10*len(X)+(-X*X+10*np.cos(2*np.pi*X)).sum()

import serial
import json
import time

# def f(X):
#     """
#     Set spectra first then brightness
#     """
#     s = serial.Serial("/dev/ttyACM0",9600)
#     s.write("manual_connect\r\n".encode("ascii"))
#     s.write("set(brilho,100)\r\n".encode("ascii"))
#     with open("../data/spectra/parameters.json") as f:
#         param = json.load(f)
#         param = sorted(param.items(), key= lambda x: x[0])
        
#         for p,x in zip(param, X):
#             time.sleep(2)
#             string = f"set({p[0]},{int(100*x)})\r\n" 
#             print(string)
#             s.write(string.encode("ascii"))
#     return 0

def f(X):
    print("Running Experiment")
    print(X)
    return 0