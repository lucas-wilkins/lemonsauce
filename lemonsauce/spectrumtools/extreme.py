from numpy import *


def extreme_spectrum(wavelengths: array, one_first: bool, *transitions):
    """ Create an "extreme spectrum"

    Args:
        wavelengths (array): wavelengths at which to calculate the spectrum
        one_first (bool): Should the reflectance start with one (true) or zero (false)
        transitions (float*): Points at which the spectrum should change between zero and one, or vice-versa

    Returns:
        an extreme spectrum
    """

    transitions = list(transitions)
    transitions.sort()

    def value(wavelength: float):
        is_one = one_first
        for transition in transitions:
            is_one ^= (transition > wavelength)

        return 1.0 if is_one else 0.0

    return array([value(wavelength) for wavelength in wavelengths])


if __name__ == "__main__":
    # Check spectra by plotting them

    import matplotlib.pyplot as plt

    wavelengths = arange(300, 800, 1.0)

    plt.subplot(2, 2, 1)
    plt.plot(wavelengths, extreme_spectrum(wavelengths, True, 400, 500))

    plt.subplot(2, 2, 2)
    plt.plot(wavelengths, extreme_spectrum(wavelengths, True, 400, 500, 600))

    plt.subplot(2, 2, 3)
    plt.plot(wavelengths, extreme_spectrum(wavelengths, False, 430.2, 721.4))

    plt.subplot(2, 2, 4)
    plt.plot(wavelengths, extreme_spectrum(wavelengths, False, 350, 400, 450, 500, 550))

    plt.show()

