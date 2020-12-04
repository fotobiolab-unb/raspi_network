import sys
sys.path.append("../main_server/")
import numpy as np
import json
import hanashi
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
    s.write("set(brilho,{})\r\n".format(str(b)).encode("ascii"))

def set_uniform(s):
    with open("../data/spectra/parameters.json") as f:
        param = json.load(f)
        param = sorted(param.items(), key= lambda x: x[0])
        
        for p,x in zip(param, X):
            string = "set({},{})\r\n".format(str(p[0]),str(int(100*x)))
            time.sleep(1)
            print(string)
            s.write(string.encode("ascii"))
