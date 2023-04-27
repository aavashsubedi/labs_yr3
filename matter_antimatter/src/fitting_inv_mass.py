import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from src.distributions import crystal_fitted
from src.distributions import chi_squared

from scipy.stats import expon
from scipy.stats import halfnorm
from scipy.stats import crystalball


def attempt_fit():
    #optimal parameters: beta, m, loc, scale, c_norm, comb_mu, comb_sigma, comb_n, tau, xoffset, exp_norm, total_norm
    #                    |         crystalball      |       half norm            |      expon            |

    popt_all = [1.148e+0, 3.825e+0, 5.284e+3, 2.006e+1, 8.429e+2, 5.096e+3, 4.199e+1, 5.737e+2, 5.297e+3, 1.692e+3, 7.917e+3, 2.140e+2]
    popt_Bplus = [1.359e+0, 1.713e+0, 5.283e+3, 2.089e+1, 4.282e+2, 5.101e+3, 3.784e+1, 2.309e+2, 4.764e+3, 1.801e+3, 5.343e+3, 2.306e+2]
    popt_Bminus = [1.079e+0, 5.191e+0, 5.284e+3, 1.936e+1, 5.238e+2, 5.091e+3, 4.458e+1, 3.999e+2, 1.615e+3, 1.618e+3, 5.765e+3, 1.682e+2]

    inv_mass1 = np.genfromtxt("data/inv_mass_filtered_Bplus.csv", delimiter=',')
    inv_mass2 = np.genfromtxt("data/inv_mass_filtered_Bminus.csv", delimiter=',')
    inv_mass = np.append(inv_mass1, inv_mass2)

    x_sample = np.linspace(5100, 5600, 100)
    y_all, bins_x, im1 = plt.hist(inv_mass, bins=100, range=[5100, 5600])
    y_Bplus, bins_x, im2 = plt.hist(inv_mass1, bins=100, range=[5100, 5600])
    y_Bminus, bins_x, im3 = plt.hist(inv_mass2, bins=100, range=[5100, 5600])
    plt.clf()

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(27, 9))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    
    err_y_all = np.sqrt(y_all)
    popt_all_new, pcov = curve_fit(crystal_fitted, x_sample, y_all, p0=popt_all, sigma=err_y_all, absolute_sigma=True)
    chi_all = chi_squared(y_all, crystal_fitted(x_sample, *popt_all_new), err_y_all, len(popt_all_new))
    print(chi_all)

    ax[0].plot(x_sample, crystal_fitted(x_sample, *popt_all_new), label="Fit")
    ax[0].errorbar(x_sample, y_all, err_y_all, ls='None', capsize=4, label="Data")
    ax[0].plot(x_sample, expon.pdf(x_sample, popt_all_new[9], popt_all_new[8]) * popt_all_new[10] * popt_all_new[11], label="Combinatorial", ls='--')
    ax[0].plot(x_sample, halfnorm.pdf(x_sample, popt_all_new[5], popt_all_new[6]) * popt_all_new[7] * popt_all_new[11], label=r"B$\rightarrow$4 body", ls='--' )
    ax[0].plot(x_sample, crystalball.pdf(x_sample, popt_all_new[0], popt_all_new[1], popt_all_new[2], popt_all_new[3]) * popt_all_new[4] * popt_all_new[11], label="Signal", ls='--')
    ax[0].legend(fontsize=18)
    
    
    err_y_Bplus = np.sqrt(y_Bplus)
    popt_Bplus_new, pcov = curve_fit(crystal_fitted, x_sample, y_Bplus, p0=popt_Bplus, sigma=err_y_Bplus, absolute_sigma=True)
    chi_Bplus = chi_squared(y_Bplus, crystal_fitted(x_sample, *popt_Bplus_new), err_y_Bplus, len(popt_Bplus_new))
    print(chi_Bplus)

    ax[1].plot(x_sample, crystal_fitted(x_sample, *popt_Bplus_new), label="Fit")
    ax[1].errorbar(x_sample, y_Bplus, err_y_Bplus, ls='None', capsize=4, label="Data")
    ax[1].plot(x_sample, expon.pdf(x_sample, popt_Bplus_new[9], popt_Bplus_new[8]) * popt_Bplus_new[10] * popt_Bplus_new[11], label="Combinatorial", ls='--')
    ax[1].plot(x_sample, halfnorm.pdf(x_sample, popt_Bplus_new[5], popt_Bplus_new[6]) * popt_Bplus_new[7] * popt_Bplus_new[11], label=r"B$\rightarrow$4 body", ls='--' )
    ax[1].plot(x_sample, crystalball.pdf(x_sample, popt_Bplus_new[0], popt_Bplus_new[1], popt_Bplus_new[2], popt_Bplus_new[3]) * popt_Bplus_new[4] * popt_Bplus_new[11], label="Signal", ls='--')
    ax[1].legend(fontsize=18)

    err_y_Bminus = np.sqrt(y_Bminus)
    popt_Bminus_new, pcov = curve_fit(crystal_fitted, x_sample, y_Bminus, p0=popt_Bminus, sigma=err_y_Bminus, absolute_sigma=True)
    chi_Bminus = chi_squared(y_Bminus, crystal_fitted(x_sample, *popt_Bminus_new), err_y_Bminus, len(popt_Bminus_new))
    print(chi_Bminus)

    ax[2].plot(x_sample, crystal_fitted(x_sample, *popt_Bminus_new), label="Fit")
    ax[2].errorbar(x_sample, y_Bminus, err_y_Bminus, ls='None', capsize=4, label="Data")
    ax[2].plot(x_sample, expon.pdf(x_sample, popt_Bminus_new[9], popt_Bminus_new[8]) * popt_Bminus_new[10] * popt_Bminus_new[11], label="Combinatorial", ls='--')
    ax[2].plot(x_sample, halfnorm.pdf(x_sample, popt_Bminus_new[5], popt_Bminus_new[6]) * popt_Bminus_new[7] * popt_Bminus_new[11], label=r"B$\rightarrow$4 body", ls='--' )
    ax[2].plot(x_sample, crystalball.pdf(x_sample, popt_Bminus_new[0], popt_Bminus_new[1], popt_Bminus_new[2], popt_Bminus_new[3]) * popt_Bminus_new[4] * popt_Bminus_new[11], label="Signal", ls='--')
    ax[2].legend(fontsize=18)

    ax[0].set_title("Invariant mass all events")
    ax[1].set_title("Invariant mass $B^{+}$")
    ax[2].set_title("Invariant mass $B^{-}$")

    ax[0].set_xlabel("Invariant mass (MeV)", fontsize=18)
    ax[0].set_ylabel("Counts / 5 MeV", fontsize=18)
    ax[1].set_xlabel("Invariant mass (MeV)", fontsize=18)
    ax[1].set_ylabel("Counts / 5 MeV", fontsize=18)
    ax[2].set_xlabel("Invariant mass (MeV)", fontsize=18)
    ax[2].set_ylabel("Counts / 5 MeV", fontsize=18)


    fig.savefig("plots/fits_invariant_mass_100bins.png")
    plt.show()

    return popt_all_new, popt_Bplus_new, popt_Bminus_new