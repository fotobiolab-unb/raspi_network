import sys
sys.path.append("../main_server/")
import numpy as np
import json
import time
import serial

def uniform(alpha):
    with open("../data/spectra/neutral_spectrum_components.json") as f:
        coefficients = json.load(f)["coefficients"]
        coefficients = np.array(coefficients)
        coefficients = alpha*coefficients
        hanashi.create_new_batch(coefficients.reshape((1,coefficients.shape[0])))
        hanashi.step()

def init(*params):
    s = serial.Serial(*params)
    s.write("silent_connect\r\n".encode("ascii"))
    return s

def brilho(s,b):
    s.write(f"set(brilho,{b})\r\n".encode("ascii"))

def set_uniform(s):
    with open("../data/spectra/parameters.json") as f, open("../data/spectra/neutral_spectrum_components.json") as g:
        param = json.load(f)
        param = sorted(param.items(), key= lambda x: x[0])
        coefficients = json.load(g)
        X = coefficients["coefficients"]
        
        for p,x in zip(param, X):
            string = f"set({p[0]},{int(100*x)})\r\n"
            s.write(string.encode("ascii"))
            time.sleep(1)
            print(string)
            s.write(string.encode("ascii"))
