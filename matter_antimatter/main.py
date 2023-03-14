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
    pT, pX, pY, pZ, h1_prob, h2_prob, h3_prob, master_prob, inv_mass, two_body= read_file(MAX_EVENTS=50000, mode=4, path_name="", selection=True)
    print(len(h1_prob[0]))
    #np.savetxt("data/inv_mass.csv", inv_mass, delimiter=',')
    #print(inv_mass)
    #plotting_histograms_probability(master_prob[0], master_prob[1], savefig_name="small_sel")
    two_body = np.array(two_body)
    two_body.flatten
    plt.hist(two_body, bins=500, range=[500, 5000], histtype='step')
    plt.show()
    

    return None

if __name__ == "__main__":
    main()