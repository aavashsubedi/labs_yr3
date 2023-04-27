import numpy as np
import matplotlib.pyplot as plt
from utils.histogram import use_histogram_frame
from src.binning_files import get_bins
from utils.histogram import plot_frame
from utils.histogram import plot2d


from scipy.optimize import curve_fit
from src.distributions import norm_fitted
from src.distributions import chi_squared

from src.fitting_inv_mass import attempt_fit
from src.dalitz_plots import subtract_background
from src.dalitz_plots import variable_bins
from utils.histogram import convert_2d_hist


def local_asymmetry( Bplus_data = [], Bminus_data = [], x_resolution=200, y_resolution=50 ):
    weigths_Bplus = Bplus_data
    weigths_Bminus = Bminus_data

    #print(weigths_Bplus[10, 20], weigths_Bminus[10, 20])

    all_events = np.sum(weigths_Bplus) + np.sum(weigths_Bminus)

    

    asymmetry = (weigths_Bminus - weigths_Bplus) / (weigths_Bplus + weigths_Bminus)
    asymmetry = np.where(np.isnan(asymmetry), np.full(np.shape(asymmetry), np.nan), asymmetry)
    #print(asymmetry[10, 20])

    sum = (weigths_Bplus + weigths_Bminus)
    difference = (weigths_Bminus - weigths_Bplus)

    #sigma_Bplus = np.sqrt(weigths_Bplus * (1 - weigths_Bplus / (all_events)))
    #sigma_Bminus = np.sqrt(weigths_Bminus * (1 - weigths_Bminus / (all_events)))
    sigma_Bplus = np.sqrt(weigths_Bplus)
    sigma_Bminus = np.sqrt(weigths_Bminus)
    #print(np.max(sigma_Bplus))
    #print(np.min(sum))

    sigma_sum  = np.sqrt(sigma_Bminus**2 + sigma_Bplus**2)
    #print(np.max(sigma_sum))
    #sigma_diff = sigma_sum

    #sigma_asymmetry =  np.sqrt( (sigma_sum * difference)**2 + (sigma_sum / sum)**2 )
    sigma_asymmetry = np.sqrt( (1 - asymmetry**2) / sum )
    #sigma_asymmetry = np.sqrt((np.square(asymmetry) + np.square(np.square(asymmetry))) / sum) 
    sigma_asymmetry = np.where(np.isinf(sigma_asymmetry), np.full(np.shape(sigma_asymmetry), np.nan), sigma_asymmetry)
    sigma_asymmetry = np.where(np.isnan(sigma_asymmetry), np.full(np.shape(sigma_asymmetry), np.nan), sigma_asymmetry)
    #print(sigma_asymmetry[10, 20])

    significance = (asymmetry/sigma_asymmetry)
    #significance = np.where(significance > 5 , significance, np.full(np.shape(significance), np.nan)) #cut siginificant only
    
    #plt.contourf(x_centres_Bplus, y_centres_Bplus, asymmetry, levels=[-1.0, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 0.75, 1.0], corner_mask=False)
    #plt.hist2d(x_centres_Bplus, y_centres_Bplus, bins=[x_resolution, y_resolution], weights=asymmetry)
    
    #plot2d(asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[0])

    #plt.colorbar()
    

    #plot2d(sigma_asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[1])
    

    return asymmetry, sigma_asymmetry, significance

