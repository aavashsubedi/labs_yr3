from matplotlib import pyplot as plt
import numpy as np



def get_bins(data, values=0):
    bin_centers = [(a+b)/2 for a,b in zip(data[0:-1],data[1:]) ]
    bin_widths = [(b-a) for a,b in zip(data[0:-1], data[1:])]
    
    uncertainties = np.sqrt(values)
    #print (uncertainties)
    return bin_centers, uncertainties

def get_bins_values(mode="B+", BINS=100, x_min=5100, x_max=5800, array=None,
                    path_name='/workspaces/labs_yr3/matter_antimatter/data/inv_mass.csv'):

    if array.any() != None:
        dataset = array
    else:
        if mode == "B+":
            dataset = np.genfromtxt('/workspaces/labs_yr3/matter_antimatter/data/inv_mass_positive.csv', delimiter=',')
        elif mode == "B-":
            dataset = np.genfromtxt('/workspaces/labs_yr3/matter_antimatter/data/inv_mass_negative.csv', delimiter=',')

        else:
            try:
                dataset = np.genfromtxt(path_name, delimiter=',')
            except:
                print("No file found")
                return 0, 0, 0, 0
    #x_data = np.linspace(x_min, x_max, BINS)
    invariant_mass_numpy = np.array(dataset)
    invariant_mass_numpy = np.where((
        invariant_mass_numpy > x_min) & (
        invariant_mass_numpy < x_max), invariant_mass_numpy, np.nan)
    values, bins, patches = plt.hist(invariant_mass_numpy, bins=BINS);
    plt.close()
    return bins, values, patches, invariant_mass_numpy

