"""
Shape Compiler Modules

This package contains shape-specific pattern compilers that generate complete
PatternDSL structures for various 3D crochet forms.

Each shape compiler:
- Takes dimensional parameters (diameter, height, etc.) and gauge
- Generates round-by-round instructions using core algorithms
- Returns fully-formed PatternDSL objects

Available Compilers:
- SphereCompiler: Generates spiral-round single crochet spheres
- CylinderCompiler: Generates cylindrical patterns with optional caps
- ConeCompiler: (Future) Generates tapered/conical patterns
"""

from knit_wit_engine.shapes.sphere import SphereCompiler
from knit_wit_engine.shapes.cylinder import CylinderCompiler

__all__ = ["SphereCompiler", "CylinderCompiler"]
