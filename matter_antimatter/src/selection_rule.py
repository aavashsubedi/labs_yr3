import numpy as np


#(pion_prob, kaon_prob)
def is_pion(probabilities, pimin=0.5):

    if probabilities[0] > pimin:
        return True
    return False
<<<<<<< HEAD


=======
    
>>>>>>> 457d525dac4949a062c836c679ece238ddd00a47
def is_kaon(probabilities, kmin=0.6, pimax=0.4):
    if probabilities[1] > kmin:
        if probabilities[0] < pimax:
            return True
    return False


def is_neither(probabilities, kmin=0.2, pi_min=0.2):
    if probabilities[0] < pi_min:
        if probabilities[1] < kmin:
            return True
    return False


def selection_rule_iterator(probabilites = [[], [], []],
                            charges = [1, 1, -1]):

    summed_charges = charges[0] + charges[1] + charges[2]

    #index_intrest = np.where(charges != summed_charges)
    index_interest = []
    for index in range(0, len(charges)):
        if(charges[index] != summed_charges):
            index_interest.append(index)

    
    for index_iterator in index_interest:
        if is_pion(probabilites[index_iterator]):
            return 1
    
    return 0


def assign_kaon_iterator(probabilites = [[], [], []],
                         charges = [1, 1, -1]):
    
    summed_charges = charges[0] + charges[1] + charges[2]
    count_pion = 1
    count_kaon = 0
    where_kaon = []

    for iterator_particles in range(0, len(charges)):

        
            
        if(charges[iterator_particles] == summed_charges):
            if is_kaon(probabilites[iterator_particles]):
                count_kaon += 1
                where_kaon.append(1)
            if is_pion(probabilites[iterator_particles]):
                count_pion += 1
                where_kaon.append(0)

        if(charges[iterator_particles] != summed_charges):
            if is_pion(probabilites[iterator_particles]):
                where_kaon.append(0)
    #print(where_kaon)
    if count_kaon == 1:
        if len(where_kaon) == 3:
            return where_kaon
    
    return False

