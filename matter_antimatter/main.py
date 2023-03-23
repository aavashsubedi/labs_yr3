import uproot
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as colors
from scipy.optimize import curve_fit
# import file_reading from src file 
from src.file_reading import read_file
from src.fitting_functions import fit_data
from utils.printing_results import print_results
from utils.plotting_functions import default_plot
from src.Task1_plot_prob import plotting_histograms_probability
from src.two_body_resonance import iterate_events
from src.reject_resonances import fit_resonances
from src.distributions import lifted_gaussian
from src.reject_resonances import iterate_reject
from src.binning_files import get_bins
from src.distributions import fit_func_half
from src.distributions import exponential
from src.distributions import gaussian
from src.distributions import half_gaussian




def main():
    
    # Read data
    #args = read_file(MAX_EVENTS=50000, mode=4, path_name="", selection=True)
    #two_body = iterate_events(args)
    """
    two_body = np.genfromtxt("data/two_body_resonance.csv", delimiter=',')
    new_two_body = iterate_reject( two_body_masses=two_body)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    ax[0].hist(new_two_body[:, 0], bins=200, range=[600, 4000], label='$K + pion$')
    ax[0].hist(two_body[:, 0], bins=200, range=[600, 4000], histtype='step', label='$K + pion$')
    ax[1].hist(new_two_body[:, 1], bins=200, range=[600, 4000], label='$pion + pion$')
    ax[1].hist(two_body[:, 1], bins=200, range=[600, 4000], histtype='step', label='$pion + pion$')
    plt.show()
    """
    
    #np.savetxt("data/inv_mass.csv", inv_mass, delimiter=',')
    #print(inv_mass)
    #plotting_histograms_probability(master_prob[0], master_prob[1], savefig_name="small_sel")
    """
    resolution = 1700
    range_resonance = [600, 4000]
    mev_per_bin = int((range_resonance[1] - range_resonance[0]) / resolution)

    
    two_body = np.genfromtxt("data/two_body_resonance.csv", delimiter=',')
    popt, x_values, x_values_pipi, y_values, y_values_pipi, kpi_limits, pipi_limits, unc = fit_resonances(two_body, sigma=3, mev_per_bin=mev_per_bin)


    print(popt)

    two_body = np.array(two_body)
    new_two_body, new_inv_mass = iterate_reject(inv_mass_3body=inv_mass, two_body_masses=two_body, sigma=3, mev_per_bin=mev_per_bin)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    ax[0].hist(two_body[:, 0], bins=resolution, range=range_resonance, histtype='step', label='$K + pion$')
    ax[0].plot(x_values, lifted_gaussian(x_values, *popt[0]))
    #ax[0].plot(x_values, y_values)
    ax[0].plot(np.full(10, kpi_limits[0]), np.linspace(0, np.max(y_values), 10), color='r', linestyle='dashed')
    ax[0].plot(np.full(10, kpi_limits[1]), np.linspace(0, np.max(y_values), 10), color='r', linestyle='dashed')
    ax[1].hist(two_body[:, 1], bins=resolution, range=range_resonance, histtype='step', label='$pion + pion$') 
    ax[1].plot(x_values_pipi, lifted_gaussian(x_values_pipi, *popt[1]))
    ax[1].plot(np.full(10, pipi_limits[0]), np.linspace(0, np.max(y_values_pipi), 10), color='r', linestyle='dashed')
    ax[1].plot(np.full(10, pipi_limits[1]), np.linspace(0, np.max(y_values_pipi), 10), color='r', linestyle='dashed')
    #ax[1].plot(x_values_pipi, y_values_pipi)

    
    values_kpi, bins_kpi, patches_kpi = ax[0].hist(new_two_body[:, 0], bins=resolution, range=range_resonance, label='$K + pion$')
    x_kpi, sigma_kpi = get_bins(bins_kpi, values_kpi)
    ax[0].errorbar(x_values, y_values, unc[0], ls='None')
    ax[1].errorbar(x_values_pipi, y_values_pipi, unc[1], ls='None')
    ax[0].errorbar(x_kpi, values_kpi, yerr=np.abs(sigma_kpi), ls='None')
    values_pipi, bins_pipi, patches_pipi = ax[1].hist(new_two_body[:, 1], bins=resolution, range=range_resonance, label='$pion + pion$')
    x_pipi, sigma_pipi = get_bins(bins_pipi, values_pipi)
    #ax[1].errorbar(x_pipi, values_pipi, yerr=np.abs(sigma_pipi), ls='None')
    
    plt.show()
    """

    data_Bminus = np.genfromtxt("data/inv_mass_filtered_all_Bminus.csv", delimiter =' ')
    values, bins, patches = plt.hist(data_Bminus, bins=200, range=[5100, 5600])
    x_values, unc = get_bins(bins, values)
    plt.errorbar(x_values, values, unc, ls='None')
    

    popt, pcov = curve_fit(fit_func_half, x_values, values, p0=[1000, 5100, 50, 1000, 5280, 50, 1000, 1000, 10])

    plt.plot(x_values, fit_func_half(x_values, *popt))
    plt.plot(x_values, exponential(x_values, popt[6], popt[7], popt[8]))
    plt.plot(x_values, gaussian(x_values, popt[3], popt[4], popt[5]))
    plt.plot(x_values, half_gaussian(x_values, popt[0], popt[1], popt[2]))

    print(popt)
    plt.show()
    
    #np.savetxt("data/two_body_resonance_filtered.csv", new_two_body, delimiter=',')
    

    return None

if __name__ == "__main__":
    main()