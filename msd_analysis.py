#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 19:42:04 2022

@author: todor
"""

from xml2csv import xml2csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants import Boltzmann as k


FPS = 62.8
pixel = 0.6e-4 / 979.3




def MSD(data, max_tau):
    
    
    
    mean_sq_dev = []
    
    for interval in range(1, max_tau):
        
        sq_dev = []
        
        for row in range(0, len(data) - interval - 1):
        
            sq_dev.append((data[row + interval] - data[row])**2)
            
        
        mean_sq_dev.append(np.mean(sq_dev) )
        
        
    
    
    return mean_sq_dev


def fit_viscosity(msd, fit_limit=-1):
    if fit_limit == -1:
        fit_limit = len(msd)
    
    t = np.arange(0, fit_limit)
    t = t * 1/ FPS
    msd = np.array(msd)
    msd = msd * pixel
    popt, pcov = curve_fit(linear, t, msd[0:fit_limit])
    plt.scatter(t, msd[0:fit_limit], )
    plt.plot(t, linear(t, *popt), color='red')
    plt.show()
    D = popt[0] / 2
    print(D)
    T = (273.15 + 20)
    viscosity = k * T / (6 * np.pi * D * 0.25e-6)
    visc2 = (4 * k * T) / (3 * np.pi * popt[0] * 0.5e-6)
    print(viscosity, visc2)
    

def linear (x, a, b):
    return a * x + b


if __name__ == "__main__":
    filename = "day3_vid2_Tracks0-3500.xml"
    data_raw = xml2csv(filename)
    data = data_raw[5]
    print(len(data))
    x_msd = MSD(data=data[:, 1], max_tau=100)
    y_msd = MSD(data=data[:, 2], max_tau=100)
    
    plt.plot(data[:, 1], data[:, 2])
    plt.show()
    
    fit_viscosity(x_msd)
    fit_viscosity(y_msd)
    
    
    