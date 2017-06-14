"""

Data Access
===========

Example of how to work with the raw data in the colour solid objects.

Introduces the `points`, `edges`, `faces`, `cells` and `simplices` methods `ColourSolid`

"""

# For plotting we need matplotlib
import matplotlib.pyplot as plt

# The ColourSolid class does all the work
from lemonsauce import ColourSolid

#
# Create some colour solids to work with.
#
# [plotting_and_exporting.py and fractional_yields.py has more detailed information on this]
#

from lemonsauce_examples.fractional_yields import example_fraction_yields

s1 = ColourSolid(example_fraction_yields[:, :1])  # Monochromat
s2 = ColourSolid(example_fraction_yields[:, :2])  # Dichromat
s3 = ColourSolid(example_fraction_yields[:, :3])  # Trichromat
s4 = ColourSolid(example_fraction_yields[:, :4], simplify_tolerance=0.1) # Tetrachromat

#
#
#   Examine the colour solids data
#   ==============================
#
#

#
# The monochromat solid's data has nothing very interesting, just two points
#

print("Monochromat data:")
print(s1.points)

#
# A dichromat has points and edges, we can use these manually
#

points = s2.points
edges = s2.highest_dimension_simplices

print()
print("Dichromat data:")
print("Point data shape: ", points.shape, " type: ", points.dtype)
print(" Edge data shape: ", edges.shape, " type: ", edges.dtype)
print()

for edge in edges:
    # Get the x coordinates of the 2 edge points
    x = points[edge, 0]

    # Get the y coordinates of the 2 edge points
    y = points[edge, 1]

    # Draw a line for each one
    plt.plot(x, y)

plt.show()

#
# A trichromat has points, edges and faces
#

points = s3.points
edges = s3.edges
faces = s3.faces

print()
print("Trichromat data:")
print("Point data shape: ", points.shape, " type: ", points.dtype)
print(" Edge data shape: ", edges.shape, " type: ", edges.dtype)
print(" Face data shape: ", faces.shape, " type: ", faces.dtype)
print()

# We can plot a 2D projection of the edges, but it is very slow
plt.subplot(1, 2, 1)
for edge in edges:
    # Get the x coordinates of the 2 edge points
    x = points[edge, 0]

    # Get the y coordinates of the 2 edge points
    y = points[edge, 1]

    # Draw a closed loop
    plt.plot(x, y)


# We can easily plot a 2D projection of the faces
plt.subplot(1, 2, 2)
for face in faces:
    # Get the x coordinates of the 3 face points
    x = points[face, 0]

    # Get the y coordinates of the 3 face points
    y = points[face, 1]

    # Draw a closed loop
    plt.fill(x, y, fill=False)

plt.show()

#
# A tetrachromat has points, edges, faces and cells
#

points = s4.points
edges = s4.edges
faces = s4.faces
cells = s4.cells

print()
print("Tetrachromat data:")
print("Point data shape: ", points.shape, " type: ", points.dtype)
print(" Edge data shape: ", edges.shape, " type: ", edges.dtype)
print(" Face data shape: ", faces.shape, " type: ", faces.dtype)
print(" Cell data shape: ", cells.shape, " type: ", cells.dtype)
print()

#
# One can also use the more general function, `.simplices(dimension)`
#  Note that the simplices(0) does not give point positions, but
#  like all other calls, returns an array of integers indexing `.points`
#

points = s4.simplices(0)
edges = s4.simplices(1)
faces = s4.simplices(2)
cells = s4.simplices(3)


print()
print("Tetrachromat data using alternative accessor:")
print("simplices(0) data shape: ", points.shape, " type: ", points.dtype)
print("simplices(1) data shape: ", edges.shape, " type: ", edges.dtype)
print("simplices(2) data shape: ", faces.shape, " type: ", faces.dtype)
print("simplices(3) data shape: ", cells.shape, " type: ", cells.dtype)
print()
