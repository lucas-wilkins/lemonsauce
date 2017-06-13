
     __       _______ .___  ___.   ______   .__   __.      _______.     ___      __    __    ______  _______
    |  |     |   ____||   \/   |  /  __  \  |  \ |  |     /       |    /   \    |  |  |  |  /      ||   ____|
    |  |     |  |__   |  \  /  | |  |  |  | |   \|  |    |   (----`   /  ^  \   |  |  |  | |  ,----'|  |__
    |  |     |   __|  |  |\/|  | |  |  |  | |  . `  |     \   \      /  /_\  \  |  |  |  | |  |     |   __|
    |  `----.|  |____ |  |  |  | |  `--'  | |  |\   | .----)   |    /  _____  \ |  `--'  | |  `----.|  |____
    |_______||_______||__|  |__|  \______/  |__| \__| |_______/    /__/     \__\ \______/   \______||_______|

                                       The Colour Solid Python Library



About
=====

Lemonsauce is a python 3 package for performing calculations involving colour solids
for arbitrary observers.

Features
--------

* Get the geometry for colour solids with any dimension
* Plotting tools for matplotlib
* Export tools compatible with 3D rendering tools such as blender.
* Calculation of vividness
* Implementation of related functions
  * Pigment templates
  * Extreme spectra
  * Some human colourmetric functions

Examples
========

A number of full examples can be found in the `examples` directory.
There is a dedicated README.md explaining them in that direction.

But here is a basic example, displaying a colour solid in 2D:

```python

# Get some example data from the examples package
from examples.fractional_yields import example_fraction_yields

# Import the ColourSolid class
from lemonsauce import ColourSolid

# Create a dicromat ColourSolid
solid = ColourSolid(example_fraction_yields[:, :2])

# Show the solid (`draw_on(<pyplot object>)` can be used too)
solid.draw()
```

Licencing
=========

Lemonsauce is licenced under a Creative Commons
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
A copy of the licence is in the root folder in the file 'licence.txt'.

This excludes the human colourmetric data in the files
'cie64.txt' and 'd65.txt' which was obtained from the
[UCL Opthalmology Lab](http://www.cvrl.org/).
They give the following conditions for its use.

> The information and data on this website are provided free of charge
> as a service to the vision science community. They were believed to be
> correct at the time of posting. Their use and any consequences arising
> from their use are the sole responsibility of the user.


Notes
=====

* This library is written to work with numpy. Methods will
often expect to have arrays as input, and generally there is no check that this is so.