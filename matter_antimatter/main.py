import uproot
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as colors

# import file_reading from src file 

from src.binning_files import get_bins

from src.dalitz_plots import variable_bins

from utils.histogram import convert_2d_hist
from src.local_asymmetry import get_Bplus_Bminus
from utils.histogram import plot2d
from src.dalitz_plots import subtract_background
from utils.histogram import use_histogram_frame
from utils.histogram import plot_frame

from matplotlib import ticker, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable



from src.fitting_inv_mass import attempt_fit

from src.local_regions import fit_region
from src.fit_muon import jpsi_fit

from src.file_reading import read_file
from src.fit_muon import asymmetry_jpsi
from utils.misc_plots import plot_comparison
from src.local_asymmetry import procedure_local_asymmetry

import mplhep as hep

hep.style.use("LHCb2")


def main():
    
    


    
    x_resolution = 600
    y_resolution = 30
    limits = [0, 27]

    procedure_local_asymmetry(x_resolution, y_resolution, limits, transpose=True)
    
    
    """
    data1 = np.genfromtxt("data/two_body_resonance_filtered_Bplus.csv", delimiter=',')
    data2 = np.genfromtxt("data/two_body_resonance_filtered_Bminus.csv", delimiter=',')
    
    # Swapping axes on dalitz plot
    data1_swap1 = data1[:, 0]
    data1_swap2 = data1[:, 1]
    data1 = np.append(np.array([data1_swap2]).T, np.array([data1_swap1]).T, axis=1)

    data2_swap1 = data2[:, 0]
    data2_swap2 = data2[:, 1]
    data2 = np.append(np.array([data2_swap2]).T, np.array([data2_swap1]).T, axis=1)
    
    inv_mass1 = np.genfromtxt("data/inv_mass_filtered_Bplus.csv", delimiter=',')
    inv_mass2 = np.genfromtxt("data/inv_mass_filtered_Bminus.csv", delimiter=',')
    data = np.append(data1, data2, axis=0)
    inv_mass = np.append(inv_mass1, inv_mass2)
    popt_all, popt_Bplus, popt_Bminus = attempt_fit()
    popt_exp = [popt_all[9], popt_all[8], popt_all[10], popt_all[11]]

    subtract_background(popt_exp , inv_mass_all=inv_mass, two_body_all=data, )
    """

    return None

if __name__ == "__main__":
    main()