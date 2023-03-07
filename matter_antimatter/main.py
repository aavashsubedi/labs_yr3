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

def main():
    events_path = "data/example_file.root"
    # Read data
    pT, pX, pY, pZ = read_file(MAX_EVENTS=5000, mode=1)



    coeff_pT,cov_pT, bin_centres_pT, bin_centres_red_pT, chi2_pT, ndf_pT = fit_data( bins_pT, values_pT, 5000, 15000, [100,10000,10000] )

    print_results(coeff_pT,cov_pT, chi2_pT, ndf_pT)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    default_plot(ax,bin_centres_pT,bin_centres_red_pT,values_pT,coeff_pT,'fit_pT.pdf')

    return None

if __name__ == "__main__":
    main()