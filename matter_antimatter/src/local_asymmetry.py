import numpy as np
import matplotlib.pyplot as plt
from utils.histogram import use_histogram_frame
from src.binning_files import get_bins
from utils.histogram import plot_frame
from utils.histogram import plot2d


def local_asymmetry( Bplus_data = [], Bminus_data = [], x_resolution=200, y_resolution=50 ):
    x_centres_Bplus, y_centres_Bplus, weigths_Bplus = Bplus_data
    x_centres_Bminus, y_centres_Bminus, weigths_Bminus = Bminus_data

    

    asymmetry = (weigths_Bminus - weigths_Bplus) / (weigths_Bplus + weigths_Bminus)
    asymmetry = np.where(np.isnan(asymmetry), np.zeros(np.shape(asymmetry)), asymmetry)
        
    
    #plt.contourf(x_centres_Bplus, y_centres_Bplus, asymmetry, levels=[-1.0, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 0.75, 1.0], corner_mask=False)
    #plt.hist2d(x_centres_Bplus, y_centres_Bplus, bins=[x_resolution, y_resolution], weights=asymmetry)
    plot2d(asymmetry, x_centres_Bplus, y_centres_Bplus)

    #plt.colorbar()
    plt.show()

    return

def get_Bplus_Bminus(data_Bplus, data_Bminus, x_bins_edges, y_bins_edges,x_resolution=200, y_resolution=50, limits_x=[0, 20]):
    
    new_values_Bplus, x_bins_Bplus, y_bins_Bplus = use_histogram_frame(data_Bplus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)
    new_values_Bminus, x_bins_Bminus, y_bins_Bminus = use_histogram_frame(data_Bminus, x_bins_edges, y_bins_edges, x_resolution, y_resolution, limits_x)

    #x_centres_Bplus, unc = get_bins(x_bins_Bplus, new_values_Bplus)
    x_centres_Bplus = x_bins_Bplus
    y_centres_Bplus, unc_Bplus = get_bins(y_bins_Bplus, new_values_Bplus)

    #x_centres_Bminus, unc = get_bins(x_bins_Bminus, new_values_Bminus)
    x_centres_Bminus = x_bins_Bminus
    y_centres_Bminus, unc_Bminus = get_bins(y_bins_Bminus, new_values_Bminus)

    
    plt.show()
    
    plot_frame(x_bins_edges[1:], y_bins_edges[1:], x_resolution, limits_x)
    #local_asymmetry([x_centres_Bplus, y_centres_Bplus, new_values_Bplus], [x_centres_Bminus, y_centres_Bminus, new_values_Bminus], x_resolution, y_resolution)
    local_asymmetry([x_bins_Bplus, y_bins_Bplus, new_values_Bplus], [x_bins_Bminus, y_bins_Bminus, new_values_Bminus], x_resolution, y_resolution)
