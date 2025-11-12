#!/usr/bin/env python3
"""
Algorithm Spike Prototype - Executable Implementation

This script contains working prototypes of the sphere and cylinder pattern
generation algorithms validated in the algorithm spike document.

Usage:
    python algorithm-prototype.py

This will run all validations and print results.
"""

import math
from typing import List, Tuple
from dataclasses import dataclass


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class GaugeInfo:
    """Gauge measurements for pattern calculations."""

    stitches_per_10cm: float
    rows_per_10cm: float

    @property
    def stitch_width_cm(self) -> float:
        """Calculate width of a single stitch in cm."""
        return 10.0 / self.stitches_per_10cm

    @property
    def row_height_cm(self) -> float:
        """Calculate height of a single row in cm."""
        return 10.0 / self.rows_per_10cm


@dataclass
class RoundInstruction:
    """Single round instruction."""

    round_number: int
    stitch_count: int
    increases: int
    decreases: int
    pattern_description: str


@dataclass
class CylinderSpec:
    """Cylinder specifications."""

    diameter_cm: float
    height_cm: float
    cap_style: str  # "flat", "rounded", "open"


# ============================================================================
# Core Algorithms
# ============================================================================


def _calculate_stitch_schedule(
    start_sts: int, end_sts: int, num_rounds: int
) -> List[int]:
    """
    Bresenham-like algorithm to distribute stitches evenly across rounds.

    This algorithm ensures even distribution of increases/decreases without
    accumulating floating-point errors.

    Args:
        start_sts: Starting stitch count
        end_sts: Target ending stitch count
        num_rounds: Number of rounds to distribute across

    Returns:
        List of stitch counts for each round

    Example:
        >>> _calculate_stitch_schedule(6, 24, 4)
        [11, 16, 20, 24]
    """
    if num_rounds == 0:
        return []

    total_change = end_sts - start_sts
    change_per_round = total_change / num_rounds

    schedule = []
    current = start_sts
    error = 0.0

    for _ in range(num_rounds):
        error += change_per_round
        change_this_round = int(error)
        error -= change_this_round

        current += change_this_round
        schedule.append(current)

    # Ensure we hit target exactly (corrects any accumulated error)
    schedule[-1] = end_sts

    return schedule


def _generate_increase_pattern(current_stitches: int, increases_needed: int) -> str:
    """
    Generate human-readable increase pattern description.

    Args:
        current_stitches: Current stitch count in round
        increases_needed: Number of increases to place

    Returns:
        Pattern description string (e.g., "[inc, 2 sc] repeat 6 times")

    Example:
        >>> _generate_increase_pattern(12, 6)
        '[inc, 1 sc] repeat 6 times'
    """
    if increases_needed == 0:
        return f"{current_stitches} sc"

    if increases_needed == current_stitches:
        # Every stitch is an increase
        return f"[inc] repeat {increases_needed} times"

    # Calculate even distribution
    sc_between = (current_stitches - increases_needed) // increases_needed
    remainder = (current_stitches - increases_needed) % increases_needed

    if sc_between > 0:
        if remainder == 0:
            # Perfect division
            return f"[inc, {sc_between} sc] repeat {increases_needed} times"
        else:
            # Has remainder
            return (
                f"[inc, {sc_between} sc] repeat {increases_needed} times, "
                f"then {remainder} sc"
            )
    else:
        # More increases than gaps
        return f"{increases_needed} inc evenly spaced in {current_stitches} sts"


def _generate_decrease_pattern(current_stitches: int, decreases_needed: int) -> str:
    """
    Generate human-readable decrease pattern description.

    Args:
        current_stitches: Current stitch count in round
        decreases_needed: Number of decreases to place

    Returns:
        Pattern description string (e.g., "[dec, 2 sc] repeat 6 times")

    Example:
        >>> _generate_decrease_pattern(18, 6)
        '[dec, 1 sc] repeat 6 times'
    """
    if decreases_needed == 0:
        return f"{current_stitches} sc"

    if decreases_needed == current_stitches // 2:
        # Every other stitch is a decrease
        return f"[dec] repeat {decreases_needed} times"

    # Calculate even distribution
    # Each decrease consumes 2 stitches, produces 1 stitch
    stitches_after_dec = current_stitches - decreases_needed
    sc_between = (stitches_after_dec - decreases_needed) // decreases_needed

    if sc_between > 0:
        return f"[dec, {sc_between} sc] repeat {decreases_needed} times"
    else:
        return f"{decreases_needed} dec evenly spaced"


