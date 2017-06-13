"""

Fractional Yield Example
========================


This is an example of how to calculate fractional yield functions

The data loaded here is used in the other examples.

"""

# Numpy imports
from numpy import arange, transpose, array


# Imports from the colour and spectrum packages
from lemonsauce import d65, total_absorption, template_pigment

lambda_min = 300
lambda_max = 750
wavelengths = arange(lambda_min, lambda_max)

spectral_sensitivities = []
for lmax in [420, 500, 620, 580]:

    # Use A1 Pigment template
    # Assume an optical density of 1
    ss = total_absorption(template_pigment(wavelengths, lmax), 1)
    spectral_sensitivities.append(ss)

# factor in the illuminant
illumination = d65(wavelengths)
example_fraction_yields = [ss * illumination for ss in spectral_sensitivities]

# normalise
example_fraction_yields = [cf / sum(cf) for cf in example_fraction_yields]

# make into an array with the correct orientation
example_fraction_yields = transpose(array(example_fraction_yields))

# If we're running this file as a script, plot the data we have calculated
if __name__ == "__main__":

    import matplotlib.pyplot as plt

    for i in range(4):

        plt.subplot(2, 1, 1)
        plt.title("Spectral Sensitivities")
        plt.plot(wavelengths, spectral_sensitivities[i])

        plt.subplot(2, 1, 2)
        plt.title("Fractional Yield under D65 Illumination")
        plt.plot(wavelengths, example_fraction_yields[:, i])

    plt.show()
