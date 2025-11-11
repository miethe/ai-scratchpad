"""
Cone/Tapered Limb Pattern Compiler

Generates complete crochet patterns for tapered cylindrical shapes (cones) using
spiral rounds and single crochet stitches. Implements Bresenham-like distribution
algorithm to smoothly transition from one diameter to another without visible stacking.

The compiler uses a line-drawing algorithm to distribute increases or decreases
evenly across the height of the cone, ensuring a smooth, monotonic taper that
is visually appealing and structurally sound.

Critical for amigurumi limbs (arms, legs, tentacles) where smooth tapering is
essential for realistic appearance.

Performance Target: < 150ms per pattern generation
"""

from typing import List, Literal
import math

from knit_wit_engine.models.dsl import (
    PatternDSL,
    RoundInstruction,
    StitchInstruction,
    GaugeInfo,
    ShapeParameters,
    PatternMetadata,
)
from knit_wit_engine.models.requests import Gauge
from knit_wit_engine.algorithms.distribution import even_distribution, jitter_offset
from knit_wit_engine.algorithms.gauge import estimate_yardage, gauge_to_stitch_length


class ConeCompiler:
    """
    Generates tapered/cone patterns with Bresenham distribution for smooth tapering.

    The compiler uses a Bresenham-like line-drawing algorithm to determine which
    rounds receive increases or decreases, ensuring that the taper is smooth and
    monotonic without any visible stacking or column formation.

    Key Features:
    - Bresenham distribution for optimal delta placement across rounds
    - Jitter offset prevents vertical column stacking
    - Handles both increasing and decreasing tapers
    - Monotonic stitch count progression (no backtracking)

    Attributes:
        None (stateless compiler)

    Example:
        >>> compiler = ConeCompiler()
        >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        >>> # Tapered limb: 6cm diameter to 2cm diameter over 8cm height
        >>> pattern = compiler.generate(
        ...     diameter_start_cm=6,
        ...     diameter_end_cm=2,
        ...     height_cm=8,
        ...     gauge=gauge
        ... )
        >>> print(pattern.metadata.total_rounds)
        13
        >>> # Verify monotonic decrease
        >>> stitch_counts = [r.total_stitches for r in pattern.rounds]
        >>> all(stitch_counts[i] >= stitch_counts[i+1] for i in range(len(stitch_counts)-1))
        True
    """

    def generate(
        self,
        diameter_start_cm: float,
        diameter_end_cm: float,
        height_cm: float,
        gauge: Gauge,
        yarn_weight: str = "Worsted",
    ) -> PatternDSL:
        """
        Generate a complete cone/tapered pattern with smooth transitions.

        Uses Bresenham-like algorithm to distribute increases or decreases evenly
        across the height, creating a smooth taper without visible stacking patterns.

        Args:
            diameter_start_cm: Starting diameter in centimeters (at beginning)
            diameter_end_cm: Ending diameter in centimeters (at end)
            height_cm: Height of cone in centimeters
            gauge: Gauge specification with sts_per_10cm and rows_per_10cm
            yarn_weight: Yarn weight category for yardage estimation.
                        Options: "Baby", "DK", "Worsted", "Bulky"
                        Default: "Worsted"

        Returns:
            PatternDSL object containing complete pattern specification with:
            - Shape parameters (cone, diameters, height)
            - Gauge information
            - Round-by-round instructions
            - Metadata (total rounds, difficulty, tags)

        Algorithm:
            1. Calculate start_stitches: π × start_diameter × (sts_per_10cm / 10)
            2. Calculate end_stitches: π × end_diameter × (sts_per_10cm / 10)
            3. Calculate total_rounds: height × (rows_per_10cm / 10)
            4. Determine direction: increase if end > start, else decrease
            5. For each round r in [1, total_rounds]:
                a. Calculate target cumulative delta using Bresenham:
                   target = round(delta_total × r / total_rounds)
                b. Calculate round_delta = target - cumulative_delta
                c. If round_delta > 0, apply deltas with even_distribution + jitter
                d. Build stitch instructions with increases or decreases
                e. Update cumulative_delta and current_stitches
            6. Calculate yardage estimate

        Bresenham Logic:
            The key insight is to treat the taper as a line from (0, 0) to
            (total_rounds, delta_total). For each round, we calculate the ideal
            cumulative delta and compare to actual. This ensures even distribution
            without floating-point accumulation errors.

            Example: 27 stitches → 18 stitches over 10 rounds (9 total decreases)
            - Round 1: target = round(9 × 1/10) = 1, apply 1 decrease
            - Round 2: target = round(9 × 2/10) = 2, apply 1 decrease
            - Round 3: target = round(9 × 3/10) = 3, apply 1 decrease
            - ...and so on

        Acceptance Criteria:
            - AC-G-2: 6cm → 2cm over 8cm must have monotonic taper
            - No two consecutive deltas in same column position (jitter prevents)
            - Visual inspection: no stacking visible
            - Performance: < 150ms execution time

        Examples:
            >>> # Decreasing taper (typical amigurumi limb)
            >>> compiler = ConeCompiler()
            >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
            >>> pattern = compiler.generate(6, 2, 8, gauge, "Worsted")
            >>> pattern.shape.base_diameter_cm
            6.0
            >>> pattern.shape.top_diameter_cm
            2.0

            >>> # Increasing taper (tree trunk base)
            >>> pattern_inc = compiler.generate(2, 6, 8, gauge, "Worsted")
            >>> start = pattern_inc.rounds[0].total_stitches
            >>> end = pattern_inc.rounds[-1].total_stitches
            >>> start < end
            True

            >>> # Verify monotonic progression
            >>> stitch_counts = [r.total_stitches for r in pattern.rounds]
            >>> # For decreasing taper, each count >= next count
            >>> all(stitch_counts[i] >= stitch_counts[i+1] for i in range(len(stitch_counts)-1))
            True

        Notes:
            - Uses spiral rounds (not joined) for seamless appearance
            - Starts with chain round at starting diameter
            - Applies jitter_offset to prevent vertical stacking of changes
            - Yardage estimate includes 10% waste factor
            - Handles both increasing and decreasing tapers automatically
        """
        # 1. Calculate cone parameters
        start_stitches = round(
            math.pi * diameter_start_cm * (gauge.sts_per_10cm / 10)
        )
        end_stitches = round(math.pi * diameter_end_cm * (gauge.sts_per_10cm / 10))
        total_rounds = round((gauge.rows_per_10cm / 10) * height_cm)

        # Ensure minimum viable structure
        if total_rounds < 1:
            total_rounds = 1

        # Determine delta and direction
        delta_total = abs(end_stitches - start_stitches)
        direction: Literal["increase", "decrease"] = (
            "decrease" if start_stitches > end_stitches else "increase"
        )

        rounds: List[RoundInstruction] = []
        current_stitches = start_stitches
        cumulative_delta = 0
        round_num = 0

        # 2. Starting round (chain and join)
        rounds.append(
            RoundInstruction(
                round_number=round_num,
                stitches=[StitchInstruction(stitch_type="ch", count=start_stitches)],
                total_stitches=start_stitches,
                description=f"Chain {start_stitches}, join with sl st to form ring",
            )
        )
        round_num += 1

        # 3. Taper rounds (Bresenham distribution)
        for r in range(1, total_rounds + 1):
            # Bresenham algorithm: calculate target cumulative delta for this round
            # This gives us the ideal cumulative delta if we were drawing a perfect line
            # from (0, 0) to (total_rounds, delta_total)
            target_cumulative = round(delta_total * r / total_rounds)

            # How many deltas should we apply THIS round?
            # This is the difference between where we should be and where we are
            round_delta = target_cumulative - cumulative_delta

            if round_delta > 0:
                # Apply delta(s) this round
                offset = jitter_offset(r)
                delta_indices = even_distribution(current_stitches, round_delta, offset)

                if direction == "decrease":
                    # Build decrease operations
                    stitch_list = self._build_decrease_operations(
                        current_stitches, delta_indices
                    )
                    new_stitch_count = current_stitches - round_delta
                else:
                    # Build increase operations
                    stitch_list = self._build_increase_operations(
                        current_stitches, delta_indices
                    )
                    new_stitch_count = current_stitches + round_delta

                cumulative_delta += round_delta
            else:
                # No delta this round - steady stitching
                stitch_list = [
                    StitchInstruction(stitch_type="sc", count=current_stitches)
                ]
                new_stitch_count = current_stitches

            rounds.append(
                RoundInstruction(
                    round_number=r,
                    stitches=stitch_list,
                    total_stitches=new_stitch_count,
                    description=f"Round {r}: taper ({direction})",
                )
            )

            current_stitches = new_stitch_count

        # 4. Calculate yardage estimate
        total_stitches = sum(r.total_stitches for r in rounds)
        stitch_length = gauge_to_stitch_length(gauge, yarn_weight)
        yardage = estimate_yardage(total_stitches, stitch_length)

        # 5. Normalize yarn weight to match GaugeInfo Literal type
        yarn_weight_map = {
            "Baby": "fingering",
            "DK": "DK",
            "Worsted": "worsted",
            "Bulky": "bulky",
        }
        normalized_yarn_weight = yarn_weight_map.get(yarn_weight, yarn_weight.lower())

        # 6. Build complete DSL
        return PatternDSL(
            shape=ShapeParameters(
                shape_type="cone",
                base_diameter_cm=diameter_start_cm,
                top_diameter_cm=diameter_end_cm,
                height_cm=height_cm,
            ),
            gauge=GaugeInfo(
                stitches_per_cm=gauge.sts_per_10cm / 10,
                rows_per_cm=gauge.rows_per_10cm / 10,
                yarn_weight=normalized_yarn_weight,
            ),
            rounds=rounds,
            metadata=PatternMetadata(
                total_rounds=len(rounds),
                difficulty="intermediate",
                tags=["cone", "tapered", "limb", "3D"],
            ),
        )

    def _build_decrease_operations(
        self, current_stitches: int, dec_indices: List[int]
    ) -> List[StitchInstruction]:
        """
        Build stitch list with decreases at specified indices.

        Decreases consume 2 stitches to make 1 stitch (sc2tog). This method
        constructs a list of StitchInstructions where decreases are placed
        at the specified indices and regular single crochets fill the gaps.

        Args:
            current_stitches: Total number of stitches in the round
            dec_indices: List of 1-indexed positions where decreases occur
                        (from even_distribution)

        Returns:
            List of StitchInstruction objects for the round

        Algorithm:
            Walk through stitches 1 to current_stitches:
            - If position is in dec_indices AND not the last stitch:
              - Add decrease instruction (consumes this stitch + next)
              - Skip next stitch (already consumed)
            - Otherwise:
              - Add regular single crochet

        Example:
            >>> # 12 stitches, decreases at positions [3, 6, 9, 12]
            >>> stitch_list = self._build_decrease_operations(12, [3, 6, 9, 12])
            >>> # Result: [sc, sc, dec, sc, dec, sc, dec, dec]
            >>> # This creates: sc, sc, (sc2tog), sc, (sc2tog), sc, (sc2tog), (sc2tog)
            >>> # Total output: 8 stitches from 12 input stitches

        Notes:
            - Decreases at position i consume stitches i and i+1
            - If a decrease index points to the last stitch, it's treated as
              a regular sc to avoid consuming a non-existent stitch
            - The resulting stitch count is current_stitches - len(dec_indices)
        """
        stitch_list: List[StitchInstruction] = []
        dec_set = set(dec_indices)
        i = 1

        while i <= current_stitches:
            if i in dec_set and i < current_stitches:
                # Decrease: sc2tog (consumes 2 stitches, produces 1)
                stitch_list.append(StitchInstruction(stitch_type="dec", count=1))
                i += 2  # Skip next stitch (consumed by decrease)
            else:
                # Regular single crochet
                stitch_list.append(StitchInstruction(stitch_type="sc", count=1))
                i += 1

        return stitch_list

    def _build_increase_operations(
        self, current_stitches: int, inc_indices: List[int]
    ) -> List[StitchInstruction]:
        """
        Build stitch list with increases at specified indices.

        Increases work 2 stitches into the same stitch, effectively adding 1 stitch
        at each increase position. This method constructs a list of StitchInstructions
        where increases are placed at the specified indices and regular single crochets
        fill the gaps.

        Args:
            current_stitches: Total number of stitches in the round
            inc_indices: List of 1-indexed positions where increases occur
                        (from even_distribution)

        Returns:
            List of StitchInstruction objects for the round

        Algorithm:
            Walk through stitches 1 to current_stitches:
            - If position is in inc_indices:
              - Add increase instruction (2 sc in same stitch)
            - Otherwise:
              - Add regular single crochet

        Example:
            >>> # 12 stitches, increases at positions [3, 6, 9, 12]
            >>> stitch_list = self._build_increase_operations(12, [3, 6, 9, 12])
            >>> # Result: [sc, sc, inc, sc, sc, inc, sc, sc, inc, sc, sc, inc]
            >>> # This creates: sc, sc, (2sc in next), sc, sc, (2sc in next), ...
            >>> # Total output: 16 stitches from 12 input stitches

        Notes:
            - Each increase adds exactly 1 stitch to the round
            - The increase is worked into the current stitch, then the pattern
              continues to the next stitch position
            - The resulting stitch count is current_stitches + len(inc_indices)
        """
        stitch_list: List[StitchInstruction] = []
        inc_set = set(inc_indices)

        for i in range(1, current_stitches + 1):
            if i in inc_set:
                # Increase: 2 sc in same stitch
                stitch_list.append(StitchInstruction(stitch_type="inc", count=1))
            else:
                # Regular single crochet
                stitch_list.append(StitchInstruction(stitch_type="sc", count=1))

        return stitch_list
