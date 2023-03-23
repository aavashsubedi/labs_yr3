import numpy as np

def gaussian(x, norm, mean, sigma):
    return np.array( (1 / sigma) * (1/np.sqrt(2 * np.pi)) * norm * np.exp( -0.5 * ( (x-mean)/sigma )**2 ) )
def exponential(x, norm, decay, xoffset):
# this is a technical parameter, which can be used to move the position at which the function evaluates to "norm"
    return np.array( (1 / decay )  * norm * np.exp(-(x-xoffset)/decay) )
def constant(x, norm):
    return np.array( norm * np.ones(len(x)) )

def half_gaussian(x, norm, mean, sigma):
    return np.array( (1 / sigma) * norm * np.exp( -0.5 * ( (x-mean)/sigma )**2 ) * (x > mean) )


def fit_func(x, norm, mean, sigma):
    return np.array( gaussian(x, norm, mean, sigma) )
def fit_func_triple(x, norm1, mean1, sigma1, norm2, mean2, sigma2, normE, decayE):
    return np.array(gaussian(x, norm1, mean1, sigma1) + gaussian(x, norm2, mean2, sigma2)  + exponential(x, normE, decayE))

def fit_func_quad(x, norm1, mean1, sigma1, norm2, mean2, sigma2, normE, decayE, constant):
    return np.array(gaussian(x, norm1, mean1, sigma1) + gaussian(x, norm2, mean2, sigma2) + exponential(x, normE, decayE) + constant(x, constant))

def fit_func_trip_gauss(x, norm1, mean1, sigma1, norm2, mean2, sigma2, norm3, mean3, sigma3):
    return np.array(gaussian(x, norm1, mean1, sigma1) + gaussian(x, norm2, mean2, sigma2) + gaussian(x, norm3, mean3, sigma3))

def fit_func_half(x, norm1, mean1, sigma1, norm2, mean2, sigma2, normE, decayE,
                  offsetE):
    return np.array(half_gaussian(x, norm1, mean1, sigma1) +
                    gaussian(x, norm2, mean2, sigma2) +
                    exponential(x, normE, decayE, offsetE))

def lifted_gaussian(x, norm, mean, std, const):
    return gaussian(x, norm, mean, std) + const
