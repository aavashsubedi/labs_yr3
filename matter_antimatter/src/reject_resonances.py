import numpy as np
import utils.constants as const
from src.binning_files import get_bins_values
from src.binning_files import get_bins
from src.distributions import lifted_gaussian
from scipy.optimize import curve_fit
from tqdm import tqdm
from src.two_body_resonance import append_args



rejected_pipi = const.MASS_J_PSI
rejected_kpi = const.MASS_D0

filepath = "data/two_body_resonance.csv"



def fit_resonances(inv_mass = [[], []], mev_per_bin=17, sigma=2):
    mass_pipi = inv_mass[:, 1]
    mass_kpi = inv_mass[:, 0]
    cutoff_kpi = 100
    cutoff_pipi = 150

    bins, values, patches, array = get_bins_values(mode="None", BINS=int(cutoff_kpi*2/mev_per_bin), x_min=(rejected_kpi-cutoff_kpi),
                                                   x_max=(rejected_kpi+cutoff_kpi), array=mass_kpi)
    bins_pipi, values_pipi, patches_pipi, array_pipi = get_bins_values(mode="None", BINS=int(cutoff_pipi*2/mev_per_bin), x_min=(rejected_pipi -cutoff_pipi),
                                                                       x_max=(rejected_pipi + cutoff_pipi), array=mass_pipi)
    
    bin_centres, unc_kpi = get_bins(bins, values)
    bin_centres_pipi, unc_pipi = get_bins(bins_pipi, values_pipi)

    popt, pcov = curve_fit(lifted_gaussian, bin_centres, values, p0=[20000, rejected_kpi, 50, 10], maxfev=1000000)
    popt_pipi, pcov_pipi = curve_fit(lifted_gaussian, bin_centres_pipi, values_pipi, p0=[20000, rejected_pipi, 50, 10], maxfev=1000000)

    lower_kpi = popt[1] - np.abs(sigma * popt[2])
    upper_kpi = popt[1] + np.abs(sigma * popt[2])

    lower_pipi = popt_pipi[1] - sigma * popt_pipi[2]
    upper_pipi = popt_pipi[1] + sigma * popt_pipi[2]

    return (popt, popt_pipi), bin_centres, bin_centres_pipi, values, values_pipi, (lower_kpi, upper_kpi), (lower_pipi, upper_pipi), (unc_kpi, unc_pipi)


def iterate_reject(inv_mass_3body, two_body_masses=[[], []], two_body_signal=[[], []], mev_per_bin=17, sigma=2):
    """fits the two body resonances on the signal only and rejects around 2 sigma on all data

    Parameters
    ----------
    inv_mass_3body : array float
        all data invariant mass
    two_body_masses : list, optional
        all data resonance, by default [[], []]
    two_body_signal : list, optional
        signal only resonance for fitting, by default [[], []]
    mev_per_bin : int, optional
        resolution in MeV per bin, by default 17
    sigma : int, optional
        cutoff standard deviation, by default 2

    Returns
    -------
    list, list
        filtered inv masses and two body resonances of all data
    """
    new_inv_mass = []
    new_two_body = [[-1, -1]]

    popt, x_kpi, x_pipi, y_kpi, y_pipi, limits_kpi, limits_pipi, unc = fit_resonances(two_body_signal, mev_per_bin=mev_per_bin, sigma=sigma)
    mass_pipi = two_body_masses[:, 1]
    mass_kpi = two_body_masses[:, 0]
    #print(limits_kpi)
    print("Iterating and rejecting D0 and J/psi events:")
    for event_iterator in tqdm(range(0, len(mass_kpi))):
        if mass_kpi[event_iterator] > limits_kpi[0] and mass_kpi[event_iterator] < limits_kpi[1]:
            
            continue
        if mass_pipi[event_iterator] > limits_pipi[0] and mass_pipi[event_iterator] < limits_pipi[1]:
            
            continue
        #if mass_pipi[event_iterator] > limits_kpi[0] and mass_pipi[event_iterator] < limits_kpi[1]:
            #continue
    
    #new_args = append_args(event_iterator, args, new_args)
        new_two_body = np.append(new_two_body, [two_body_masses[event_iterator, :]], axis=0)
        new_inv_mass.append(inv_mass_3body[event_iterator])
    new_two_body = np.delete(new_two_body, 0, axis=0)
    

    return new_two_body, new_inv_mass









