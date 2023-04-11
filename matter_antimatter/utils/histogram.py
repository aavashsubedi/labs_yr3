import matplotlib.pyplot as plt
import numpy as np

def convert_2d_hist(values, x_bins_edges, y_bins_edges, x_resolution=200, limits_x=[0, 20]):

    histogram_frame = np.linspace(limits_x[0], limits_x[1], x_resolution, endpoint=True)
    converted_values = [np.full(x_resolution, -1)]


    for row in range(0, len(values)):
        row_values = np.zeros(x_resolution)
        plt.plot([x_bins_edges[row][0], x_bins_edges[row][-1]], [y_bins_edges[row + 1], y_bins_edges[row + 1]], color='r', ls='--', lw='0.5')
        plt.plot([x_bins_edges[row][0], x_bins_edges[row][0]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
        for column in range(0, len(values[row])):
            #print("values:{0}{1}".format(len(values[row]), values[row]))
            
            #print("bins: {0} {1}".format(len(x_bins_edges[row]), x_bins_edges[row]))
            
            
            #value = np.full(x_resolution, values[row][column])
            #row_values = np.where((histogram_frame >= x_bins_edges[row][column + 1]) & (histogram_frame < x_bins_edges[row][column]), row_values, value)

            for iterator in range(0, len(histogram_frame)):
                if ((histogram_frame[iterator] < x_bins_edges[row][column + 1]) and 
                    (histogram_frame[iterator] >= x_bins_edges[row][column ])):
                    row_values[iterator] = values[row][column]
                if histogram_frame[iterator] >= x_bins_edges[row][column + 1]:
                    plt.plot([x_bins_edges[row][column + 1], x_bins_edges[row][column + 1]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
                    break

        #print(row_values)
        converted_values = np.append(converted_values, [row_values], axis=0)

    converted_values = np.delete(converted_values, 0, axis=0)
    plt.savefig("plots/variable_bin_width_1000x50.png", dpi=1200)
    plt.show()
    return converted_values, histogram_frame, y_bins_edges
            

    