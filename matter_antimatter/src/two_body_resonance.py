import numpy as np
from src.invariant_mass import inv_mass_2body


def find_resonance(momentum_1=[0, 0, 0],
                   momentum_2=[0, 0, 0],
                   momentum_3=[0, 0, 0],
                   is_kaon=[1, 1, 1],
                   charge=[1, 1, -1]):
    """Find the invariant mass of a 2 body resonance

    Parameters
    ----------
    momentum_1 : [double, double, double]
        momentum of first particle in the event, by default [0, 0, 0]
    momentum_2 : [double, double, double]
        momentum of second particle in the event, by default [0, 0, 0]
    momentum_3 : [double, double, double]
        momentum of third particle in the event, by default [0, 0, 0]
    is_kaon : [bool, bool, bool]
        which particles are kaons(1), remaining are pions(0), by default [1, 1, 1]
    charge : [int, int, int]
        charges of particles, can be +1 or -1, by default [1, 1, -1]

    Returns
    -------
    [double, double]
        invariant masses of both neutral 2 body resonances for the event [Kpi, pipi]
    """    
    total_charge = np.sum(charge)

    momentum_matrix = np.append([momentum_1], [momentum_2], axis=0)
    momentum_matrix = np.append(momentum_matrix, [momentum_3], axis=0)

    body1_index = -1
    body2_index = -1
    inv_mass = [0, 0]
    
    print("New event:")
    print(is_kaon)
    for j in range(0, len(is_kaon)):
        if charge[j] != total_charge:
            body1_index = j
            print("    {0}".format(j))
            break

    for i in range(0, len(is_kaon)):
        if charge[i] == total_charge:
            body2_index == i

            if is_kaon[i] == 1:
                print("    filling 0")
                inv_mass[0] = inv_mass_2body(momentum_matrix[body1_index, :], 
                                            momentum_matrix[i, :], 
                                            is_kaon=[is_kaon[body1_index], is_kaon[i]])
            else:
                print("    filling 1")
                inv_mass[1] = inv_mass_2body(momentum_matrix[body1_index, :], 
                                            momentum_matrix[i, :], 
                                            is_kaon=[is_kaon[body1_index], is_kaon[i]])

            
    return inv_mass

