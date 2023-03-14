import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from src.distributions import gaussian, exponential, constant, half_gaussian
from src.distributions import fit_func, fit_func_half
from src.binning_files import get_bins_values, get_bins

def clean_data(y_data, y_other):

    for y_indivual in y_other:
        y_data = y_data - y_indivual
    
    return y_data

def seperate_background_signal(path_name ='/workspaces/labs_yr3/inv_mass.csv',
                                bin_num=100, x_min=5100, x_max=5800, expected_resonance=5271,
                                init_vals=[1000, 5100, 5, 1000, 5300, 10, 10, 5, 5100 ],
                                fit_func="default"):
    """
    Seperates the background and signal from the data
    using the defaulf parameters for the half gaussian fitting.
    Defaults to entire dataset.
    
    """
    #read file
    #dataset = np.genfromtxt(path_name, delimiter=',')

    BIN_NUM = bin_num
    np.random.seed(42)
    bins, values, patches, array = get_bins_values(mode="None", BINS=bin_num, x_min=5100, x_max=5800,
                                                    path_name=path_name)

    popt, pcov = curve_fit(fit_func_half, get_bins(bins, values), values,
                        p0 = init_vals,
                        maxfev=1000000)
    
    x_data = np.linspace(x_min, x_max, 100)

    y_data = fit_func_half(x_data, popt[0], popt[1], popt[2],
                        popt[3], popt[4], popt[5],
                        popt[6], popt[7], popt[8])

    y_plot_1_diff = np.abs(expected_resonance - popt[1])
    y_plot_2_diff = np.abs(expected_resonance - popt[4])

    
    y_plot_1 = half_gaussian(x_data, popt[0], popt[1], popt[2])
    y_plot_2 = gaussian(x_data, popt[3], popt[4], popt[5])
    y_plot_3 = exponential(x_data, popt[6], popt[7], popt[8])
    if abs(y_plot_1_diff) < abs(y_plot_2_diff):
        other_dataaset = [y_plot_2, y_plot_3]
    else:
        other_dataaset = [y_plot_1, y_plot_3]


    y_signal = clean_data(y_data, other_dataaset)
    y_background = clean_data(y_data, [y_signal])


    return y_signal, y_background


