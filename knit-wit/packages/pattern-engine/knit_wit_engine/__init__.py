"""
Knit-Wit Pattern Engine

A parametric crochet pattern generation library for creating 3D geometric shapes.
"""

__version__ = "0.1.0"
__author__ = "Knit-Wit Project"
__description__ = "Parametric crochet pattern generation engine"

from knit_wit_engine.algorithms import generate_sphere, generate_cylinder, generate_cone
from knit_wit_engine.models import PatternDSL, StitchInstruction
from knit_wit_engine.utils import calculate_gauge_adjustments

__all__ = [
    "__version__",
    "generate_sphere",
    "generate_cylinder",
    "generate_cone",
    "PatternDSL",
    "StitchInstruction",
    "calculate_gauge_adjustments",
]
