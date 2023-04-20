import numpy as np

def num_muons(muon_prob, number_desired):
    count = 0
    for prob in muon_prob:
        if prob == 1:
            count += 1
    if count == number_desired:
        return True
    return False

#(pion_prob, kaon_prob)
def is_pion(probabilities, pimin=0.5, kmax=0.45):

    if probabilities[0] > pimin:
        if probabilities[1] < kmax:
            return True
    return False

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
    #we want to see if the absolute value of the sum of the charges is 1

    if abs(summed_charges) != 1:
        return False
    
    #now we check if this new particle is a pion 
    index_interest = -1
    for index in range(0, len(charges)):
        if abs(charges[index]) == 1:
            index_interest = index
            break

    if index_interest == -1:
        return False
    if is_pion(probabilites[index_interest]):
        return False #we don't want pions
    if is_kaon(probabilites[index_interest]):
        return True
    #returns true if we have a kaon
    return 1

def charge_rule_iterator(charges = [1, 1, -1], 
                         intrested_charge = 1):
    summed_charges = charges[0] + charges[1] + charges[2]
    if summed_charges == intrested_charge:
        return True
    return False

def assign_kaon_iterator(probabilites = [[], [], []],
                         charges = [1, 1, -1], 
                         muon_prob = [0, 0, 0]):
    
    count_muon = 0
    count_kaon = 0
    where_kaon = []

    for iterator_particles in range(0, len(charges)):

        if muon_prob[iterator_particles]:
                count_muon += 1
                where_kaon.append(0)
        elif is_kaon(probabilites[iterator_particles]):
                count_kaon += 1
                where_kaon.append(1)
        else:
            where_kaon.append(0)
    #print(where_kaon)
    if count_kaon == 1:
        #we only have on kaon in the event
        if len(where_kaon) == 3:
            return where_kaon
    
    return False

