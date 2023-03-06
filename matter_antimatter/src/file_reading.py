import numpy as np
import uproot
from tqdm import tqdm

def read_file(path_name="", MAX_EVENTS=5000, mode=1):

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
        trees = [events_down[b'DecayTree']]
        print("Magnet down data")
        print(events_down.keys())
    elif mode == 3:
        # Magnet up data
        events_up = uproot.open(path+'B2HHH_MagnetUp.root')
        trees = [events_up['DecayTree']]
        print("Magnet up data")
        print(events_up.keys())
    elif mode == 4:
        trees = [events_down[b'DecayTree'], events_up['DecayTree']]
        print("Magnet up and down data")
        print(events_down.keys())
    else:
        print("Mode not recognised")
        return [[0], [0], [0], [0]]
    print("Varialbes read")
    print()
    for tree in tqdm(trees):
        # This outer loop is a technical loop of uproot over chunks of events
        for data in tree.iterate([b'H*_P[XYZ]', b'H*_Charge', b'H*_Prob*', b'H*_isMuon']):
            # As Python can handle calculations with arrays, we can calculate derived quantities here
            pT_H1 = np.sqrt(data[b'H1_PX']**2+data[b'H1_PY']**2)
            pT_H2 = np.sqrt(data[b'H2_PX']**2+data[b'H2_PY']**2)
            pT_H3 = np.sqrt(data[b'H3_PX']**2+data[b'H3_PY']**2)

            # Your invariant mass calculation should go here

            # This loop will go over individual events
            for i in range(0, len(data[b'H1_PZ'])):
                event_counter += 1
                if 0 < MAX_EVENTS and MAX_EVENTS < event_counter:
                    break
                if 0 == (event_counter % 100000):
                    print('Read', event_counter, 'events')
                # Decide here which events to analyse
                if (data[b'H1_PZ'][i] < 0) or (data[b'H2_PZ'][i] < 0) or (data[b'H3_PZ'][i] < 0):
                    continue
                # Fill arrays of events to be plotted and analysed further below
                # Adding values for all three hadrons to the same variable here
                pT.append(pT_H1[i])
                pT.append(pT_H2[i])
                pT.append(pT_H3[i])
                pX.append(data[b'H1_PX'][i])
                pX.append(data[b'H2_PX'][i])
                pX.append(data[b'H3_PX'][i])
                pY.append(data[b'H1_PY'][i])
                pY.append(data[b'H2_PY'][i])
                pY.append(data[b'H3_PY'][i])
                pZ.append(data[b'H1_PZ'][i])
                pZ.append(data[b'H2_PZ'][i])
                pZ.append(data[b'H3_PZ'][i])
    print(f"Read {event_counter:d} events")

    return [pT, pX, pY, pZ]


if __name__ == "__main__":
    read_file()
