
"""

Colour Solid Rendering Example
==============================

This shows examples of creating colour solids and

* Plotting them using matplotlib
* Outputting them to an obj file that can be opened in 3D applications

There are two different plots. The first one shows the default views of
the colour solid, the dicromat solid has different kinds of slicing enabled

For higher dimensions than 3 it is hard to show detail. In this case we just the
orthogonal projection of the colour solid into various planes. We show this in
the second plot.

"""

from numpy import zeros, array, transpose

# For plotting we need matplotlib
import matplotlib.pyplot as plt

# The ColourSolid class does all the work
from lemonsauce import ColourSolid

#
#
# Load some example data from example_fractional_yields script
#
#

from examples.fractional_yields import example_fraction_yields

#
#
# Create the colour solids
#
#


# Monochromat solid, using just the first of the example yield functions
s1 = ColourSolid(example_fraction_yields[:, :1])

# Dichromat solid, first two example yield functions
s2 = ColourSolid(example_fraction_yields[:, :2])

# Trichromat solid, first three example yield functions
s3 = ColourSolid(example_fraction_yields[:, :3])

# Tetrachromat solid, first four example yield functions, increase the tolerance for quicker calculations (default=0.05)
s4 = ColourSolid(example_fraction_yields[:, :4], simplify_tolerance=0.1)

#
#
#     First plot.
#
# Use the draw_on method to plot it onto the matplotlib object, plt
#
#

plt.subplot(2, 3, 1)
s1.draw_on(plt_obj=plt)
plt.title("Monochromat")

plt.subplot(2, 3, 2)
s2.draw_on(plt_obj=plt)
plt.title("Dichromat")

plt.subplot(2, 3, 3)
s2.draw_on(plt_obj=plt, slices=False)
plt.title("Trichromat - no slicing")


plt.subplot(2, 3, 4)
s3.draw_on(plt_obj=plt, direction=[0, 0, 1])
plt.title("Trichromat (slices in z plane)")


plt.subplot(2, 3, 5)
s3.draw_on(plt_obj=plt, direction=[1, 1, 1])
plt.title("Trichromat (slices perpendicular to major diagonal)")


plt.subplot(2, 3, 6)
s3.draw_on(plt_obj=plt, direction=[1, 1, 0.1])
plt.title("Trichromat (slices almost perp. to XY)")


plt.show()

#
#
#    Second Plot.
#
# Tetrachromat solid, various perspectives
#
#

# Projection matrix for xy plane
projection = zeros((4, 2), dtype=float)
projection[0, 0] = 1.0
projection[1, 1] = 1.0

plt.subplot(2, 2, 1)
s4.draw_on(plt_obj=plt, projection=projection)
plt.title("XY plane")

#
# Projection matrix for zw plane
projection = zeros((4, 2), dtype=float)
projection[2, 0] = 1.0
projection[3, 1] = 1.0

plt.subplot(2, 2, 2)
s4.draw_on(plt_obj=plt, projection=projection)
plt.title("ZW plane")

#
#  Projection matrix for xz plane
projection = zeros((4, 2), dtype=float)
projection[0, 0] = 1.0
projection[2, 1] = 1.0

plt.subplot(2, 2, 3)
s4.draw_on(plt_obj=plt, projection=projection)
plt.title("XZ plane")

#
# Projection matrix for diagonal and perpendicular
projection = transpose(array([
    [1,  1,  1,  1],
    [1, -1,  1, -1]
], dtype=float))

plt.subplot(2, 2, 4)
s4.draw_on(plt_obj=plt, projection=projection, limit=False)
plt.title("Diagonal")

plt.show()

#
#
#   Export Example
#
# For dichromats and trichromats we can write solids to obj files
#

s2.write_obj("test_solid_2d.obj")
s3.write_obj("test_solid_3d.obj")


