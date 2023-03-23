import numpy as np
import matplotlib.pyplot as plt


def dalitz_plot(resonance_kpi, resonance_pipi):
    kpi_squared = resonance_kpi**2
    pipi_squared = resonance_pipi**2

    #to GeV
    kpi_squared /= 10**6
    pipi_squared /= 10**6    

    values, x_bin_edges, y_bin_edges, image = plt.hist2d(kpi_squared, pipi_squared, bins=30, range=[[0.36, 16], [0.36, 16]])
    plt.colorbar()
    plt.show()
    return values, x_bin_edges, y_bin_edges






