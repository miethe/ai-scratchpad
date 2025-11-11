"""
Even Distribution Algorithm

This module implements algorithms for evenly distributing increases or decreases
around a round's circumference in crochet patterns. The algorithms prevent visible
columns or stacking by spacing changes as uniformly as possible.

The core algorithm uses a Bresenham-like line-drawing approach to achieve optimal
spacing even when total stitches don't divide evenly by the number of changes.

Example:
    >>> # Distribute 6 increases evenly in 36 stitches
    >>> indices = even_distribution(36, 6)
    >>> print(indices)
    [6, 12, 18, 24, 30, 36]

    >>> # Every 6th stitch is an increase
    >>> # With offset for next round to prevent column stacking
    >>> indices_r2 = even_distribution(42, 7, offset=3)
    >>> print(indices_r2)
    [3, 9, 15, 21, 27, 33, 39]
"""

from typing import List


def even_distribution(total_stitches: int, num_changes: int, offset: int = 0) -> List[int]:
    """
    Calculate stitch indices for evenly distributed changes.

    Uses a Bresenham-like line-drawing algorithm to space changes as evenly as possible.
    This ensures that increases or decreases are distributed around the round's circumference
    without creating visible columns or stacking patterns.

    The algorithm handles both perfect division (e.g., 36 stitches, 6 changes) and
    imperfect division (e.g., 37 stitches, 6 changes) by ensuring maximum gap equals
    minimum gap plus 1.

    Args:
        total_stitches: Total number of stitches in the round (must be positive)
        num_changes: Number of increases or decreases to place (must be non-negative)
        offset: Starting offset for jittering across rounds (default: 0)

    Returns:
        List of stitch indices (1-indexed) where changes occur, in ascending order.
        Returns empty list if num_changes <= 0.

    Examples:
        >>> # Perfect division: 6 changes in 36 stitches
        >>> even_distribution(36, 6)
        [6, 12, 18, 24, 30, 36]

        >>> # Imperfect division: 6 changes in 37 stitches
        >>> even_distribution(37, 6)
        [6, 12, 18, 25, 31, 37]

        >>> # With offset to prevent column stacking
        >>> even_distribution(36, 6, offset=3)
        [3, 9, 15, 21, 27, 33]

        >>> # Offset with wrapping: 7 changes in 42 stitches
        >>> even_distribution(42, 7, offset=3)
        [3, 9, 15, 21, 27, 33, 39]

        >>> # Edge case: no changes
        >>> even_distribution(20, 0)
        []

        >>> # Edge case: changes equal stitches
        >>> even_distribution(5, 5)
        [1, 2, 3, 4, 5]

    Notes:
        - Indices are 1-indexed to match crochet pattern conventions
        - For num_changes >= total_stitches, returns one change per stitch
        - Indices that exceed total_stitches wrap around (e.g., index 45 in a
          42-stitch round wraps to index 3) to ensure all indices are valid
        - Deterministic output for same input parameters
        - Wrapping behavior ensures indices remain in range [1, total_stitches]
    """
    if num_changes <= 0:
        return []

    if num_changes >= total_stitches:
        # One change per stitch
        return list(range(1, total_stitches + 1))

    indices = []
    gap = total_stitches / num_changes
    position = offset

    for i in range(num_changes):
        # Round to nearest integer position
        stitch_index = int(round(position + gap))

        # Handle wrap-around for offset
        if stitch_index > total_stitches:
            stitch_index -= total_stitches

        # Ensure we're in valid 1-indexed range
        if stitch_index < 1:
            stitch_index = 1

        indices.append(stitch_index)
        position += gap

    return sorted(indices)


def jitter_offset(round_number: int, base_offset: int = 0) -> int:
    """
    Calculate jittered offset for consecutive rounds to avoid column stacking.

    When working multiple rounds with increases or decreases, placing them at the
    same positions creates visible vertical columns. This function generates an
    offset that shifts the positions slightly between rounds, creating a more
    natural spiral appearance.

    The jitter alternates by round number, creating a simple but effective
    staggering pattern that distributes visual weight evenly.

    Args:
        round_number: Current round number (1-indexed, must be positive)
        base_offset: Base offset to add to jitter (default: 0)

    Returns:
        Offset value to pass to even_distribution()

    Examples:
        >>> # Alternate offset for consecutive rounds
        >>> jitter_offset(1)
        3
        >>> jitter_offset(2)
        0
        >>> jitter_offset(3)
        3
        >>> jitter_offset(4)
        0

        >>> # With base offset
        >>> jitter_offset(1, base_offset=5)
        8
        >>> jitter_offset(2, base_offset=5)
        5

    Notes:
        - Simple alternating pattern: odd rounds get +3 offset
        - Can be combined with base_offset for more complex patterns
        - The value 3 is chosen as a good default for most stitch patterns
    """
    # Simple jitter: alternate offset by half-gap
    jitter = (round_number % 2) * 3
    return base_offset + jitter
