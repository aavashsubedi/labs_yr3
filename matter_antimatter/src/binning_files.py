from matplotlib import pyplot as plt
import numpy as np



def get_bins(data, values):
    bin_centers = [(a+b)/2 for a,b in zip(data[0:-1],data[1:]) ]
    return bin_centers

def get_bins_values(mode="B+", BINS=100, x_min=5100, x_max=5800):

    if mode == "B+":
        dataset = np.genfromtxt('/workspaces/labs_yr3/matter_antimatter/data/inv_mass_positive.csv', delimiter=',')
    elif mode == "B-":
        dataset = np.genfromtxt('/workspaces/labs_yr3/matter_antimatter/data/inv_mass_negative.csv', delimiter=',')

    else:
        dataset = np.genfromtxt('/workspaces/labs_yr3/matter_antimatter/data/inv_mass.csv', delimiter=',')
    #x_data = np.linspace(x_min, x_max, BINS)
    invariant_mass_numpy = np.array(dataset)
    invariant_mass_numpy = np.where((
        invariant_mass_numpy > x_min) & (
        invariant_mass_numpy < x_max), invariant_mass_numpy, np.nan)
    values, bins, patches = plt.hist(invariant_mass_numpy, bins=BIN_NUM);
    plt.close()
    return bins, values, patches, invariant_mass_numpy

