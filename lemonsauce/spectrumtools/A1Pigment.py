from numpy import exp, array


def visual_pigment(wls: array, lambdamax: float):
    """

    A1 Pigment Spectrum
    ===================


    An implementation of
    Govardovskii, V. I., N. Fyhrquist, T. Reuter, D. G. Kuzmin, and
    K. Donner. 2000. In search of the visual pigment template. Visual
    neuroscience 17:509–528.

    Args:
              wls: List of _wavelengths to evaluate at
        lambdamax: peak value

    """

    # Ingore PIP so that the notion here matches the paper

    lambdamax = float(lambdamax)
    
    A = 69.7
    B = 28
    b = 0.922
    C = -14.9
    c = 1.104
    D = 0.674

    a = 0.8795 + 0.0459*exp(-((lambdamax-300.)**2)/11940.)
    
    x = lambdamax/wls
    
    output = 1/(exp(A*(a-x)) + exp(B*(b-x)) + exp(C*(c-x)) + D)
    
    # beta band
    
    lambdabeta = 189 + 0.315*lambdamax
    bbeta = -40.5 + 0.195*lambdamax
    Abeta = 0.26
    
    return output + Abeta*exp(-((wls - lambdabeta)/bbeta)**2)

# A quick test
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from numpy import arange
    wls = arange(300,800)

    for lmax in [350,400, 500, 600]:
        plt.plot(wls, visual_pigment(wls,lmax))

    plt.show()
        


    
    
