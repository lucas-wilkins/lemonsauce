from .spectrumtools import template_pigment, d65, extreme_spectrum, \
    total_absorption, total_transmission, reflectance_to_rgb, spectrum_to_rgb

from .solidtools import ColourSolid as ColourSolid

__all__ = ["ColourSolid",
           "template_pigment", "d65", "extreme_spectrum",
           "total_absorption", "total_transmission",
           "reflectance_to_rgb", "spectrum_to_rgb"]

