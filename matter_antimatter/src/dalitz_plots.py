import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def dalitz_plot(resonance_kpi, resonance_pipi, bins=30):
    kpi_squared = resonance_kpi**2
    pipi_squared = resonance_pipi**2

    #to GeV
    kpi_squared /= 10**6
    pipi_squared /= 10**6    

    

    values, x_bin_edges, y_bin_edges, image = plt.hist2d(kpi_squared, pipi_squared, bins=bins, range=[[0, 20], [0, 20]])
    #plt.colorbar()
    values = np.array(values).T
    #plt.show()
    return values, x_bin_edges, y_bin_edges

def variable_bins(x_values, y_values, resolution_x=200, resolution_y=30, tolerance=0.01):

    low_limit_x = 0
    values, x_bins_edges, y_bins_edges = dalitz_plot(x_values, y_values, bins=[resolution_x,resolution_y])
    max_value = np.max(values)
    print("Max bin value is: {}".format(max_value))

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


                if column >= index_max:
                    #Dumping the last bin as it is not full
                    new_x_bin_edge = x_bins_edges[column + 1]
                    #new_x_bins_edges_row.append(new_x_bin_edge)
                    #new_values_row.append(current_column)
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
    print(np.sum(total_row_counts))
    print(np.sum(sum_of_bins))
    print(np.sum(values))

    return new_values, new_x_bins_edges, y_bins_edges
                    


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

