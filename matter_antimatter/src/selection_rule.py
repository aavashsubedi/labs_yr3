import numpy as np

def check_pion(charge_array_1, charge_array_2, charge_array_3,
                probabilities_1, probabilities_2, probabilities_3):

    summed_charge = charge_array_1[0] + charge_array_2[0] + charge_array_3[0]

    #find the indices of intrest in the charge array 1
    indices_1 = np.where(charge_array_1 != summed_charge)
    # check in charge_array_1 with the indices of intrest and find the probability
    # that it is a kaon or a pion and check if its greater than 0.5
    return 0
    #check 

def simple_selection(prob_array_h1=[[], []],
                     prob_array_h2=[[], []],
                     prob_array_h3=[[], []],):
    
    all_indices = np.arange(len(prob_array_h1[0]))

    indices = np.where((prob_array_h1[0] > 0.3) & (prob_array_h1[1] > 0.3) & (prob_array_h2[0] > 0.3) & (prob_array_h2[1] > 0.3) & (prob_array_h3[0] > 0.3) & (prob_array_h3[1] > 0.3))

    #remove the indices that are in the second list
    indices = np.setdiff1d(all_indices, indices[0])

    return indices
 
def selection_rule(data,  selection_mode = 0):
    
    """
    This function takes in the prob arrays for each particle and returns a list
    of indicies for the particles that pass the selection rule.
    @param prob_array_h1: The prob array for the first particle (
                          data[H1_ProbPi], data[H1_ProbK]
    )
    @param prob_array_h2: The prob array for the second particle
    @param prob_array_h3: The prob array for the third particle

    @return: A list of indicies for the particles that pass the selection rule
    """

    # The selection rule is that the probability of a particle being a pion
    #use Nump.where to find where prbability_array_h1 is greater than 0.5
    #use Nump.where to find where prbability_array_h2 is greater than 0.5
    #use Nump.where to find where prbability_array_h3 is greater than 0.5
    prob_array_h1 = [data['H1_ProbPi'], data['H1_ProbK']]
    prob_array_h2 = [data['H2_ProbPi'], data['H2_ProbK']]
    prob_array_h3 = [data['H3_ProbPi'], data['H3_ProbK']]

    charge_array_h1 = np.array(data["H1_Charge"])
    charge_array_h2 = np.array(data["H2_Charge"])
    charge_array_h3 = np.array(data["H3_Charge"])


    if selection_mode == 0:
        indices = simple_selection(prob_array_h1, prob_array_h2, prob_array_h3)   


    return indices
#(pion_prob, kaon_prob)
def is_pion_iterator(probabilities):

    if probabilities[0] > 0.5:
        return 1

def selection_rule_iterator(probabilites = [[], [], []],
                            charges = [1, 1, -1]):

    summed_charges = charges[0] + charges[1] + charges[2]

    index_intrest = np.where(charges != summed_charges)

    if is_pion_iterator(probabilites[index_intrest]):
        return 1

    return 0

