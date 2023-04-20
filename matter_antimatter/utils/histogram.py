import matplotlib.pyplot as plt
import numpy as np



def dalitz_plot(resonance_kpi, resonance_pipi, bins=30, limits=[0, 27]):
    kpi_squared = resonance_kpi**2
    pipi_squared = resonance_pipi**2

    #to GeV
    kpi_squared /= 10**6
    pipi_squared /= 10**6    

    

    values, x_bin_edges, y_bin_edges, image = plt.hist2d(kpi_squared, pipi_squared, bins=bins, range=[limits, limits])
    #plt.clf()
    #plt.colorbar()
    values = np.array(values).T
    #plt.show()
    return values, x_bin_edges, y_bin_edges


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
    #plt.savefig("plots/variable_bin_width_1000x50.png", dpi=1200)
    plt.show()
    return converted_values, histogram_frame, y_bins_edges


def use_histogram_frame(values, x_bins_edges, y_bins_edges, x_resolution=200, y_resolution=50, limits_x=[0, 20]):

    #hist_values, hist_bins_x, hist_bins_y = dalitz_plot(values[:, 1], values[:, 0], bins=[x_resolution, y_resolution], limits=limits_x)
    
    hist_values = values.transpose()
    histogram_frame = np.linspace(limits_x[0], limits_x[1], x_resolution, endpoint=True)
    converted_values = [np.full(x_resolution, -1)]
    
    

    #print(np.max(hist_values))

    for row in range(0, len(y_bins_edges) - 1):
        #plt.plot([x_bins_edges[row][0], x_bins_edges[row][-1]], [y_bins_edges[row + 1], y_bins_edges[row + 1]], color='r', ls='--', lw='0.5')
        #plt.plot([x_bins_edges[row][0], x_bins_edges[row][0]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
        row_values = []
        row_values_framed = np.zeros(x_resolution)
        for column in range(0, len(x_bins_edges[row]) - 1):
            column_value = 0
            for iterator in range(0, len(histogram_frame)):
                #print(iterator, histogram_frame[iterator], x_bins_edges[row][column + 1], column_value, hist_values[row, iterator])
                if ((histogram_frame[iterator] < x_bins_edges[row][column + 1]) and 
                    (histogram_frame[iterator] >= x_bins_edges[row][column ])):
                    column_value += hist_values[row, iterator]
                if histogram_frame[iterator] >= x_bins_edges[row][column + 1]:
                    #plt.plot([x_bins_edges[row][column + 1], x_bins_edges[row][column + 1]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
                    #print("break")
                    break
                    
            #print(column_value)    
            row_values.append(column_value)
        
        for second_column in range(0, len(x_bins_edges[row]) - 1):
            for index in range(0, len(histogram_frame)):
                if ((histogram_frame[index] < x_bins_edges[row][second_column + 1]) and 
                    (histogram_frame[index] >= x_bins_edges[row][second_column ])):
                    row_values_framed[index] = row_values[second_column]
                
                    
            
        converted_values = np.append(converted_values, [row_values_framed], axis=0)
        #print(row_values)


    converted_values = np.delete(converted_values, 0, axis=0)
    return converted_values, histogram_frame, y_bins_edges

def plot_frame(x_bins_edges, y_bins_edges, x_resolution=200, limits_x=[0, 20], ax=None):

    if ax==None:
        ax = plt.gca() # get current axes

    histogram_frame = np.linspace(limits_x[0], limits_x[1], x_resolution, endpoint=True)
    for row in range(0, len(y_bins_edges) - 1):
        
        ax.plot([x_bins_edges[row][0], x_bins_edges[row][-1]], [y_bins_edges[row + 1], y_bins_edges[row + 1]], color='r', ls='--', lw='0.5')
        ax.plot([x_bins_edges[row][0], x_bins_edges[row][0]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
        for column in range(0, len(x_bins_edges[row]) - 1):
            for iterator in range(0, len(histogram_frame)):
                if histogram_frame[iterator] >= x_bins_edges[row][column + 1]:
                    ax.plot([x_bins_edges[row][column + 1], x_bins_edges[row][column + 1]], [y_bins_edges[row], y_bins_edges[row + 1]], color='r', ls='-', lw='0.5')
                    break


def plot2d(h, xbins, ybins, ax=None, **plot_kwargs):
    '''Provide explicit axes to choose where to plot it, otherwise the current axes will be used'''
    if ax==None:
        ax = plt.gca() # get current axes
    
    image = ax.matshow(h, extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]], aspect='auto', origin='lower', **plot_kwargs)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    

    return ax, image