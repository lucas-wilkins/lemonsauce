""" Example calculations of vividness """

# Python packages
from numpy import random

# Local packages, ColourSolid does all the work
from lemonsauce import ColourSolid

# For making extreme spectra
from lemonsauce import extreme_spectrum


#
# load the example fractional yields
#
from examples.fractional_yields import example_fraction_yields, wavelengths

#
# Create a trichromat colour solid
#
solid = ColourSolid(example_fraction_yields[:, :3])


#
#
# Create some two transition extreme spectra, they should have a vividness close to one.
#
#

# Use a range of transition wavelengths that avoids transitions to far from visible
lambda_min = 340
lambda_max = 650

# We'll get a mean and variance for the vividness
n = 25
two_transition_data = []

for i in range(n):

    # Random parameters for the extreme spectra
    transitions = [lambda_min + (lambda_max-lambda_min)*random.rand() for i in range(2)]
    one_first = random.rand() > 0.5

    # Create an extreme spectrum
    spectrum = extreme_spectrum(wavelengths, one_first, *transitions)

    # Get its vividness
    vividness = solid.vividness(spectrum)

    # Print the result to the console
    params = ", ".join([str(x) for x in [one_first] + transitions])
    print("Two transition spectrum %i: %g (%s)" % (i, vividness, params))

    # add to data so that we can get the stats
    two_transition_data.append(vividness)

#
#
# Create some three transition extreme spectra,
# They should have a smaller average vividness, with a greater variance.
#
#

three_transition_data = []

for i in range(n):

    # Random parameters for the extreme spectra
    transitions = [lambda_min + (lambda_max-lambda_min)*random.rand() for i in range(3)]
    one_first = random.rand() > 0.5

    # Create an extreme spectrum
    spectrum = extreme_spectrum(wavelengths, one_first, *transitions)

    # Get its vividness
    vividness = solid.vividness(spectrum)

    # Print the result to the console
    params = ", ".join([str(x) for x in [one_first] + transitions])
    print("Three transition spectrum %i: %g (%s)" % (i, vividness, params))

    # add to data so that we can get the stats
    three_transition_data.append(vividness)

#
#
#   Calculate and print out the stats
#
#

m2 = sum(two_transition_data)/n
m3 = sum(three_transition_data)/n

v2 = sum([x**2 for x in two_transition_data])/n - m2**2
v3 = sum([x**2 for x in three_transition_data])/n - m3**2

sample_correction = float(n) / (n-1)

v2 *= sample_correction
v3 *= sample_correction


print()
print("  Two transition mean: %g" % m2)
print("             variance: %g" % v2)

print("Three transition mean: %g" % m3)
print("             variance: %g" % v3)
