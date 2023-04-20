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

from matplotlib import ticker, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable



from src.fitting_inv_mass import attempt_fit

from src.local_regions import fit_region
from src.fit_muon import jpsi_fit


def main():
    
    


    #popt_all, popt_Bplus, popt_Bminus = attempt_fit()

    
    
    #procedure to get local asymmetry
    x_resolution = 300
    y_resolution = 20
    limits = [0, 27]


    data1 = np.genfromtxt("data/two_body_resonance_filtered_Bplus.csv", delimiter=',')
    data2 = np.genfromtxt("data/two_body_resonance_filtered_Bminus.csv", delimiter=',')
    """
    # Swapping axes on dalitz plot
    data1_swap1 = data1[:, 0]
    data1_swap2 = data1[:, 1]
    data1 = np.append(np.array([data1_swap2]).T, np.array([data1_swap1]).T, axis=1)

    data2_swap1 = data2[:, 0]
    data2_swap2 = data2[:, 1]
    data2 = np.append(np.array([data2_swap2]).T, np.array([data2_swap1]).T, axis=1)
    """
    inv_mass1 = np.genfromtxt("data/inv_mass_filtered_Bplus.csv", delimiter=',')
    inv_mass2 = np.genfromtxt("data/inv_mass_filtered_Bminus.csv", delimiter=',')
    data = np.append(data1, data2, axis=0)
    inv_mass = np.append(inv_mass1, inv_mass2)

    #get data for specific region
    fit_region(data1[:, 0], data1[:, 1], inv_mass1)
    

    """
    # xoffset, tau, exp_norm, total_norm
    popt_exp = [popt_all[9], popt_all[8], popt_all[10], popt_all[11]]
    dalitz_values, dalitz_x_bins, dalitz_y_bins = subtract_background(popt=popt_exp, inv_mass_all=inv_mass, two_body_all=data, bins=[x_resolution,y_resolution], transpose=True, limits=limits)
    
    
    values, bins_x, bins_y = variable_bins(dalitz_values, dalitz_x_bins, dalitz_y_bins, resolution_x=x_resolution, resolution_y=y_resolution)
    hist_values, hist_x, hist_y = convert_2d_hist(values, bins_x, bins_y, x_resolution=x_resolution)
    print(np.max(hist_values))




    axes, image = plot2d(hist_values, hist_x, hist_y)
    plt.colorbar(image)
    plt.show()

    
    popt_Bplus_exp = [popt_Bplus[9], popt_Bplus[8], popt_Bplus[10], popt_Bplus[11]]
    popt_Bminus_exp = [popt_Bminus[9], popt_Bminus[8], popt_Bminus[10], popt_Bminus[11]]
    data_Bplus, x, y = subtract_background(popt=popt_Bplus_exp, inv_mass_all=inv_mass1, two_body_all=data1, bins=[x_resolution,y_resolution], transpose=True, limits=limits)
    data_Bminus, x, y = subtract_background(popt=popt_Bminus_exp, inv_mass_all=inv_mass2, two_body_all=data2, bins=[x_resolution,y_resolution], transpose=True, limits=limits)

    
    get_Bplus_Bminus(data_Bplus, data_Bminus, bins_x, bins_y, x_resolution, y_resolution, limits_x=limits)
    """

    return None

if __name__ == "__main__":
    main()