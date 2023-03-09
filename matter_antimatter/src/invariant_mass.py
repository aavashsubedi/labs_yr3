import numpy as np
from utils.constants import MASS_KAON
from utils.constants import MASS_PION



def find_invariant_mass(momentum_1=[0, 0, 0],
                                   momentum_2=[0, 0, 0],
                                   momentum_3=[0, 0, 0],
                                   is_kaon=[1, 1, 1]):
    

    mass_array=[]
    for i in is_kaon:
        if i == 1:
            mass_array.append(MASS_KAON)
        else:
            mass_array.append(MASS_PION)


    p1_x, p1_y, p1_z = momentum_1
    p2_x, p2_y, p2_z = momentum_2
    p3_x, p3_y, p3_z = momentum_3
    
    E1 = np.sqrt(np.square(p1_x) + np.square(p1_y) + np.square(p1_z) + np.square(mass_array[0]))
    E2 = np.sqrt(np.square(p2_x) + np.square(p2_y) + np.square(p2_z) + np.square(mass_array[1]))
    E3 = np.sqrt(np.square(p3_x) + np.square(p3_y) + np.square(p3_z) + np.square(mass_array[2]))
        
    energy_squared   = np.square(E1 + E2 + E3)
    total_momentum_x = p1_x + p2_x + p3_x
    total_momentum_y = p1_y + p2_y + p3_y
    total_momenum_z  = p1_z + p2_z + p3_z
    #total momentum
    inv_mass_squared = energy_squared - np.square(
        total_momentum_x) - np.square(total_momentum_y) - np.square(total_momenum_z)

    return np.sqrt(inv_mass_squared)