def get_Bplus_Bminus(data_Bplus, data_Bminus, x_bins_edges, y_bins_edges,x_resolution=200, y_resolution=50, limits_x=[0, 20]):
    
    new_values_Bplus, x_bins_Bplus, y_bins_Bplus, Bplus_flat = use_histogram_frame(data_Bplus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)
    new_values_Bminus, x_bins_Bminus, y_bins_Bminus, Bminus_flat = use_histogram_frame(data_Bminus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)
    print(np.max(new_values_Bminus), np.max(new_values_Bplus))

    #x_centres_Bplus, unc = get_bins(x_bins_Bplus, new_values_Bplus)
    x_centres_Bplus = x_bins_Bplus
    y_centres_Bplus, unc_Bplus = get_bins(y_bins_Bplus, new_values_Bplus)
    y_centres_Bplus = y_bins_Bplus #no idea why but this is correct

    #x_centres_Bminus, unc = get_bins(x_bins_Bminus, new_values_Bminus)
    x_centres_Bminus = x_bins_Bminus
    y_centres_Bminus, unc_Bminus = get_bins(y_bins_Bminus, new_values_Bminus)

    
    
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    #plot_frame(x_bins_edges[1:], y_bins_edges[1:], x_resolution, limits_x, ax[0])
    #local_asymmetry([x_centres_Bplus, y_centres_Bplus, new_values_Bplus], [x_centres_Bminus, y_centres_Bminus, new_values_Bminus], x_resolution, y_resolution)
    asymmetry, sigma_asymmetry, significance= local_asymmetry(new_values_Bplus, new_values_Bminus, x_resolution, y_resolution)
    asymmetry_flat, sigma_flat, significance_flat = local_asymmetry(Bplus_flat, Bminus_flat, x_resolution, y_resolution)
    axes, image1 = plot2d(asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[0])
    axes, image2 = plot2d(sigma_asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[1])
    axes, image3 = plot2d(significance, x_centres_Bplus, y_centres_Bplus, ax=ax[2])
    fig.colorbar(image1, cax=None, ax=ax[0])
    fig.colorbar(image2, cax=None, ax=ax[1])
    fig.colorbar(image3, cax=None, ax=ax[2])
    ax[0].set_xlabel("$m^{2}_{\pi \pi} GeV^2$", fontsize=30)
    ax[0].set_ylabel("$m^{2}_{K \pi} GeV^2$", fontsize=30)
    ax[0].set_title("Local asymmetry")

    ax[1].set_xlabel("$m^{2}_{\pi \pi} GeV^2$", fontsize=30)
    ax[1].set_ylabel("$m^{2}_{K \pi} GeV^2$", fontsize=30)
    ax[1].set_title("Local asymmetry uncertainty")

    ax[2].set_xlabel("$m^{2}_{\pi \pi} $", fontsize=30)
    ax[2].set_ylabel("$m^{2}_{K \pi} $", fontsize=30)
    ax[2].set_title("Local asymmetry significance")
    fig.savefig("plots/local_asymmetry_600x30_transpose.png")
    plt.show()
    
    significance = np.where(np.abs(significance) > 3 , significance, np.full(np.shape(significance), np.nan)) #cut siginificant only
    plot2d(significance, x_centres_Bplus, y_centres_Bplus)
    plt.xlabel("$m^{2}_{\pi \pi}$", fontsize=30)
    plt.ylabel("$m^{2}_{K \pi} $", fontsize=30)
    plt.title("regions with significance above 3 $\sigma$")
    plt.savefig("plots/local_asymmetry_600x30_transpose_significant.png")
    plt.show()
    sign_values, sign_x, image_sign = plt.hist(significance_flat, 30, range=[-6, 6])
    plt.cla()
    sign_x_centres, sign_unc = get_bins(sign_x, sign_values)
    sign_unc = np.where(sign_unc == 0, np.full(np.shape(sign_unc), 1), sign_unc)
    popt, pcov = curve_fit(norm_fitted, sign_x_centres, sign_values, p0=[0, 1, 50], sigma=sign_unc, absolute_sigma=True)
    plt.plot(sign_x_centres, norm_fitted(sign_x_centres, *popt))
    plt.errorbar(sign_x_centres, sign_values, sign_unc, ls='None', capsize=2)
    print(popt)
    print(np.sqrt(np.diag(pcov)))
    chi_fit = chi_squared(sign_values, norm_fitted(sign_x_centres, *popt), sign_unc, 3)
    print(chi_fit)
    plt.xlabel("units of $\sigma$", fontsize=30)
    plt.ylabel("$counts / 0.4 \sigma $", fontsize=30)
    plt.title("Local asymmetry histogram")
    plt.savefig("plots/local_asymmetry_600x30_transpose_consistent.png")
    plt.show()


