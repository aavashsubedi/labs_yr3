import numpy as np
import utils.constants as const
from src.binning_files import get_bins_values
from src.binning_files import get_bins
from src.distributions import lifted_gaussian
from scipy.optimize import curve_fit



rejected_pipi = const.MASS_J_PSI
rejected_kpi = const.MASS_D0

filepath = "data/two_body_resonance.csv"



def reject_resonances(inv_mass = [[], []], mev_per_bin=17, xmin=600, xmax=3500):
    mass_pipi = inv_mass[:, 1]
    mass_kpi = inv_mass[:, 0]

    bins, values, patches, array = get_bins_values(mode="None", BINS=int(200/mev_per_bin), x_min=(rejected_kpi-100), x_max=(rejected_kpi+100),
                                                    array=mass_kpi)
    
    bin_centres = get_bins(bins, values)

    popt, pcov = curve_fit(lifted_gaussian, bin_centres, values, p0=[20000, rejected_kpi, 50, 10], maxfev=1000000)

    lower_kpi = popt[1] - popt[2]
    upper_kpi = popt[1] + popt[2]

    return popt, bin_centres, values, (lower_kpi, upper_kpi)






