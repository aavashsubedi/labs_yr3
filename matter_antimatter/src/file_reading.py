import numpy as np
import uproot
from tqdm import tqdm
from src.invariant_mass import find_invariant_mass

from src.selection_rule import selection_rule_iterator
from src.selection_rule import assign_kaon_iterator

from utils.constants import MASS_PION
from utils.constants import MASS_KAON



list_of_interesting_keys = []
for i in range(1, 4):
    exec(f"list_of_interesting_keys.append('H{i}_PX')")
    exec(f"list_of_interesting_keys.append('H{i}_PY')  ")
    exec(f"list_of_interesting_keys.append('H{i}_PZ')  ")
    exec(f"list_of_interesting_keys.append('H{i}_Charge')  ")
    exec(f"list_of_interesting_keys.append('H{i}_ProbK')  ")
    exec(f"list_of_interesting_keys.append('H{i}_ProbPi')  ")
    exec(f"list_of_interesting_keys.append('H{i}_isMuon')  ")


def read_file(path_name="", MAX_EVENTS=5000, mode=1, keys = list_of_interesting_keys,
              selection=False, output=""):

    if not path_name:
        path = 'data/'  # set this to '' to run on the GitHub version
    else:
        path = path_name

    #temporarily 
    event_counter = 0

    pX = []
    pY = []
    pZ = []
    pT = []


    h1_probpi = []
    h1_probk = []

    h2_probpi = []
    h2_probk = []

    h3_probpi = []
    h3_probk = []

    master_probpi = []
    master_probk = []

    invariant_mass_array = []



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
            # As Python can handle calculations with arrays, we can calculate derived quantities here
            pT_H1 = np.sqrt(data['H1_PX']**2+data['H1_PY']**2)
            pT_H2 = np.sqrt(data['H2_PX']**2+data['H2_PY']**2)
            pT_H3 = np.sqrt(data['H3_PX']**2+data['H3_PY']**2)

            #p1_array = [data['H1_PX'], data['H1_PY'], data['H1_PZ']]
            #p2_array = [data['H2_PX'], data['H2_PY'], data['H2_PZ']]
            #p3_array = [data['H3_PX'], data['H3_PY'], data['H3_PZ']]

            
            #invariant_mass_array.append(0)




            # This loop will go over individual events
            for i in tqdm(range(0, len(data['H1_PZ']))):
                event_counter += 1
                if 0 < MAX_EVENTS and MAX_EVENTS < event_counter:
                    break
                #if 0 == (event_counter % 100000):
                    #print('Read', event_counter, 'events')
                # Decide here which events to analyse
                if (data['H1_PZ'][i] < 0) or (data['H2_PZ'][i] < 0) or (data['H3_PZ'][i] < 0):
                    continue


                if selection:
                    probabilities_itr = [[data['H1_ProbPi'][i], data['H1_ProbK'][i]],
                                        [data['H2_ProbPi'][i], data['H2_ProbK'][i]],
                                        [data['H3_ProbPi'][i], data['H3_ProbK'][i]]]
                    charges_itr = [data['H1_Charge'][i], data['H2_Charge'][i], data['H3_Charge'][i]]
                    muon_prob = [data['H1_isMuon'][i], data['H2_isMuon'][i], data['H3_isMuon'][i]]
                
                    #check if any of the muon_prob is 1
                    if any(muon_prob):
                        continue

                    if selection_rule_iterator(probabilities_itr, charges_itr) is False:
                        continue

                    if assign_kaon_iterator(probabilities_itr, charges_itr) is False:
                        continue

                    kaon_place = assign_kaon_iterator(probabilities_itr, charges_itr)
                
                    # Your invariant mass calculation should go here
                    p1_array = [data['H1_PX'][i], data['H1_PY'][i], data['H1_PZ'][i]]
                    p2_array = [data['H2_PX'][i], data['H2_PY'][i], data['H2_PZ'][i]]
                    p3_array = [data['H3_PX'][i], data['H3_PY'][i], data['H3_PZ'][i]]
                    inv_mass = find_invariant_mass(p1_array, p2_array, p3_array, is_kaon=kaon_place)
                    invariant_mass_array.append(inv_mass)
                #invariant_mass_array.append(0)

                # Fill arrays of events to be plotted and analysed further below
                # Adding values for all three hadrons to the same variable here
                pT.append(pT_H1[i])
                pT.append(pT_H2[i])
                pT.append(pT_H3[i])
                pX.append(data['H1_PX'][i])
                pX.append(data['H2_PX'][i])
                pX.append(data['H3_PX'][i])
                pY.append(data['H1_PY'][i])
                pY.append(data['H2_PY'][i])
                pY.append(data['H3_PY'][i])
                pZ.append(data['H1_PZ'][i])
                pZ.append(data['H2_PZ'][i])
                pZ.append(data['H3_PZ'][i])

                #
                h1_probpi.append(data['H1_ProbPi'][i])
                h1_probk.append(data['H1_ProbK'][i])
                h2_probpi.append(data['H2_ProbPi'][i])
                h2_probk.append(data['H2_ProbK'][i])
                h3_probpi.append(data['H3_ProbPi'][i])
                h3_probk.append(data['H3_ProbK'][i])
                
                ##
                master_probpi.append(data['H1_ProbPi'][i])
                master_probk.append(data['H1_ProbK'][i])
                master_probpi.append(data['H2_ProbPi'][i])
                master_probk.append(data['H2_ProbK'][i])
                master_probpi.append(data['H3_ProbPi'][i])
                master_probk.append(data['H3_ProbK'][i])

    print(f"Read {event_counter:d} events")

    

    return [pT, pX, pY, pZ, (h1_probpi, h1_probk), (h2_probpi, h2_probk), (h3_probpi, h3_probk), (master_probpi, master_probk), invariant_mass_array]


if __name__ == "__main__":
    read_file()
