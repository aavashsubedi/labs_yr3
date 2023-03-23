import numpy as np

def chi2(data_y, model_y)
    return np.sum( (data_y - model_y)**2 / model_y)
