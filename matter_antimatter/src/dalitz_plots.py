import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
#from src.distributions import exponential
from src.binning_files import get_bins
from utils.histogram import plot2d

from scipy.stats import expon





def variable_bins(values, x_bins_edges, y_bins_edges, resolution_x=200, resolution_y=30, tolerance=0.01):

    low_limit_x = 0
    #values, x_bins_edges, y_bins_edges = dalitz_plot(x_values, y_values, bins=[resolution_x,resolution_y])
    max_value = np.max(values)
    print("target value is: {}".format(max_value))

    values = values.transpose()

    new_x_bins_edges = [[]]
    new_values = [[]]
    total_row_counts = []
    sum_of_bins = []

    #Iterate over all rows, they remain constant in width
    for row in range(0, len(y_bins_edges) - 1):
        new_values_row = []
        new_x_bins_edges_row = [low_limit_x]
        row_counts = 0
        
        xmin, xmax, index_min, index_max = crop_row(values[row,:], x_bins_edges)
        new_x_bins_edges_row = [xmin]

        #iterate over all columns, they are summed
        column = index_min
        while( column < index_max):
            
            
            #print(column) #Debugging
            current_column = values[row, column]
            to_fill = max_value - current_column

            while(True):

                row_counts += values[row, column] #Debugging, see total counts on each row


                if column >= index_max - 1:
                    #Not Dumping the last bin as it is not full
                    new_x_bin_edge = x_bins_edges[column + 1]
                    new_x_bins_edges_row.append(new_x_bin_edge)
                    new_values_row.append(current_column)
                    #print("EoL reached: {}".format(new_x_bin_edge)) #Debugging
                    break
                
                
                
                if ((current_column <= max_value + max_value * tolerance) and 
                    (current_column >= max_value - max_value * tolerance)):

                    new_x_bin_edge = x_bins_edges[column + 1]
                    new_x_bins_edges_row.append(new_x_bin_edge)
                    new_values_row.append(current_column)
                    #print("condition met: {}".format(current_column))
                    break
                else:
                    diff_1 = to_fill - max_value * tolerance - values[row, column]
                    diff_2 = values[row, column + 1] - (to_fill + max_value * tolerance )
                    if values[row, column + 1] > (to_fill + max_value * tolerance ):
                        if diff_2 > diff_1:
                            new_x_bin_edge = x_bins_edges[column + 1]
                            new_x_bins_edges_row.append(new_x_bin_edge)
                            new_values_row.append(current_column)
                            #print("next column overshoots: {}".format(current_column))
                            break
                        else:
                            new_x_bin_edge = x_bins_edges[column + 2]
                            new_x_bins_edges_row.append(new_x_bin_edge)
                            new_values_row.append(current_column + values[row, column + 1])
                            column += 1
                            
                            row_counts += values[row, column + 1]
                            #print("next column fine: {}".format(current_column + values[row, column + 1]))
                            break
                

                column += 1
                
                current_column += values[row, column]
                to_fill = max_value - current_column
            
            column += 1
            
        new_x_bins_edges.append(new_x_bins_edges_row)
        new_values.append(new_values_row)
        total_row_counts.append(row_counts)
        sum_of_bins.append(np.sum(new_values_row))

    #print(total_row_counts)
    #print(np.sum(total_row_counts))
    #print(np.sum(sum_of_bins))
    #print(np.sum(values))
    flat_values = np.hstack(new_values)
    print("Max bin value is: {}".format(np.amax(flat_values)))

    return new_values[1:], new_x_bins_edges[1:], y_bins_edges
                    


def crop_row(x_values, x_bins_edges, treshold=1):
    x_min = x_bins_edges[0]
    x_max = x_bins_edges[-1]
    for iterator in range(0, len(x_values)):
        if x_values[iterator] >= treshold:
            x_min = x_bins_edges[iterator]
            break
    for iterator_inverse in range(1, len(x_values)):
        if x_values[-iterator_inverse] >= treshold:
            x_max = x_bins_edges[-iterator_inverse + 1]
            break
    
    
    return x_min, x_max, iterator, len(x_values) - iterator_inverse


