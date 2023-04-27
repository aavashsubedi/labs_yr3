import matplotlib.pyplot as plt

def plot_comparison():
    x_data = [0.028, 0.049, 0.032, 0.049]
    x_err = [0.03, 0.033, 0.011, 0.015]

    y_data = [3, 4, 2, 1]
    fig = plt.figure(figsize=(14, 6))
    axes = fig.add_subplot()

    axes.errorbar(x_data[0], y_data[0], xerr=x_err[0], label="BaBaR (2008)", fmt='o', capsize=5, elinewidth=5)
    axes.errorbar(x_data[1], y_data[1], xerr=x_err[1], label="Belle (2006)", fmt='o', capsize=5, elinewidth=5)
    axes.errorbar(x_data[2], y_data[2], xerr=x_err[2], label="LHCb (2013)", fmt='o', capsize=5, elinewidth=5)
    axes.errorbar(x_data[3], y_data[3], xerr=x_err[3], label="This work (2023)", fmt='o', capsize=5, elinewidth=5)
    axes.plot([0, 0], [0.5, 4.5], ls='--', color='black')
    axes.legend()
    axes.set_xlim([-0.02, 0.1])
    axes.set_ylim([0.5, 4.5])
    axes.get_yaxis().set_visible(False)
    axes.set_title("Global asymmetry values from different experiments")
    axes.set_xlabel("Asymmetry", fontsize=26)
    plt.savefig("plots/comparison_results.png", dpi=600)
    plt.show()