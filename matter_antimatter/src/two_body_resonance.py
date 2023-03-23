import numpy as np
from src.invariant_mass import inv_mass_2body
from tqdm import tqdm


def append_args(iterator, args, args_new):
    """_summary_

    Parameters
    ----------
    iterator : int
        event to be added to new array
    args : list [][]
        all arguments returned by file reading unpacked
    args_new : ndarray
        numpy array with every row separate event
    """
    new_row = np.array([])
    print(new_row)
    for i in range(0, len(args)):
        new_row = np.append(new_row, args[i][iterator])
    args_new = np.append(args_new, [new_row], axis=0)
    return args_new
    


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
    
    #print("New event:")
    #print(is_kaon)
    for j in range(0, len(is_kaon)):
        if charge[j] != total_charge:
            body1_index = j
            #print("    {0}".format(j))
            break

    for i in range(0, len(is_kaon)):
        if charge[i] == total_charge:
            body2_index = i

            if is_kaon[i] == 1:
                #print("    filling 0")
                inv_mass[0] = inv_mass_2body(momentum_matrix[body1_index, :], 
                                            momentum_matrix[body2_index, :], 
                                            is_kaon=[is_kaon[body1_index], is_kaon[body2_index]])
            else:
                #print("    filling 1")
                inv_mass[1] = inv_mass_2body(momentum_matrix[body1_index, :], 
                                            momentum_matrix[body2_index, :], 
                                            is_kaon=[is_kaon[body1_index], is_kaon[body2_index]])

            
    return inv_mass

def iterate_events(args):
    """_summary_

    Parameters
    ----------
    args : same as outputted by the file reading
    """
    pT, p_H1, p_H2, p_H3, h1_prob, h2_prob, h3_prob, master_prob, invariant_mass_array, is_kaon, charge_H1, charge_H2, charge_H3 = args
    new_inv_mass = []
    
    xmin, xmax = (5235, 5333)   #functional optimisation
    

    two_body_resonance_array = np.array([[-1, -1]])
    

    print("Iterating all read events:")
    for event_iterator in tqdm(range(0, len(invariant_mass_array))):
        if invariant_mass_array[event_iterator] < xmin or invariant_mass_array[event_iterator] > xmax:
            continue
        
        
        kaon_place = [is_kaon[0][event_iterator], is_kaon[1][event_iterator], is_kaon[2][event_iterator]]
        charges = [charge_H1[event_iterator], charge_H2[event_iterator], charge_H3[event_iterator]]
        p1 = [p_H1[0][event_iterator], p_H1[1][event_iterator], p_H1[2][event_iterator] ]
        p2 = [p_H2[0][event_iterator], p_H2[1][event_iterator], p_H2[2][event_iterator] ]
        p3 = [p_H3[0][event_iterator], p_H3[1][event_iterator], p_H3[2][event_iterator] ]
        resonance = find_resonance(p1, p2, p3 , is_kaon=kaon_place, charge=charges)
        
        two_body_resonance_array = np.append(two_body_resonance_array, [resonance], axis=0)
        new_inv_mass.append(invariant_mass_array[event_iterator])
        #new_args = append_args(event_iterator, args, new_args)

    two_body_resonance_array = np.delete(two_body_resonance_array, 0, axis=0)
    return  two_body_resonance_array, new_inv_mass
            