def subtract_background(popt=[], signal_limits=[5235, 5333], combinatorial_limits=[5400, 5600], inv_mass_all=[], two_body_all=[], bins=[30, 30], transpose=False, limits=[0, 27]):
    #find ratio of the exponential integrals in signal and combinatorial regions
    signal_x_values = np.linspace(signal_limits[0], signal_limits[1], 1000)
    combinatorial_x_values = np.linspace(combinatorial_limits[0], combinatorial_limits[1], 1000)
    signal_exponential = expon.pdf(signal_x_values, popt[0], popt[1]) * popt[2] * popt[3]
    combinatorial_exponential = expon.pdf(combinatorial_x_values, popt[0], popt[1]) * popt[2] * popt[3]
    signal_integral = np.trapz(signal_exponential, signal_x_values)
    combinatorial_integral = np.trapz(combinatorial_exponential, combinatorial_x_values)
    ratio_exponentials = combinatorial_integral / signal_integral

    #Select events in both regions by invariant masses
    
    signal_indexes = np.argwhere((inv_mass_all > signal_limits[0]) &
                                  (inv_mass_all < signal_limits[1]))
    
    signal_events_inv_mass = inv_mass_all[signal_indexes]
    signal_two_body = two_body_all[signal_indexes, :]
    signal_two_body = signal_two_body[:, 0, :]
    

    combinatorial_indexes = np.argwhere((inv_mass_all > combinatorial_limits[0]) & 
                                        (inv_mass_all < combinatorial_limits[1]))
    combinatorial_events_inv_mass = inv_mass_all[combinatorial_indexes]
    combinatorial_two_body = two_body_all[combinatorial_indexes, :]
    combinatorial_two_body = combinatorial_two_body[:, 0, :]

    column1_s = np.array([])
    column2_s = np.array([])
    column1_c = np.array([])
    column2_c = np.array([])
    if transpose == True:
        column1_s = signal_two_body[:, 1]
        column2_s = signal_two_body[:, 0]
        column1_c = combinatorial_two_body[:, 1]
        column2_c = combinatorial_two_body[:, 0]
    else:
        column1_s = signal_two_body[:, 0]
        column2_s = signal_two_body[:, 1]
        column1_c = combinatorial_two_body[:, 0]
        column2_c = combinatorial_two_body[:, 1]

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))
    fig.subplots_adjust(wspace=0.3) # increase horizontal space between plots
    image1 = ax[0].hist2d(np.square(column1_s / 10**3), np.square(column2_s / 10**3), bins=bins, range=[limits, limits])
    ax[0].set_xlabel("$K \pi$")
    ax[0].set_ylabel("$\pi \pi$")
    ax[0].set_title("Dalitz plot of signal peak")
    fig.colorbar(image1[3], cax=None, ax=ax[0])

    image2 = ax[1].hist2d(np.square(column1_c / 10**3), np.square(column2_c / 10**3), bins=bins, range=[limits, limits])
    ax[1].set_xlabel("$K \pi$")
    ax[1].set_ylabel("$\pi \pi$")
    ax[1].set_title("Dalitz plot of combinatorial region")
    fig.colorbar(image2[3], cax=None, ax=ax[1])

    x_centres = get_bins(image1[1])
    y_centres = get_bins(image1[2])

    weight1 = np.array(image1[0])
    weight2 = np.array(image2[0])
    weight2 /= ratio_exponentials
    weight_subtracted = np.subtract(weight1, weight2)
    weight_subtracted = np.where(weight_subtracted < 0, np.full(np.shape(weight_subtracted), 0), weight_subtracted)
    #weight_subtracted = np.where(weight_subtracted == 0, np.full(np.shape(weight_subtracted), np.nan), weight_subtracted)

    axis3, image3 = plot2d(weight_subtracted.transpose(), image1[1], image1[2], ax[2])
    ax[2].set_xlabel("$K \pi$")
    ax[2].set_ylabel("$\pi \pi$")
    ax[2].set_title("Dalitz plot subtracted")
    fig.colorbar(image3, cax=None, ax=ax[2])
    #fig.savefig("plots/subtract_dalitz.png", dpi=600)
    plt.show()

    #print(weight_subtracted.shape)
    #print(image1[1].shape)

    return weight_subtracted, image1[1], image1[2]