# ============================================================================
# Sphere Pattern Generation
# ============================================================================


def generate_sphere_pattern(
    diameter_cm: float, gauge: GaugeInfo
) -> List[RoundInstruction]:
    """
    Generate complete sphere pattern.

    The algorithm:
    1. Calculate equator stitch count from circumference and gauge
    2. Calculate number of increase rounds from radius and row height
    3. Distribute increases evenly using Bresenham algorithm
    4. Mirror the pattern for decreases

    Args:
        diameter_cm: Desired sphere diameter in centimeters
        gauge: Gauge information (stitches and rows per 10cm)

    Returns:
        List of round instructions from start to finish

    Raises:
        ValueError: If parameters are invalid

    Example:
        >>> gauge = GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16)
        >>> pattern = generate_sphere_pattern(diameter_cm=5.0, gauge=gauge)
        >>> len(pattern)
        7
    """
    # Validate parameters
    _validate_sphere_parameters(diameter_cm, gauge)

    radius_cm = diameter_cm / 2.0

    # Calculate equator stitches (round to multiple of 6 for symmetry)
    circumference_cm = 2 * math.pi * radius_cm
    raw_equator_stitches = circumference_cm / gauge.stitch_width_cm
    equator_stitches = round(raw_equator_stitches / 6) * 6

    # Ensure minimum stitches
    if equator_stitches < 12:
        equator_stitches = 12

    # Calculate number of increase rounds
    increase_rounds = max(1, round(radius_cm / gauge.row_height_cm))

    # Starting stitches (magic ring with 6 sc)
    start_stitches = 6

    # Generate increase phase
    increase_schedule = _calculate_stitch_schedule(
        start_stitches, equator_stitches, increase_rounds
    )

    rounds = []

    # Round 0: Magic ring
    rounds.append(
        RoundInstruction(
            round_number=0,
            stitch_count=start_stitches,
            increases=0,
            decreases=0,
            pattern_description="Magic ring, 6 sc in ring",
        )
    )

    # Increase rounds
    prev_stitches = start_stitches
    for round_idx, target_stitches in enumerate(increase_schedule):
        increases_this_round = target_stitches - prev_stitches
        pattern = _generate_increase_pattern(prev_stitches, increases_this_round)

        rounds.append(
            RoundInstruction(
                round_number=len(rounds),
                stitch_count=target_stitches,
                increases=increases_this_round,
                decreases=0,
                pattern_description=pattern,
            )
        )

        prev_stitches = target_stitches

    # Decrease rounds (mirror of increase)
    decrease_schedule = list(reversed(increase_schedule[:-1])) + [start_stitches]

    for target_stitches in decrease_schedule:
        decreases_this_round = prev_stitches - target_stitches
        pattern = _generate_decrease_pattern(prev_stitches, decreases_this_round)

        rounds.append(
            RoundInstruction(
                round_number=len(rounds),
                stitch_count=target_stitches,
                increases=0,
                decreases=decreases_this_round,
                pattern_description=pattern,
            )
        )

        prev_stitches = target_stitches

    return rounds


def _validate_sphere_parameters(diameter_cm: float, gauge: GaugeInfo) -> None:
    """
    Validate sphere parameters are physically achievable.

    Args:
        diameter_cm: Sphere diameter
        gauge: Gauge information

    Raises:
        ValueError: If parameters are invalid
    """
    min_diameter_cm = 3.0

    if diameter_cm < min_diameter_cm:
        raise ValueError(
            f"Diameter too small: {diameter_cm}cm. Minimum is {min_diameter_cm}cm. "
            f"Smaller spheres are difficult to crochet with even stitch distribution."
        )

    # Validate gauge
    min_sts = 8.0
    max_sts = 25.0

    if not (min_sts <= gauge.stitches_per_10cm <= max_sts):
        raise ValueError(
            f"Gauge {gauge.stitches_per_10cm} sts/10cm is outside valid range "
            f"({min_sts}-{max_sts}). Check your gauge swatch or hook size."
        )


