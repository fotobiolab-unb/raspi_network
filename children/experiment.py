import numpy as np
import logging
import random
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

"""
Wrapper for function used on the raspberries. Called on hanashi/static_set
"""

def f(X):
    X = np.array(X)
    return 10*len(X)+(X*X-10*np.cos(2*np.pi*X)).sum()
