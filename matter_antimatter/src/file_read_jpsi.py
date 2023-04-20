import numpy as np
import uproot
from tqdm import tqdm
from src.invariant_mass import find_invariant_mass

from src.selection_rule_jpsi import selection_rule_iterator
from src.selection_rule_jpsi import assign_kaon_iterator
from src.selection_rule_jpsi import charge_rule_iterator
from src.selection_rule_jpsi import num_muons
from src.two_body_resonance import find_resonance

from utils.constants import MASS_MUON



list_of_interesting_keys = []
for i in range(1, 4):
    exec(f"list_of_interesting_keys.append('H{i}_PX')")
    exec(f"list_of_interesting_keys.append('H{i}_PY')  ")
    exec(f"list_of_interesting_keys.append('H{i}_PZ')  ")
    exec(f"list_of_interesting_keys.append('H{i}_Charge')  ")
    exec(f"list_of_interesting_keys.append('H{i}_ProbK')  ")
    exec(f"list_of_interesting_keys.append('H{i}_ProbPi')  ")
    exec(f"list_of_interesting_keys.append('H{i}_isMuon')  ")


def two_body_muon_reconstruction(momentum_1 = [0, 0, 0],
                                momentum_2  = [0, 0, 0],
                                momentum_3  = [0, 0, 0],
                                muon_prob   = [1, 1, 1]):     
    cleaned_momentum = []
    total_momentum_array = [momentum_1, momentum_2, momentum_3]

    for i in range(3):
        if muon_prob[i] == 1:
            cleaned_momentum.append(total_momentum_array[i])
    del total_momentum_array
    momentum_1 = cleaned_momentum[0]
    momentum_2 = cleaned_momentum[1]

    p1_x, p1_y, p1_z = momentum_1
    p2_x, p2_y, p2_z = momentum_2

    E1 = np.sqrt(p1_x**2 + p1_y**2 + p1_z**2 + MASS_MUON**2)
    E2 = np.sqrt(p2_x**2 + p2_y**2 + p2_z**2 + MASS_MUON**2)

    energy_squared = np.square(E1 + E2)
    total_momentum_x = p1_x + p2_x
    total_momentum_y = p1_y + p2_y
    total_momentum_z = p1_z + p2_z

    inv_mass_squared = energy_squared - (total_momentum_x**2 + total_momentum_y**2 + total_momentum_z**2)

    return np.sqrt(inv_mass_squared)



def read_file(path_name="", MAX_EVENTS=5000, mode=1, keys = list_of_interesting_keys,
              selection=False, output="", interest=None):
    #if interest == "B+" or interest == "B+" then we apply the selection rule
    if not path_name:
        path = 'data/'  # set this to '' to run on the GitHub version
    else:
        path = path_name

    #temporarily 
    event_counter = 0

    jpsi_reconstructed = []
    is_kaon_H1 = []
    is_kaon_H2 = []
    is_kaon_H3 = []

    print(f" Selecting {interest} events")

    print("Input data varaiables: ")
    if mode == 0:
        events_test = uproot.open(path+'example_file.root')
        print("Test mode")
        trees = [events_test['PhaseSpaceTree;1']]  # Test mode
#        return [[0], [0], [0], [0]]
        print(events_test.keys())

    elif mode == 1:
        events_sim = uproot.open(path+'PhaseSpaceSimulation.root')
        trees = [events_sim['PhaseSpaceTree']]                       # Simulation
        print("Phase space simulation")
        print(events_sim.keys())
    elif mode == 2:
        # Magnet down data
        events_down = uproot.open(path+'B2HHH_MagnetDown.root')
        trees = [events_down['DecayTree']]
        print("Magnet down data")
        print(events_down.keys())
    elif mode == 3:
        # Magnet up data
        events_up = uproot.open(path+'B2HHH_MagnetUp.root')
        trees = [events_up['DecayTree']]
        print("Magnet up data")
        print(events_up.keys())
    elif mode == 4:
        events_up = uproot.open(path+'B2HHH_MagnetUp.root')
        events_down = uproot.open(path+'B2HHH_MagnetDown.root')
        trees = [events_down['DecayTree'], events_up['DecayTree']]
        print("Magnet up and down data")
        print(events_down.keys())
    else:
        print("Mode not recognised")
        return [[0], [0], [0], [0]]
    print("Varialbes read")
    print()
    for tree in trees:
        # This outer loop is a technical loop of uproot over chunks of events
        for data in tree.iterate(keys):
            num_elem = MAX_EVENTS if MAX_EVENTS < len(data['H1_PZ']) else len(data['H1_PZ'])

            for i in tqdm(range(0, num_elem)):
                event_counter += 1
                if 0 < MAX_EVENTS and MAX_EVENTS < event_counter:
                    break

                if (data['H1_PZ'][i] < 0) or (data['H2_PZ'][i] < 0) or (data['H3_PZ'][i] < 0):
                    continue


                if selection:
                    probabilities_itr = [[data['H1_ProbPi'][i], data['H1_ProbK'][i]],
                                        [data['H2_ProbPi'][i], data['H2_ProbK'][i]],
                                        [data['H3_ProbPi'][i], data['H3_ProbK'][i]]]
                    
                    charges_itr = [data['H1_Charge'][i], data['H2_Charge'][i], data['H3_Charge'][i]]
                    
                    muon_prob = [data['H1_isMuon'][i], data['H2_isMuon'][i], data['H3_isMuon'][i]]


                    #if there are no muons we can continue
                    if muon_prob.count(1) !=2:
                        continue
                    
                    if selection_rule_iterator(probabilities_itr, charges_itr) is False:
                        continue

                    if assign_kaon_iterator(probabilities_itr, charges_itr, muon_prob) is False:
                        #now we only have 2 muons and one kaon
                        continue
                    
                    if interest == "B+" or interest == "B-":
                        if interest == "B+":
                            if charge_rule_iterator(charges_itr, +1) is False:
                                continue
                        elif interest == "B-":
                            if charge_rule_iterator(charges_itr, -1) is False:
                                continue
                    #now we have 2 muons and one kaon and the correct charge (e.g. B+ -> K+ mu+ mu-)
                    kaon_place = assign_kaon_iterator(probabilities_itr, charges_itr, muon_prob)
                    is_kaon_H1.append(kaon_place[0])
                    is_kaon_H2.append(kaon_place[1])
                    is_kaon_H3.append(kaon_place[2])

                    #now we have an array of [0, 0, 1] where there is a kaon  in the third place
                    #we need to find the the ind
                
                
                    # Your invariant mass calculation should go here
                    p1_array = [data['H1_PX'][i], data['H1_PY'][i], data['H1_PZ'][i]]
                    p2_array = [data['H2_PX'][i], data['H2_PY'][i], data['H2_PZ'][i]]
                    p3_array = [data['H3_PX'][i], data['H3_PY'][i], data['H3_PZ'][i]]

                    jpsi_inv_mass = two_body_muon_reconstruction(p1_array, p2_array, p3_array, muon_prob)
                    jpsi_reconstructed.append(jpsi_inv_mass)

    return jpsi_reconstructed
    


if __name__ == "__main__":
    read_file()