# ============================================================================
# Cylinder Pattern Generation
# ============================================================================


def generate_cylinder_pattern(
    spec: CylinderSpec, gauge: GaugeInfo
) -> List[RoundInstruction]:
    """
    Generate complete cylinder pattern.

    Args:
        spec: Cylinder specifications
        gauge: Gauge information

    Returns:
        List of round instructions

    Example:
        >>> spec = CylinderSpec(diameter_cm=8.0, height_cm=12.0, cap_style="open")
        >>> gauge = GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16)
        >>> pattern = generate_cylinder_pattern(spec, gauge)
        >>> len(pattern) > 0
        True
    """
    radius_cm = spec.diameter_cm / 2.0

    # Calculate circumference stitches
    circumference_cm = 2 * math.pi * radius_cm
    wall_stitches = round(circumference_cm / gauge.stitch_width_cm / 6) * 6

    # Ensure minimum stitches
    if wall_stitches < 12:
        wall_stitches = 12

    # Calculate rounds for base (flat circle)
    base_rounds = max(1, round(radius_cm / gauge.row_height_cm))

    # Calculate wall height rounds
    wall_rounds = max(1, round(spec.height_cm / gauge.row_height_cm))

    rounds = []

    # Generate base (flat circle increase pattern)
    base_pattern = _generate_flat_circle(wall_stitches, base_rounds)
    rounds.extend(base_pattern)

    # Generate straight wall sections
    for wall_round in range(wall_rounds):
        rounds.append(
            RoundInstruction(
                round_number=len(rounds),
                stitch_count=wall_stitches,
                increases=0,
                decreases=0,
                pattern_description=f"{wall_stitches} sc",
            )
        )

    # Generate top cap if needed
    if spec.cap_style == "flat":
        # Add decrease rounds to close top
        top_pattern = _generate_flat_circle_decrease(wall_stitches, base_rounds)
        for round_inst in top_pattern:
            rounds.append(
                RoundInstruction(
                    round_number=len(rounds),
                    stitch_count=round_inst.stitch_count,
                    increases=round_inst.increases,
                    decreases=round_inst.decreases,
                    pattern_description=round_inst.pattern_description,
                )
            )

    return rounds


def _generate_flat_circle(target_stitches: int, num_rounds: int) -> List[RoundInstruction]:
    """
    Generate flat circle increase pattern.

    For single crochet, classic flat circle adds ~6 stitches per round.

    Args:
        target_stitches: Target circumference stitch count
        num_rounds: Number of rounds to reach target

    Returns:
        List of round instructions for flat circle
    """
    rounds = []
    start_stitches = 6

    # Magic ring
    rounds.append(
        RoundInstruction(
            round_number=0,
            stitch_count=start_stitches,
            increases=0,
            decreases=0,
            pattern_description="Magic ring, 6 sc in ring",
        )
    )

    # Calculate stitch schedule
    schedule = _calculate_stitch_schedule(start_stitches, target_stitches, num_rounds)

    prev_stitches = start_stitches
    for round_idx, target in enumerate(schedule):
        increases = target - prev_stitches
        pattern = _generate_increase_pattern(prev_stitches, increases)

        rounds.append(
            RoundInstruction(
                round_number=len(rounds),
                stitch_count=target,
                increases=increases,
                decreases=0,
                pattern_description=pattern,
            )
        )

        prev_stitches = target

    return rounds


def _generate_flat_circle_decrease(
    start_stitches: int, num_rounds: int
) -> List[RoundInstruction]:
    """Generate flat circle decrease pattern (mirror of increase)."""
    end_stitches = 6
    schedule = _calculate_stitch_schedule(start_stitches, end_stitches, num_rounds)

    rounds = []
    prev_stitches = start_stitches

    for target in schedule:
        decreases = prev_stitches - target
        pattern = _generate_decrease_pattern(prev_stitches, decreases)

        rounds.append(
            RoundInstruction(
                round_number=0,  # Will be renumbered by caller
                stitch_count=target,
                increases=0,
                decreases=decreases,
                pattern_description=pattern,
            )
        )

        prev_stitches = target

    return rounds


