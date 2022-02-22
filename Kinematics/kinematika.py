#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

def r(time):
    #Here define the function that describes the motion.
    return (5*(time**2)-2*time+4)

def posVector(time1, time2):
    # Position vector of the motion between a timeframe.
    return (r(time2)-r(time1))

def avgVelocity(time1, time2):
    # The average velocity of a timeframe.
    return (posVector(time1, time2) / (time2-time1))

def instantVelocity(time, offset):
    # The velocity at a little enough timeframe, that defines instantVelocity.
    return avgVelocity(time, time+offset)

def diff(r, stepSize):
    # Differentiate the r(t) function with forward, backward and between differentiation
    if len(r) < 2:
        return False
    y = np.empty((1))
    for x in range(len(r)):
        if x == 0:
            y = np.append(y, (r[x+1]-r[x])/stepSize)
        elif x == (len(r)-1):
            y = np.append(y, (r[x]-r[x-1])/stepSize)
        else:
            y = np.append(y, (r[x+1]-r[x])/(2*stepSize))
    return y

def posTime(timeRange):
    # Draws the position-time diagram of the r(t) function.
    rt = [r(t) for t in range(timeRange)]
    plt.figure()
    plt.plot(rt)
    plt.show()
    return rt

def velTime(timeRange):
    # Draws the velocity-time diagram of the r(t) function. Derived from r(t)
    v = diff(posTime(timeRange))
    plt.figure()
    plt.plot(v)
    plt.show()
    return v

def accelaration():
    pass

def draw(timeRange, stepSize):
    # Draw all the diagrams: position-time, velocity-time, accelaration-time
    rt = [r(t) for t in range(0, timeRange, stepSize)] # position-time
    vt = diff(rt, stepSize) # velocity-time
    at = diff(vt, stepSize) # accelaration-time
    print(rt)
    print(vt)
    print(at)
    plt.figure(1, figsize=(10,4))
    plt.subplot(311)
    plt.plot(rt)
    plt.subplot(312)
    plt.plot(vt)
    plt.subplot(313)
    plt.plot(at)
    plt.show()
    


if __name__ == '__main__':
    draw(10, 1)
