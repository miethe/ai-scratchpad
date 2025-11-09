"""
Gauge Calculation Utilities

Functions for working with crochet gauge measurements, unit conversions,
and yarn estimation calculations.
"""

from typing import Dict, Tuple
import numpy as np


def calculate_gauge_adjustments(
    target_stitches_per_cm: float,
    actual_stitches_per_cm: float,
    target_rows_per_cm: float,
    actual_rows_per_cm: float,
) -> Dict[str, float]:
    """
    Calculate adjustment factors when actual gauge differs from target gauge.

    Args:
        target_stitches_per_cm: Intended gauge for stitches
        actual_stitches_per_cm: Measured gauge for stitches
        target_rows_per_cm: Intended gauge for rows
        actual_rows_per_cm: Measured gauge for rows

    Returns:
        Dictionary containing adjustment factors and recommendations

    Example:
        >>> adjustments = calculate_gauge_adjustments(3.0, 2.8, 3.5, 3.3)
        >>> print(adjustments['stitch_adjustment_factor'])
        1.071

    Note:
        Stub implementation. Will be enhanced in Phase 1.
    """
    stitch_factor = target_stitches_per_cm / actual_stitches_per_cm
    row_factor = target_rows_per_cm / actual_rows_per_cm

    return {
        "stitch_adjustment_factor": round(stitch_factor, 3),
        "row_adjustment_factor": round(row_factor, 3),
        "recommendation": _generate_gauge_recommendation(stitch_factor, row_factor),
    }


def convert_inches_to_cm(inches: float) -> float:
    """
    Convert inches to centimeters.

    Args:
        inches: Measurement in inches

    Returns:
        Measurement in centimeters
    """
    return inches * 2.54


def convert_cm_to_inches(cm: float) -> float:
    """
    Convert centimeters to inches.

    Args:
        cm: Measurement in centimeters

    Returns:
        Measurement in inches
    """
    return cm / 2.54


def estimate_yarn_length(
    total_stitches: int,
    stitches_per_cm: float,
    avg_yarn_per_stitch_cm: float = 2.5,
) -> Tuple[float, str]:
    """
    Estimate total yarn length needed for a pattern.

    Args:
        total_stitches: Total number of stitches in the pattern
        stitches_per_cm: Gauge measurement
        avg_yarn_per_stitch_cm: Average yarn consumed per stitch (default: 2.5cm)

    Returns:
        Tuple of (total_meters, formatted_string)

    Note:
        This is a rough estimate. Actual yarn consumption varies by stitch type,
        tension, and yarn characteristics. Stub for Phase 1.
    """
    total_cm = total_stitches * avg_yarn_per_stitch_cm
    total_meters = total_cm / 100

    # Add 20% buffer for safety
    total_meters_with_buffer = total_meters * 1.2

    formatted = f"{total_meters_with_buffer:.1f}m (includes 20% buffer)"

    return total_meters_with_buffer, formatted


def _generate_gauge_recommendation(
    stitch_factor: float, row_factor: float
) -> str:
    """
    Generate human-readable gauge adjustment recommendation.

    Args:
        stitch_factor: Stitch adjustment factor
        row_factor: Row adjustment factor

    Returns:
        Recommendation string

    Note:
        Stub for Phase 1 implementation.
    """
    # Simplified recommendation logic
    if abs(stitch_factor - 1.0) < 0.05 and abs(row_factor - 1.0) < 0.05:
        return "Gauge is close to target. Proceed with pattern."

    recommendations = []

    if stitch_factor > 1.05:
        recommendations.append("Try a smaller hook size to increase stitch density")
    elif stitch_factor < 0.95:
        recommendations.append("Try a larger hook size to decrease stitch density")

    if row_factor > 1.05:
        recommendations.append("Rows are too loose - adjust tension or hook size")
    elif row_factor < 0.95:
        recommendations.append("Rows are too tight - adjust tension or hook size")

    return "; ".join(recommendations) if recommendations else "Gauge is acceptable"


def calculate_stitch_distribution(
    total_stitches: int, num_sections: int
) -> np.ndarray:
    """
    Distribute stitches evenly across sections with remainder handling.

    Args:
        total_stitches: Total number of stitches to distribute
        num_sections: Number of sections to distribute across

    Returns:
        Array of stitch counts for each section

    Note:
        Stub for Phase 1 implementation.
    """
    base_stitches = total_stitches // num_sections
    remainder = total_stitches % num_sections

    distribution = np.full(num_sections, base_stitches)
    # Distribute remainder evenly
    distribution[:remainder] += 1

    return distribution
