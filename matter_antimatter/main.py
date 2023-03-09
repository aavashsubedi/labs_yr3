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
    pT, pX, pY, pZ, h1_prob, h2_prob, h3_prob, master_prob, inv_mass= read_file(MAX_EVENTS=5000, mode=2, path_name="", selection=True)
    print(len(h1_prob[0]))

    #print(inv_mass)
    plotting_histograms_probability(master_prob[0], master_prob[1], savefig_name="small_sel")
    

    return None

if __name__ == "__main__":
    main()