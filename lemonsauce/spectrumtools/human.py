""" Human data"""

import os

from numpy import array, interp, dot

from .cie_d65 import d65


def make_safe(rgb_value):
    """ Make sure rgb values are in [0,1] """
    return array([0.0 if v < 0.0 else 1.0 if v > 1.0 else v for v in rgb_value])


def srgb(rgb_value):
    """ Convert from RGB to sRGB"""
    return array([
        12.95 * x if x <= 0.0031308 else 1.055 * (x ** (1.0 / 2.4)) - 0.055
            for x in rgb_value])

# Matrix to convert from CIE XYZ to LMS space
xyz2lms = array([
    [ 0.38971,  0.68898, -0.07868],
    [-0.22981,  1.18340,  0.04641],
    [ 0.00000,  0.00000,  1.00000]
    ])

# Matrix ro convert from CIE XYZ to RGB coordinate for display
xyz2rgb = array([
    [ 3.2406, -1.5372, -0.4986],
    [-0.9689,  1.8758,  0.0415],
    [ 0.0557, -0.2040,  1.0570]
    ])

_loaded_xyz_10deg = None

def cie_xyz_10deg(wavelengths: array):
    """Human XYZ data, CIE 1964

    Args:
        wavelengths (array): Wavelengths which the data is to be got

    Returns:
        tuple of (x,y,z) spectra

    """

    # We cache the data so that we don't need to read it every time
    global _loaded_xyz_10deg

    if _loaded_xyz_10deg is None:

        # Load data from file
        filename = os.path.join(os.path.dirname(__file__), 'cie64.txt')
        fid = open(filename, 'r')

        els = []
        for line in fid:
            els.append(map(float, line.split()))

        fid.close()

        file_wls, x, y, z = zip(*els)

        _loaded_xyz_10deg = file_wls, x, y, z

    file_wls, x, y, z = _loaded_xyz_10deg

    xi = interp(wavelengths, file_wls, x, left=0.0, right=0.0)
    yi = interp(wavelengths, file_wls, y, left=0.0, right=0.0)
    zi = interp(wavelengths, file_wls, z, left=0.0, right=0.0)

    return array([xi, yi, zi])


def spectrum_to_rgb(wavelengths: array, spectrum: array):
    """ Get an approximation of a spectrum's colour under D65 illumination.

        Args:
            wavelengths (array): Wavelengths at which the reflectance spectrum is measured.
            reflectance (array): Reflectance at each wavelength


        Return:
            RGB coordinates approximating the light's appearance in standard conditions
        """

    xyz_funds = cie_xyz_10deg(wavelengths)

    xyz = dot(xyz_funds, spectrum)

    return make_safe(srgb(dot(xyz2rgb, xyz)))


def reflectance_to_rgb(wavelengths: array, reflectance: array):
    """ Get an approximation of a reflectance spectrum's colour under D65 illumination.

    Args:
        wavelengths (array): Wavelengths at which the reflectance spectrum is measured.
        reflectance (array): Reflectance at each wavelength


    Return:
        RGB coordinates approximating the reflectance's appearance in standard conditions
    """

    illum = d65(wavelengths, normalise=True)
    incident = illum*reflectance

    return spectrum_to_rgb(wavelengths, incident)