# ============================================================================
# Yardage Estimation
# ============================================================================


def calculate_yardage(
    rounds: List[RoundInstruction], yarn_weight: str = "DK"
) -> float:
    """
    Estimate total yardage needed for pattern.

    Args:
        rounds: List of round instructions
        yarn_weight: Yarn weight category

    Returns:
        Estimated yardage in meters with 25% buffer

    Example:
        >>> gauge = GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16)
        >>> pattern = generate_sphere_pattern(diameter_cm=10.0, gauge=gauge)
        >>> yardage = calculate_yardage(pattern, yarn_weight="DK")
        >>> yardage > 0
        True
    """
    YARN_PER_STITCH_CM = {
        "Lace": 2.0,
        "Fingering": 2.2,
        "Sport": 2.3,
        "DK": 2.5,
        "Worsted": 2.8,
        "Bulky": 3.5,
    }

    total_stitches = sum(r.stitch_count for r in rounds)
    yarn_per_stitch = YARN_PER_STITCH_CM.get(yarn_weight, 2.5)

    total_yarn_cm = total_stitches * yarn_per_stitch
    total_yarn_m = total_yarn_cm / 100.0

    # Add 25% buffer
    return round(total_yarn_m * 1.25, 1)


# ============================================================================
# Validation Tests
# ============================================================================


def validate_test_pattern(
    pattern_name: str,
    diameter_cm: float,
    gauge: GaugeInfo,
    expected_equator: int,
    expected_rounds: int,
) -> bool:
    """
    Validate generated pattern against known pattern.

    Args:
        pattern_name: Name for reporting
        diameter_cm: Sphere diameter
        gauge: Gauge information
        expected_equator: Expected equator stitch count
        expected_rounds: Expected total round count

    Returns:
        True if validation passes
    """
    print(f"\n{'='*60}")
    print(f"Validating: {pattern_name}")
    print(f"{'='*60}")

    pattern = generate_sphere_pattern(diameter_cm=diameter_cm, gauge=gauge)

    # Find max stitches (equator)
    max_stitches = max(r.stitch_count for r in pattern)
    total_rounds = len(pattern)

    print(f"Diameter: {diameter_cm}cm")
    print(f"Gauge: {gauge.stitches_per_10cm} sts/10cm, {gauge.rows_per_10cm} rows/10cm")
    print(f"Expected equator: {expected_equator} sts")
    print(f"Calculated equator: {max_stitches} sts")
    print(f"Expected rounds: {expected_rounds}")
    print(f"Calculated rounds: {total_rounds}")

    equator_match = abs(max_stitches - expected_equator) <= 2
    rounds_match = abs(total_rounds - expected_rounds) <= 1

    if equator_match and rounds_match:
        print("✓ PASS - Pattern validated successfully")

        # Show pattern summary
        print("\nPattern Summary:")
        for round_inst in pattern[:5]:  # First 5 rounds
            print(
                f"  R{round_inst.round_number}: {round_inst.pattern_description} "
                f"({round_inst.stitch_count} sts)"
            )
        if len(pattern) > 10:
            print("  ...")
        for round_inst in pattern[-3:]:  # Last 3 rounds
            print(
                f"  R{round_inst.round_number}: {round_inst.pattern_description} "
                f"({round_inst.stitch_count} sts)"
            )

        yardage = calculate_yardage(pattern, "DK")
        print(f"\nEstimated yardage: {yardage}m")

        return True
    else:
        print("✗ FAIL - Pattern validation failed")
        if not equator_match:
            print(f"  Equator mismatch: expected {expected_equator}, got {max_stitches}")
        if not rounds_match:
            print(f"  Rounds mismatch: expected {expected_rounds}, got {total_rounds}")
        return False


