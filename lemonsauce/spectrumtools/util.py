from numpy import exp, array, concatenate, dot


def total_absorption(absorption_coefficient, optical_depth):
    """ Calculates absorption based on the absorption coefficient and optical density"""
    return 1.0 - total_transmission(absorption_coefficient, optical_depth)


def total_transmission(absorption_coefficient, optical_depth):
    """ Calculates transmission based on the absorption coefficient and optical density"""
    return exp(-absorption_coefficient*optical_depth)


def normalise_spectral_density(wavelengths: array, spectral_density: array):
    """ This normalises a spectrum to have a total integrated area of 1

    Args:
        wavelengths (array): The wavelengths at which the density is recorded (units: nm)
        spectral_density (array): A density with respect to wavelength (units: [some units] / nm)

    Returns:
        A spectral density that integrates to 1 with respect to wavelength (units: [some units])
    """

    mid_bins = 0.5 * (wavelengths[1:] + wavelengths[:-1])
    bin_bounds = concatenate((wavelengths[:1], mid_bins, wavelengths[-1:]))
    bin_sizes = bin_bounds[1:] - bin_bounds[:-1]

    total_area = dot(spectral_density, bin_sizes)

    return spectral_density / total_area




