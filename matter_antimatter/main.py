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




def main():
    
    # Read data
    pT, pX, pY, pZ, h1_prob, h2_prob, h3_prob, master_prob, inv_mass, two_body= read_file(MAX_EVENTS=10000, mode=4, path_name="", selection=True)
    print(len(h1_prob[0]))
    print(np.shape(two_body))
    #np.savetxt("data/inv_mass.csv", inv_mass, delimiter=',')
    #print(inv_mass)
    #plotting_histograms_probability(master_prob[0], master_prob[1], savefig_name="small_sel")
    two_body = np.array(two_body)
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    ax[0].hist(two_body[:, 0], bins=100, range=[0, 5000], histtype='step', label='$K + pion$')
    ax[1].hist(two_body[:, 1], bins=100, range=[0, 5000], histtype='step', label='$pion + pion$')
    ax[2].hist(inv_mass, bins=200, range=[4500, 6200], histtype='step', label='inv mass')                    
    
    plt.show()
    

    return None

if __name__ == "__main__":
    main()