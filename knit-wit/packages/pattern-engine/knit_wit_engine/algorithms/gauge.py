"""
Gauge Mapping and Yardage Estimation Algorithms

This module provides functions for converting gauge measurements into stitch dimensions
and estimating yarn yardage requirements for crochet patterns.

Performance Target: < 1ms per function call
"""

from typing import Literal
from knit_wit_engine.models.requests import Gauge


# Type alias for supported yarn weights
YarnWeight = Literal["Baby", "DK", "Worsted", "Bulky"]


def gauge_to_stitch_length(gauge: Gauge, yarn_weight: str) -> float:
    """
    Calculate average stitch length in centimeters based on gauge and yarn weight.

    This function computes the physical length of yarn consumed per stitch by combining
    the gauge measurement (stitches per unit length) with an empirical yarn weight factor.
    The yarn weight factor accounts for the additional yarn consumed in the stitch loop
    beyond the simple horizontal span.

    Args:
        gauge: Gauge object containing sts_per_10cm and rows_per_10cm measurements
        yarn_weight: Yarn weight category - one of 'Baby', 'DK', 'Worsted', 'Bulky'
                    (case-sensitive). Unknown weights default to Worsted factor (0.7)

    Returns:
        Average stitch length in centimeters (float)

    Algorithm:
        1. Calculate base stitch length from horizontal gauge: 10cm / sts_per_10cm
        2. Apply empirical yarn weight factor:
           - Baby (fingering): 0.5x multiplier (fine yarn, tight loops)
           - DK (light worsted): 0.6x multiplier
           - Worsted (medium): 0.7x multiplier (default)
           - Bulky (chunky): 0.9x multiplier (thick yarn, larger loops)
        3. Return base_length × factor

    Examples:
        >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        >>> stitch_length = gauge_to_stitch_length(gauge, "Worsted")
        >>> print(f"{stitch_length:.3f} cm")
        0.500 cm

        >>> # Fine gauge with DK yarn
        >>> gauge_fine = Gauge(sts_per_10cm=18, rows_per_10cm=20)
        >>> stitch_length = gauge_to_stitch_length(gauge_fine, "DK")
        >>> print(f"{stitch_length:.3f} cm")
        0.333 cm

        >>> # Coarse gauge with bulky yarn
        >>> gauge_coarse = Gauge(sts_per_10cm=10, rows_per_10cm=12)
        >>> stitch_length = gauge_to_stitch_length(gauge_coarse, "Bulky")
        >>> print(f"{stitch_length:.3f} cm")
        0.900 cm

    Performance:
        Executes in < 1ms (simple arithmetic operations)

    Notes:
        - The yarn weight factors are empirical values based on typical stitch geometry
        - For unknown yarn weights, defaults to Worsted factor (0.7)
        - This is a simplification; actual stitch consumption varies by:
          - Stitch type (sc, hdc, dc use different amounts)
          - Crocheter tension
          - Yarn elasticity and texture
          - Hook size relative to yarn weight
    """
    # Calculate base stitch length from horizontal gauge
    base_length = 10.0 / gauge.sts_per_10cm

    # Empirical yarn weight multipliers
    # Based on typical yarn loop geometry for each weight category
    weight_factors = {
        'Baby': 0.5,      # Fine yarn, small loops
        'DK': 0.6,        # Light worsted, medium-small loops
        'Worsted': 0.7,   # Standard medium weight
        'Bulky': 0.9      # Thick yarn, large loops
    }

    # Get factor for specified yarn weight, default to Worsted if unknown
    factor = weight_factors.get(yarn_weight, 0.7)

    return base_length * factor


def estimate_yardage(stitch_count: int, stitch_length: float) -> float:
    """
    Estimate total yarn yardage required for a pattern in meters.

    Calculates the total yarn length needed based on the number of stitches and
    the average yarn consumed per stitch. Includes a 10% waste factor to account
    for:
    - Yarn ends and weaving in
    - Gauge swatching
    - Potential frogging (ripping out) and rework
    - Yarn breakage or defects

    Args:
        stitch_count: Total number of stitches in the pattern (integer)
        stitch_length: Average length of yarn per stitch in centimeters (float)
                      Typically obtained from gauge_to_stitch_length()

    Returns:
        Estimated yarn yardage in meters (float), including 10% waste factor

    Algorithm:
        1. Calculate raw yarn length: stitch_count × stitch_length (in cm)
        2. Convert to meters: total_cm / 100
        3. Apply 10% waste factor: total_meters × 1.1

    Examples:
        >>> # Small amigurumi sphere (~200 stitches)
        >>> yardage = estimate_yardage(stitch_count=200, stitch_length=0.5)
        >>> print(f"{yardage:.1f}m")
        1.1m

        >>> # Medium project (~1000 stitches, worsted)
        >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        >>> stitch_len = gauge_to_stitch_length(gauge, "Worsted")
        >>> yardage = estimate_yardage(1000, stitch_len)
        >>> print(f"{yardage:.1f}m")
        5.5m

        >>> # Large project with bulky yarn (~800 stitches)
        >>> gauge_bulky = Gauge(sts_per_10cm=10, rows_per_10cm=12)
        >>> stitch_len = gauge_to_stitch_length(gauge_bulky, "Bulky")
        >>> yardage = estimate_yardage(800, stitch_len)
        >>> print(f"{yardage:.1f}m")
        7.9m

    Performance:
        Executes in < 1ms (simple arithmetic operations)

    Notes:
        - This is an estimate; actual yarn consumption varies by:
          - Stitch type mix (sc vs. dc vs. increases/decreases)
          - Individual crocheter tension
          - Yarn characteristics (elasticity, texture)
          - Pattern complexity (more ends = more waste)
        - The 10% waste factor is conservative for most projects
        - For very small projects (<5m), consider a larger buffer (15-20%)
        - For colorwork or multiple yarn changes, increase waste factor

    Accuracy:
        Typical estimate accuracy is ±10% for standard single-color patterns.
        Accuracy decreases for:
        - Mixed stitch types (not accounted for in current model)
        - Extreme gauge variations (very fine or very coarse)
        - Complex colorwork or texture patterns
    """
    # Calculate total yarn length in centimeters
    total_cm = stitch_count * stitch_length

    # Convert to meters
    total_meters = total_cm / 100.0

    # Apply 10% waste factor for safety margin
    return total_meters * 1.1
