import numpy as np
import matplotlib.pyplot as plt

from src.binning_files import get_bins

from scipy.optimize import curve_fit
from src.distributions import crystal_fitted
from iminuit import cost
from iminuit import Minuit

from src.distributions import chi_squared

from scipy.stats import expon
from scipy.stats import halfnorm
from scipy.stats import crystalball

def get_events(mass_kpi, mass_pipi, inv_mass, limits_kpi=[0, 3872], limits_pipi=[282, 812]):

    events_inv_mass = []
    events_kpi = []
    events_pipi = []

    for iterator in range(0, len(mass_pipi)):
        if mass_pipi[iterator] > limits_pipi[0] and mass_pipi[iterator] < limits_pipi[1]:
            if mass_kpi[iterator] > limits_kpi[0] and mass_kpi[iterator] < limits_kpi[1]:
                events_inv_mass.append(inv_mass[iterator])
                events_kpi.append(mass_kpi[iterator])
                events_pipi.append(mass_pipi[iterator])

    return events_inv_mass

def fit_region(mass_kpi, mass_pipi, inv_mass, limits_kpi=[0, 3872], limits_pipi=[282, 812]):

    events_inv_mass = get_events(mass_kpi, mass_pipi, inv_mass, limits_kpi, limits_pipi)
    print(len(events_inv_mass))
    hist_values, bins_x, image = plt.hist(events_inv_mass, bins=50, range=[5100, 5600])
    x_centres, unc = get_bins(bins_x, hist_values)

    result = np.append(np.array([hist_values]).T, np.array([x_centres]).T, axis=1)
    result = np.append(result, np.array([unc]).T, axis=1)
    np.savetxt("data/region_local_Bminus.csv", events_inv_mass, delimiter=',')
    plt.show()

    p0 = [0.2, 3, 5.283e+3, 9.9, 2, 4617, 165, 1146, 728, 1991, 4553, 1228]
    popt, pcov = curve_fit(crystal_fitted, x_centres, hist_values, p0, unc, absolute_sigma=True, maxfev=10000)
    #popt, pcov = curve_fit(crystal_fitted, x_centres, hist_values, p0, maxfev=10000)
    print(popt)
    c = cost.ExtendedUnbinnedNLL(x_centres, crystal_fitted)
    m = Minuit(c, *p0)
    


    #popt[0] = 0.21089
    #popt[1] = 3.00469
    #popt[4] = 0.501267
    #popt[6] = 169.4387
    plt.errorbar(x_centres, hist_values, unc, ls='None', capsize=2, label="Data")
    plt.plot(x_centres, crystal_fitted(x_centres, *popt), label="Fit")
    plt.plot(x_centres, expon.pdf(x_centres, popt[9], popt[8]) * popt[10] * popt[11], label="Comb back", ls='--')
    plt.plot(x_centres, halfnorm.pdf(x_centres, popt[5], popt[6]) * popt[7] * popt[11], label="Part reconstr", ls='--' )
    plt.plot(x_centres, crystalball.pdf(x_centres, popt[0], popt[1], popt[2], popt[3]) * popt[4] * popt[11], label="Signal", ls='--')
    plt.legend()
    
    print(chi_squared(hist_values, crystal_fitted(x_centres, *popt), unc, 10))
    plt.title("$B^-$ in region of interest")
    plt.xlabel("Invariant mass (MeV)")
    plt.ylabel("Counts per 10 MeV")
    plt.savefig("plots/region_Bminus.png", dpi=600)
    plt.show()
    print(popt)

    




