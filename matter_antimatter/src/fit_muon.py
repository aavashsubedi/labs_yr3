import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from src.binning_files import get_bins

def jpsi_fit():
    data = np.genfromtxt("data/Bplus_muon.csv", delimiter=',')
    hist_values, x_bins, image = plt.hist(data, 100, range=[3000, 3200])
    x_centres, unc = get_bins(x_bins, hist_values)
    p0 = [3100, 1, 1000]
    
    plt.show()