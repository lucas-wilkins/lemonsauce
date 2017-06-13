"""

Colour Solid from Linear Programming
====================================

This example shows how to calculate the colour
solid geometry using a linear programming method.

The linear programming routine is built in to the
ColourSolid object, but it is not used for its
default rendering.

This example also shows how to assign RGB values to spectra.

"""

from numpy import array, arange, pi, sin, cos

# We will plot this
import matplotlib.pyplot as plt

# Imports from main packages
from lemonsauce import ColourSolid
from lemonsauce import reflectance_to_rgb

# We will use the example data
from examples.fractional_yields import example_fraction_yields, wavelengths

#
# We do a two dimensional case for simplicity, we use entries 0 and 2 to better demonstrate
# the colour mapping used for rendering.
#

solid = ColourSolid(example_fraction_yields[:, (0, 2)], wavelengths=wavelengths)

# Sample the angles around a point
angles = arange(0, 1, 0.05)

for a in angles:

    # Convert angles to points around the centre of the solid
    x = 0.5 * (1 + sin(2*pi*a))
    y = 0.5 * (1 + cos(2*pi*a))

    # solid.boundary_spectrum uses a linear programming method
    spec = solid.boundary_spectrum(array([x, y]))
    colour = solid.colour(spec)

    plot_colour = reflectance_to_rgb(wavelengths, spec)

    plt.scatter([colour[0]], [colour[1]], color=plot_colour)

    # It's a bit slow, so a printout let's us know that something is going on!
    print("%d deg. : %.4g, %.4g" % (a*360, x, y))

    plt.plot([0.5, colour[0]], [0.5, colour[1]], 'k:')

# Show the solid calculated in the normal way as a comparison
solid.draw_on(plt, limit=False)

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])

plt.show()


