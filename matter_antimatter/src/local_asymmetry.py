import numpy as np
import matplotlib.pyplot as plt


def local_asymmetry( Bplus_data = [], Bminus_data = [] ):
    x_centres_Bplus, y_centres_Bplus, weigths_Bplus = Bplus_data
    x_centres_Bminus, y_centres_Bminus, weigths_Bminus = Bminus_data

    asymmetry = (weigths_Bminus - weigths_Bplus) / (weigths_Bplus + weigths_Bminus)

    plt.hist2d(x_centres_Bplus, y_centres_Bminus, asymmetry)

    return