import matplotlib.pyplot as plt


def plotting_defaults():
    plt.rcParams.update({"axes.prop_cycle" : "cycler('color', ['0C5DA5', '00B945', 'FF9500', 'FF2C00', '845B97', '474747', '9e9e9e'])",
    "figure.figsize" : (3.5, 2.625),
    "xtick.major.size" : 3,
    "xtick.major.width" : 0.5,
    "xtick.minor.size" : 1.5,
    "xtick.minor.width" : 0.5,
    "xtick.minor.visible" : True,
    "xtick.top" : True,

    "ytick.major.size" : 3,
    "ytick.major.width" : 0.5,
    "ytick.minor.size" : 1.5,
    "ytick.minor.width" : 0.5,
    "ytick.minor.visible" : True,
    "ytick.right" : True,

    "xtick.labelsize" : 16,
    "ytick.labelsize" : 16,
    "legend.fontsize" : 16,
    "legend.title_fontsize" : 16,
    "axes.titlesize" : 16,
    "axes.labelsize" : 16,


    "axes.linewidth" : 0.5,
    "grid.linewidth" : 0.5,
    "lines.linewidth" : 1.0,
    "legend.frameon" : False,
    "legend.loc" : "best",

    "savefig.bbox" : "tight",
    "savefig.pad_inches" : 0.05,

    "font.family" : "sans-serif",
    "mathtext.fontset" : "dejavusans",
    })
    plt.rcParams["figure.figsize"] = (12, 8)
    return 0
