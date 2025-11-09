"""
Utility Functions

This module contains helper functions for gauge calculations, unit conversions,
and other common operations used across the pattern engine.
"""

from knit_wit_engine.utils.gauge import (
    calculate_gauge_adjustments,
    convert_inches_to_cm,
    convert_cm_to_inches,
    estimate_yarn_length,
)

__all__ = [
    "calculate_gauge_adjustments",
    "convert_inches_to_cm",
    "convert_cm_to_inches",
    "estimate_yarn_length",
]