def procedure_local_asymmetry(x_resolution, y_resolution, limits, transpose=False):
    popt_all, popt_Bplus, popt_Bminus = attempt_fit()
    
    #procedure to get local asymmetry



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
    #fit_region(data2[:, 0], data2[:, 1], inv_mass2)
    





    
    # xoffset, tau, exp_norm, total_norm
    popt_exp = [popt_all[9], popt_all[8], popt_all[10], popt_all[11]]
    dalitz_values, dalitz_x_bins, dalitz_y_bins = subtract_background(popt=popt_exp, inv_mass_all=inv_mass, two_body_all=data, bins=[x_resolution,y_resolution], transpose=transpose, limits=limits)
    rough_values, rough_x_bins, rough_y_bins = subtract_background(popt=popt_exp, inv_mass_all=inv_mass, two_body_all=data, bins=[y_resolution,y_resolution], transpose=transpose, limits=limits)
    rough_values = np.hstack(rough_values)
    rough_values = np.where(rough_values <= 0, np.full(np.shape(rough_values), -10), rough_values)
    
    values, bins_x, bins_y = variable_bins(dalitz_values, dalitz_x_bins, dalitz_y_bins, resolution_x=x_resolution, resolution_y=y_resolution)
    hist_values, hist_x, hist_y = convert_2d_hist(values, bins_x, bins_y, x_resolution=x_resolution, limits_x=limits)
    flat_values = np.hstack(values)




    axes, image = plot2d(hist_values, hist_x, hist_y)
    plot_frame(bins_x, bins_y, x_resolution, limits)

    plt.colorbar(image)
    plt.xlabel(r"$m_{\pi \pi}^2$[GeV$^2$]", fontsize=30)
    plt.ylabel(r"$m_{K \pi}^2$[GeV$^2$]", fontsize=30)
    plt.title("Dalitz plot in variable bins")
    plt.savefig("plots/variable_bins_goodness.png")

    plt.show()
    print(len(flat_values), len(rough_values))
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 9))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    ax[0].hist(flat_values, bins=50, range=[0, 200])
    ax[1].hist(rough_values, bins=50, range=[0,200])
    ax[0].set_ylim([0, 150])
    ax[1].set_ylim([0, 150])
    ax[0].set_title("Binned values for variable bins 20x20")
    ax[1].set_title("Binned values for default bins 20x20")
    ax[0].set_xlabel("Events in each bin", fontsize=30)
    ax[1].set_xlabel("Events in each bin", fontsize=30)
    ax[0].set_ylabel("Number of bins / 4 events", fontsize=30)
    ax[1].set_ylabel("Number of bins / 4 events", fontsize=30)
    #fig.savefig("plots/compare_var_bins_20x20.png", dpi=400)
    plt.show()

    
    popt_Bplus_exp = [popt_Bplus[9], popt_Bplus[8], popt_Bplus[10], popt_Bplus[11]]
    popt_Bminus_exp = [popt_Bminus[9], popt_Bminus[8], popt_Bminus[10], popt_Bminus[11]]
    data_Bplus, x, y = subtract_background(popt=popt_Bplus_exp, inv_mass_all=inv_mass1, two_body_all=data1, bins=[x_resolution,y_resolution], transpose=transpose, limits=limits)
    data_Bminus, x, y = subtract_background(popt=popt_Bminus_exp, inv_mass_all=inv_mass2, two_body_all=data2, bins=[x_resolution,y_resolution], transpose=transpose, limits=limits)

    
    get_Bplus_Bminus(data_Bplus, data_Bminus, bins_x, bins_y, x_resolution, y_resolution, limits_x=limits)