import numpy as np
import logging
import random
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

"""
Wrapper for function used on the raspberries. Called on hanashi/static_set
"""

def f(X):
    return random.random()
