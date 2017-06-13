from .A1Pigment import visual_pigment as template_pigment
from .cie_d65 import d65
from .extreme import extreme_spectrum
from .util import total_absorption, total_transmission
from .human import reflectance_to_rgb, spectrum_to_rgb

__all__ = [
    "template_pigment", "d65", "extreme_spectrum",
    "total_absorption", "total_transmission",
    "reflectance_to_rgb", "spectrum_to_rgb"]

