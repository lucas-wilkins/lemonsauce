import os

from numpy import array, interp

from lemonsauce.spectrumtools import normalise_spectral_density

# We cache the data from the file in this variable
_d65_data = None


def d65(wavelengths: array, normalise: bool=False):
    """ D65 Illumunation spectrum.

    We have data for 300nm to 830nm, this function will pad with zeros outside that region

    Args:
        wavelengths (array): wavelengths to get the spectrum data for.
        normalise (bool): Apply a normalisation so that the total integrated intensity is one.

    Returns:
        D65 relative power [range of 0-120]
    """

    # We cache the data so that we don't need to read it every time
    global _d65_data

    if _d65_data is None:

        # Load D65 data
        filename = os.path.join(os.path.dirname(__file__), 'd65.txt')
        fid = open(filename, 'r')

        els = []
        for line in fid:
            els.append(map(float, line.split()))

        fid.close()

        d65lambda, d65intensity = zip(*els)

        _d65_data = d65lambda, d65intensity

    d65wls, d65f = _d65_data

    out = interp(wavelengths, d65wls, d65f, left=0.0, right=0.0)

    if normalise:
        return normalise_spectral_density(wavelengths, out)
    else:
        return out


if __name__ == "__main__":
    from numpy import arange
    import matplotlib.pyplot as plt

    # non-uniform data points outside of expected range to check interpolation
    wls = (arange(0,1000,10)**2)/1000.0

    plt.plot(wls, d65(wls), "+")

    plt.show()
