import numpy as np
import matplotlib.pyplot as plt
from src.binning_files import get_bins
from scipy.optimize import curve_fit
from src.distributions import fit_func_half
from src.distributions import exponential
from src.distributions import gaussian
from src.distributions import half_gaussian
from src.distributions import fit_func_triple

def attempt_fit(data, p0=[1000, 5100, 50, 1000, 5280, 50, 1000, 1000, 0]):

    values, bins, patches = plt.hist(data, bins=200, range=[5100, 5600])
    x_values, unc = get_bins(bins, values)
    plt.errorbar(x_values, values, unc, ls='None')
    

    popt, pcov = curve_fit(fit_func_triple, x_values, values, p0=p0, maxfev=2000000)

    plt.plot(x_values, fit_func_triple(x_values, *popt))
    plt.plot(x_values, exponential(x_values, popt[6], popt[7], popt[8]))
    plt.plot(x_values, gaussian(x_values, popt[3], popt[4], popt[5]))
    plt.plot(x_values, half_gaussian(x_values, popt[0], popt[1], popt[2]))

    print(popt)
    plt.show()