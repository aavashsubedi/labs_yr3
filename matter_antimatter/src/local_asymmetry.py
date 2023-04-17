import numpy as np
import matplotlib.pyplot as plt
from utils.histogram import use_histogram_frame
from src.binning_files import get_bins
from utils.histogram import plot_frame
from utils.histogram import plot2d


def local_asymmetry( Bplus_data = [], Bminus_data = [], x_resolution=200, y_resolution=50 ):
    x_centres_Bplus, y_centres_Bplus, weigths_Bplus = Bplus_data
    x_centres_Bminus, y_centres_Bminus, weigths_Bminus = Bminus_data

    all_events = np.sum(weigths_Bplus) + np.sum(weigths_Bminus)

    

    asymmetry = (weigths_Bminus - weigths_Bplus) / (weigths_Bplus + weigths_Bminus)
    asymmetry = np.where(np.isnan(asymmetry), np.full(np.shape(asymmetry), np.nan), asymmetry)
    #print(np.max(weigths_Bplus))

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
    sigma_asymmetry = np.where(np.isinf(sigma_asymmetry), np.full(np.shape(sigma_asymmetry), np.nan), sigma_asymmetry)
    sigma_asymmetry = np.where(np.isnan(sigma_asymmetry), np.full(np.shape(sigma_asymmetry), np.nan), sigma_asymmetry)
    print(np.min(sigma_asymmetry))

    significance = np.abs(asymmetry/sigma_asymmetry)
    significance = np.where(significance > 5, significance, np.full(np.shape(significance), np.nan)) #cut siginificant only
    
    #plt.contourf(x_centres_Bplus, y_centres_Bplus, asymmetry, levels=[-1.0, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 0.75, 1.0], corner_mask=False)
    #plt.hist2d(x_centres_Bplus, y_centres_Bplus, bins=[x_resolution, y_resolution], weights=asymmetry)
    
    #plot2d(asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[0])

    #plt.colorbar()
    

    #plot2d(sigma_asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[1])
    

    return asymmetry, sigma_asymmetry, significance

def get_Bplus_Bminus(data_Bplus, data_Bminus, x_bins_edges, y_bins_edges,x_resolution=200, y_resolution=50, limits_x=[0, 20]):
    
    new_values_Bplus, x_bins_Bplus, y_bins_Bplus = use_histogram_frame(data_Bplus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)
    new_values_Bminus, x_bins_Bminus, y_bins_Bminus = use_histogram_frame(data_Bminus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)

    #x_centres_Bplus, unc = get_bins(x_bins_Bplus, new_values_Bplus)
    x_centres_Bplus = x_bins_Bplus
    y_centres_Bplus, unc_Bplus = get_bins(y_bins_Bplus, new_values_Bplus)
    y_centres_Bplus = y_bins_Bplus #no idea why but this is correct

    #x_centres_Bminus, unc = get_bins(x_bins_Bminus, new_values_Bminus)
    x_centres_Bminus = x_bins_Bminus
    y_centres_Bminus, unc_Bminus = get_bins(y_bins_Bminus, new_values_Bminus)

    
    plt.show()
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    #plot_frame(x_bins_edges[1:], y_bins_edges[1:], x_resolution, limits_x, ax[0])
    #local_asymmetry([x_centres_Bplus, y_centres_Bplus, new_values_Bplus], [x_centres_Bminus, y_centres_Bminus, new_values_Bminus], x_resolution, y_resolution)
    asymmetry, sigma_asymmetry, significance= local_asymmetry([x_bins_Bplus, y_bins_Bplus, new_values_Bplus], [x_bins_Bminus, y_bins_Bminus, new_values_Bminus], x_resolution, y_resolution)
    
    axes, image1 = plot2d(asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[0])
    axes, image2 = plot2d(sigma_asymmetry, x_centres_Bplus, y_centres_Bplus, ax=ax[1])
    axes, image3 = plot2d(significance, x_centres_Bplus, y_centres_Bplus, ax=ax[2])
    fig.colorbar(image1, cax=None, ax=ax[0])
    fig.colorbar(image2, cax=None, ax=ax[1])
    fig.colorbar(image3, cax=None, ax=ax[2])
    ax[0].set_xlabel("a")
    fig.savefig("plots/local_asymmetry_150x15.png")
    plt.show()