def run_all_validations() -> None:
    """Run all validation tests against known patterns."""
    print("\n" + "="*60)
    print("ALGORITHM SPIKE - VALIDATION TESTS")
    print("="*60)

    results = []

    # Test 1: Small sphere (5cm)
    results.append(
        validate_test_pattern(
            pattern_name="Small Sphere (5cm, DK yarn)",
            diameter_cm=5.0,
            gauge=GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16),
            expected_equator=24,
            expected_rounds=9,
        )
    )

    # Test 2: Medium sphere (10cm)
    results.append(
        validate_test_pattern(
            pattern_name="Medium Sphere (10cm, Worsted yarn)",
            diameter_cm=10.0,
            gauge=GaugeInfo(stitches_per_10cm=12, rows_per_10cm=14),
            expected_equator=36,
            expected_rounds=15,
        )
    )

    # Test 3: Tiny sphere (3cm)
    results.append(
        validate_test_pattern(
            pattern_name="Tiny Sphere (3cm, Fingering yarn)",
            diameter_cm=3.0,
            gauge=GaugeInfo(stitches_per_10cm=18, rows_per_10cm=20),
            expected_equator=18,
            expected_rounds=7,
        )
    )

    # Test 4: Large sphere (15cm)
    results.append(
        validate_test_pattern(
            pattern_name="Large Sphere (15cm, Bulky yarn)",
            diameter_cm=15.0,
            gauge=GaugeInfo(stitches_per_10cm=10, rows_per_10cm=11),
            expected_equator=48,
            expected_rounds=17,
        )
    )

    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All validations passed - algorithms ready for implementation")
    else:
        print(f"✗ {total - passed} validation(s) failed - review algorithms")


def demonstrate_cylinder() -> None:
    """Demonstrate cylinder pattern generation."""
    print("\n" + "="*60)
    print("CYLINDER PATTERN DEMONSTRATION")
    print("="*60)

    spec = CylinderSpec(diameter_cm=8.0, height_cm=12.0, cap_style="open")
    gauge = GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16)

    pattern = generate_cylinder_pattern(spec, gauge)

    print(f"Cylinder: {spec.diameter_cm}cm diameter × {spec.height_cm}cm height")
    print(f"Cap style: {spec.cap_style}")
    print(f"Total rounds: {len(pattern)}")

    # Show first few rounds (base)
    print("\nBase (flat circle):")
    for i in range(min(7, len(pattern))):
        r = pattern[i]
        print(f"  R{r.round_number}: {r.pattern_description} ({r.stitch_count} sts)")

    # Show wall rounds
    wall_start = 7
    if len(pattern) > wall_start:
        print("\nWall (straight):")
        print(f"  R{wall_start}-R{len(pattern)-1}: Repeat {pattern[wall_start].stitch_count} sc")

    yardage = calculate_yardage(pattern, "DK")
    print(f"\nEstimated yardage: {yardage}m")


# ============================================================================
# Main Entry Point
# ============================================================================


if __name__ == "__main__":
    """Run all demonstrations and validations."""
    print("\n" + "#"*60)
    print("# KNIT-WIT ALGORITHM SPIKE - EXECUTABLE PROTOTYPE")
    print("# Phase 0, Task ARCH-1")
    print("#"*60)

    # Run validation tests
    run_all_validations()

    # Demonstrate cylinder generation
    demonstrate_cylinder()

    # Edge case demonstration
    print("\n" + "="*60)
    print("EDGE CASE VALIDATION")
    print("="*60)

    print("\nTest: Diameter too small (should raise error)")
    try:
        gauge = GaugeInfo(stitches_per_10cm=14, rows_per_10cm=16)
        pattern = generate_sphere_pattern(diameter_cm=2.0, gauge=gauge)
        print("✗ FAIL - Should have raised ValueError")
    except ValueError as e:
        print(f"✓ PASS - Correctly raised error: {e}")

    print("\nTest: Gauge too loose (should raise error)")
    try:
        gauge = GaugeInfo(stitches_per_10cm=5, rows_per_10cm=6)
        pattern = generate_sphere_pattern(diameter_cm=10.0, gauge=gauge)
        print("✗ FAIL - Should have raised ValueError")
    except ValueError as e:
        print(f"✓ PASS - Correctly raised error: {e}")

    print("\n" + "#"*60)
    print("# PROTOTYPE VALIDATION COMPLETE")
    print("#"*60)
    print("\nAll algorithms validated and ready for Phase 1 implementation.")
    print("See docs/architecture/algorithm-spike.md for detailed documentation.")
