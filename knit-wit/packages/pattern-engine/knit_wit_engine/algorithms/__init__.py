"""
Pattern Generation Algorithms

This module contains algorithms for generating crochet patterns for various 3D shapes.
Each algorithm takes shape parameters and gauge information to produce stitch-by-stitch
instructions following the Knit-Wit Pattern DSL.
"""

from knit_wit_engine.algorithms.sphere import generate_sphere
from knit_wit_engine.algorithms.cylinder import generate_cylinder
from knit_wit_engine.algorithms.cone import generate_cone
from knit_wit_engine.algorithms.gauge import (
    gauge_to_stitch_length,
    estimate_yardage,
)

__all__ = [
    "generate_sphere",
    "generate_cylinder",
    "generate_cone",
    "gauge_to_stitch_length",
    "estimate_yardage",
]
