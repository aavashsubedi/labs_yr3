import uproot
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as colors
from scipy.optimize import curve_fit
# import file_reading from src file 
from src.file_reading import read_file
from importlib import reload

def main():
    events_path = "data/example_file.root"
    # Read data
    pT, pX, pY, pZ = read_file(MAX_EVENTS=5000, mode=0)

    return None

if __name__ == "__main__":
    main()