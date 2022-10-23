

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:01:57 2022
@author: todor
"""

def xml2csv(filename, tolerance=3):
    """
    Read xml file into an numpy array with format [t, x, y]
    Parameters
    ----------
    filename : string
        DESCRIPTION.
    tolerance : int
        If a gap has fewer frames than this number the tracks will be combined.
    Returns
    -------
    output : ndarray
        [t, x, y].
    """
    import xml.etree.ElementTree as ET
    from collections import defaultdict
    import numpy as np

    root = ET.parse(filename).getroot()

    
    
    data = np.array([[-1, -1, -1]])
    
    for i in range(0, len(root[:])):
        for row in range(0, len(root[i][:])):
            temp_row = []
            temp_row.append(int(root[i][row].attrib['t']))
            temp_row.append(float(root[i][row].attrib["x"]))
            temp_row.append(float(root[i][row].attrib["y"]))
            
            temp_row = np.array([temp_row])
            
            data = np.append(data, temp_row, axis=0)

    data = np.delete(data, 0, axis=0)
    output = []
    prev_gap = 0
    for index in range(0, len(data) - 1):
        if(data[index + 1, 0] - data[index, 0] > tolerance):
            output.append(data[prev_gap:index + 1, :])
            prev_gap = index + 1
        if (index + 1 == len(data) - 1):
            output.append(data[prev_gap:index + 1, :])

    return output            
    
            
    
    

    
if __name__=="__main__":
    print(xml2csv(filename, 3))
