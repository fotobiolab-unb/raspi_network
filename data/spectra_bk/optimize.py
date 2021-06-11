import numpy
from scipy.optimize import minimize

def least_squares(func,xdata,ydata):
    return lambda w: ((func(xdata,w)-ydata)**2).sum()

def curve_fit(func,xdata,ydata,x0,*p):
    """
    func must receive paramaters in the form (x,param). Where param is a numpy array of parameters.
    """
    return minimize(least_squares(func,xdata,ydata),x0,*p)