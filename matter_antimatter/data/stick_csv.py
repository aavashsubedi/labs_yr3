#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:43:30 2023

@author: todor
"""

import numpy as np

mode = "inv_mass"
charge = "Bplus"

array1 = np.genfromtxt(mode + "_filtered_5100_5235_" + charge + ".csv", delimiter=',')
array2 = np.genfromtxt(mode + "_filtered_" + charge + ".csv", delimiter=',')
array3 = np.genfromtxt(mode + "_filtered_5333_5400_" + charge + ".csv", delimiter=',')
array4 = np.genfromtxt(mode + "_combinatorial_" + charge + ".csv", delimiter=',')

result = np.append(array1, array2, axis=0)
result = np.append(result, array3, axis=0)
result = np.append(result, array4, axis=0)

np.savetxt(mode + "_filtered_all_" + charge + ".csv", result, delimiter=',')