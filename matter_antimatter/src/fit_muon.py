import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from src.binning_files import get_bins
from scipy.stats import norm
from scipy.stats import crystalball
from src.distributions import chi_squared

def scaled_norm(x, mean, sigma, scale, const, slope):
    return (norm.pdf(x, mean, sigma) * scale + const + np.multiply(x, slope))

def scaled_crystal(x, beta, m, loc, scale, norm):
    return crystalball.pdf(x, beta, m, loc, scale) * norm



def jpsi_fit(filepath="data/Bplus_muon.csv"):
    data = np.genfromtxt(filepath, delimiter=',')
    hist_values, x_bins, image = plt.hist(data, 100, range=[3050, 3150])
    plt.cla()
    x_centres, unc = get_bins(x_bins, hist_values)
    p0 = [3100, 1, 1000, 10, -1000]
    #p0 = [1, 1, 3100, 50, 1000]

    popt, pcov = curve_fit( scaled_norm, x_centres, hist_values, p0, unc, absolute_sigma=True, maxfev=10000)
    plt.errorbar(x_centres, hist_values, unc, ls='None')
    plt.plot(x_centres, scaled_norm(x_centres, *popt))
    print(popt)

    chi_sq = chi_squared(hist_values, scaled_norm(x_centres, *popt), unc, 4)
    print("Chi^2 is: {}".format(chi_sq))

    plt.show()
    return popt

def asymmetry_jpsi():
    Bplus_popt = jpsi_fit()
    Bminus_popt = jpsi_fit("data/Bminus_muon.csv")

    