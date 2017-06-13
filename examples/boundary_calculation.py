"""

Example calculations of the boundary spectrum
=============================================

We give an example of using solid.boundary_spectrum to get the
spectrum of a colours corresponding boundary, then we get
the colour of that point and bind it here.

"""

# Python packages
import matplotlib.pyplot as plt
from numpy import array

# Lemonsauce packages, ColourSolid does all the work
from lemonsauce import ColourSolid

#
# load the example fractional yields
#
from examples.fractional_yields import example_fraction_yields, wavelengths

#
# Create a dichromat colour solid to do calculations on (dichromats are easy to plot)
#
solid = ColourSolid(example_fraction_yields[:, :2], wavelengths=wavelengths)


# Choose a point somewhere in the solid
p = array([0.30, 0.65])

# Find the spectrum of the boundary point
spectrum = solid.boundary_spectrum(p)

# Get the position of the boundary colour
p_boundary = solid.colour(spectrum)


#
# Top plot, the spectrum of the boundary colour
#

plt.subplot(1, 2, 1)


plt.plot(wavelengths, spectrum)

#
# Bottom plot - the colour solid
#

plt.subplot(1, 2, 2)

# Add the point, and the centre, to the plot
plt.scatter([0.5, p[0], p_boundary[0]], [0.5, p[1], p_boundary[1]])

# Add the solid to the plot
solid.draw_on(plt)

plt.show()