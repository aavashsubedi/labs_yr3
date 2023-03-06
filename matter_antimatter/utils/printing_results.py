import numpy as np

#default printer of results

def print_results(coeff,cov,chi2,ndf):
    perr = np.sqrt(np.diag(cov)) # extract errors from covarianve matrix
    # output fit results
    print(f"Fit results with chi2/ndf {chi2} / {ndf}")
    parcount = 0
    for p,e in zip(coeff,perr):
        parcount += 1
        print(f"Par {parcount:d}: {p:f} +/- {e:f}")


if __name__=="main":
    print_results(coeff, cov, chi2, ndf)