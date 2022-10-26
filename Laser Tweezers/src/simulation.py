#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 00:54:42 2022

@author: todor
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import Boltzmann as kb



TIMESTEP = 0.01
initial_position = np.array([0, 0, 0])
total_steps = 30000
PARTICLE_RADIUS = 2    #in microns
VISCOSITY = 0.001      #in Pa.s
TEMPERATURE = 300
pdf_resolution = 30
  #in m
# wall is in -z direction

k_x = 2  #in fN/nm
k_y = 2
k_z = 0.5      #in fN/nm
r = PARTICLE_RADIUS * 1e-6


gamma = 6 * np.pi * VISCOSITY * r



k_x = k_x * 1e+9 * 1e-15
k_y = k_y * 1e+9 * 1e-15
k_z = k_z * 1e+9 * 1e-15


def D(h=np.inf):
    Dinf = kb * TEMPERATURE / gamma
    if h == np.inf:
        return np.array([Dinf, Dinf, Dinf])
    else:
        D_par = (1 - 9 * r / (16 * h)) * Dinf
        D_perp = (1 - 9 * r / (8 * h)) * Dinf
        if(D_par < 0 or D_perp < 0):
           print("Hit wall")
           return np.array([-1, -1, -1])
        #print("No wall")
        return np.array([D_par, D_par, D_perp])
    



def gaussian (x, sigma, mean):
    
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / sigma)**2)




def trapped_particle(dist_wall = 1e-5):
    
    noise_sample = np.random.normal(0, 1 / np.sqrt(TIMESTEP), (total_steps, 3))


    k = np.array([k_x, k_y, k_z])
    
    h = dist_wall
    position_time = np.array([[0, 0, 0]])
    

    for iterator in range(1, len(noise_sample)):
        if(D(h)[1] == -1 or h < 0):
            h = dist_wall
            position_time = np.append(position_time, np.array([[0, 0, 0]]), axis=0)
            continue
        next_position = position_time[-1, :] - k/gamma * position_time[-1, :] \
        * TIMESTEP + np.sqrt(2 * D(h)) * noise_sample[iterator, :]
        position_time = np.append(position_time, np.array([next_position]), axis=0)
        h += next_position[2] - position_time[-2, 2]
        
        
        

    x_t = position_time[:, 0]
    y_t = position_time[:, 1]
    z_t = position_time[:, 2]
    plt.scatter(x_t, y_t, alpha=0.01)
    
    print("Generated sample")
    
    pdf = np.zeros((pdf_resolution, pdf_resolution))
    pdf_z = np.zeros((pdf_resolution, pdf_resolution))
    range_x = np.max(x_t) - np.min(x_t)
    range_y = np.max(y_t) - np.min(y_t)
    range_z = np.max(z_t) - np.min(z_t)
    
    for i in range(0, len(x_t)):
        if(i%1000 == 0):
            print("{0}/{1}".format(i, len(x_t)))
        
        for iterator_x in range(0, pdf.shape[1]):
            if(x_t[i] >= range_x/pdf.shape[1] * iterator_x + np.min(x_t) and x_t[i] < range_x/pdf.shape[1] * (iterator_x + 1) + np.min(x_t)):
                
            
            
                for iterator_y in range(0, pdf.shape[0]):
                    if(y_t[i] >= iterator_y * range_y/pdf.shape[0] + np.min(y_t) and y_t[i] < (iterator_y + 1) * range_y/pdf.shape[0] + np.min(y_t)):
                        pdf[iterator_y, iterator_x] += 1
                    if(z_t[i] >= iterator_y * range_z/pdf.shape[0] + np.min(z_t) and z_t[i] < (iterator_y + 1) * range_z/pdf.shape[0] + np.min(z_t)):
                        pdf_z[iterator_y, iterator_x] += 1
            
            
    
    
    x_plot = np.linspace(-2e-5, 2e-5, 100)
    y_plot =  np.sqrt(((2e-5 )**2  * k[0] - k[0] * x_plot**2) / k[1])
    plt.plot(x_plot, y_plot, color="r")
    plt.plot(x_plot, -y_plot, color="r")
    plt.show()
    
    
    x_cont = np.linspace(np.min(x_t), np.max(x_t), pdf.shape[1])
    y_cont = np.linspace(np.min(y_t), np.max(x_t), pdf.shape[0])
    z_cont = np.linspace(np.min(z_t), np.max(z_t), pdf_z.shape[1])
    
    

    
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 5)
    ax.contourf(x_cont, y_cont, pdf)
    ax.set_title("PDF of particle position in trap")
    ax.set_ylabel("y(m)")
    ax.set_xlabel("x(m)")
    fig.savefig("pdf_trapped.png", dpi=600)
    plt.show()
    
    plt.scatter(x_t, z_t, alpha=0.05)
    dummy = np.linspace(np.min(x_t), np.max(x_t), 1000)
    plt.plot(dummy, np.full(dummy.shape, -dist_wall))
    
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 5)
    ax.contourf(x_cont, z_cont, pdf_z)
    ax.set_title("PDF of particle position in trap")
    ax.set_ylabel("z(m)")
    ax.set_xlabel("x(m)")
    dummy = np.linspace(np.min(x_t), np.max(x_t), 1000)
    plt.plot(dummy, np.full(dummy.shape, -dist_wall))
    fig.savefig("pdf_trapped_z.png", dpi=600)
    plt.show()
    
    
if __name__ == "__main__":
    trapped_particle()
