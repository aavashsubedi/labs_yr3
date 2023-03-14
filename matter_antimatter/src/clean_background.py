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

def seperate_background_signal(path_name ='data/inv_mass.csv',
                                bin_num=100, x_min=5100, x_max=5800, expected_resonance=5271,
                                init_vals=[1000, 5100, 5, 1000, 5300, 10, 10, 5, 5100 ],
                                fit_func="default"):
    """
    Seperates the background and signal from the data
    using the defaulf parameters for the half gaussian fitting.
    Defaults to entire dataset.

    Parameters
    ----------
    path_name : str, optional
        Path to the data file, by default '/workspaces/labs_yr3/inv_mass.csv'
    bin_num : int, optional
        Number of bins to use, by default 100
    x_min : int, optional
        Minimum x value to use, by default 5100
    x_max : int, optional
        Maximum x value to use, by default 5800
    expected_resonance : int, optional
        Expected resonance value, by default 5271. Used to check which is the background
    init_vals : list, optional
        Initial values for the fitting, by default [1000, 5100, 5, 1000, 5300, 10, 10, 5, 5100 ]
    fit_func : str, optional
        Which fitting function to use, by default "default"
    

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

    y_plot_1 = half_gaussian(x_data, popt[0], popt[1], popt[2])
    y_plot_2 = gaussian(x_data, popt[3], popt[4], popt[5])
    y_plot_3 = exponential(x_data, popt[6], popt[7], popt[8])

    other_dataset = [y_plot_1, y_plot_3]

    y_signal = clean_data(y_data, other_dataset)
    y_background = clean_data(y_data, [y_signal])


    return popt, y_signal, y_background


