"""
Sphere Pattern Compiler

Generates complete crochet patterns for spherical shapes using spiral rounds
and single crochet stitches. Implements even distribution of increases and
decreases to create a smooth, spherical form.

The compiler follows a five-phase approach:
1. Magic ring initialization (6 stitches)
2. Increase phase (expanding to equator)
3. Steady phase (1-2 rounds at maximum diameter)
4. Decrease phase (contracting from equator)
5. Finishing (closing at 6 stitches)

Performance Target: < 150ms per pattern generation
"""

from typing import List
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


class SphereCompiler:
    """
    Generates sphere patterns with spiral rounds and even increase/decrease spacing.

    The compiler uses parametric calculations to determine the number of rounds
    and stitches at each stage, then applies the even_distribution algorithm
    to space increases and decreases uniformly around the circumference.

    Attributes:
        None (stateless compiler)

    Example:
        >>> compiler = SphereCompiler()
        >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        >>> pattern = compiler.generate(diameter_cm=10, gauge=gauge)
        >>> print(pattern.metadata.total_rounds)
        19
        >>> # Equator should be ~44 stitches for 10cm sphere at 14/16 gauge
        >>> max_stitches = max(r.total_stitches for r in pattern.rounds)
        >>> print(max_stitches)
        44
    """

    def generate(
        self, diameter_cm: float, gauge: Gauge, yarn_weight: str = "Worsted"
    ) -> PatternDSL:
        """
        Generate a complete sphere pattern.

        Calculates the required number of rounds and stitch counts based on the
        desired diameter and gauge, then generates round-by-round instructions
        with evenly-spaced increases and decreases.

        Args:
            diameter_cm: Target sphere diameter in centimeters (must be positive)
            gauge: Gauge specification with sts_per_10cm and rows_per_10cm
            yarn_weight: Yarn weight category for yardage estimation.
                        Options: "Baby", "DK", "Worsted", "Bulky"
                        Default: "Worsted"

        Returns:
            PatternDSL object containing complete pattern specification with:
            - Shape parameters (sphere, diameter)
            - Gauge information
            - Round-by-round instructions
            - Metadata (total rounds, difficulty, tags)

        Algorithm:
            1. Calculate equator stitches: π × diameter × (sts_per_10cm / 10)
            2. Calculate increase rounds: (rows_per_10cm / 10) × radius
            3. Generate magic ring start (6 stitches)
            4. Increase phase: distribute increases evenly with jitter
            5. Steady phase: 1-2 rounds at equator
            6. Decrease phase: mirror increase pattern
            7. Calculate yardage estimate

        Acceptance Criteria:
            - AC-G-1: 10 cm sphere at 14/16 gauge → ~44 equator stitches (±1)
            - Increases/decreases evenly spaced (no vertical stacking)
            - Monotonic stitch count: increases then decreases
            - Performance: < 150ms execution time

        Examples:
            >>> # Standard worsted sphere
            >>> compiler = SphereCompiler()
            >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
            >>> pattern = compiler.generate(10, gauge, "Worsted")
            >>> pattern.shape.diameter_cm
            10.0

            >>> # Fine gauge DK sphere
            >>> gauge_fine = Gauge(sts_per_10cm=18, rows_per_10cm=20)
            >>> pattern = compiler.generate(8, gauge_fine, "DK")
            >>> equator = max(r.total_stitches for r in pattern.rounds)
            >>> print(equator)
            45

        Notes:
            - Uses spiral rounds (not joined) for seamless appearance
            - Starts and ends with 6 stitches (standard magic ring)
            - Applies jitter_offset to prevent vertical stacking of changes
            - Yardage estimate includes 10% waste factor
        """
        # 1. Calculate sphere parameters
        radius = diameter_cm / 2

        # Equator circumference in stitches
        # Formula: π × diameter × stitches_per_cm
        equator_stitches = round(math.pi * diameter_cm * (gauge.sts_per_10cm / 10))

        # Number of rounds to reach equator
        # Formula: radius × rows_per_cm
        increase_rounds = round((gauge.rows_per_10cm / 10) * radius)

        # Ensure minimum viable structure
        if increase_rounds < 1:
            increase_rounds = 1

        rounds: List[RoundInstruction] = []
        current_stitches = 6
        round_num = 0

        # 2. Magic ring start (Round 0)
        rounds.append(
            RoundInstruction(
                round_number=round_num,
                stitches=[StitchInstruction(stitch_type="MR", count=6)],
                total_stitches=6,
                description="Magic ring with 6 sc",
            )
        )
        round_num += 1

        # 3. Increase phase - expand from 6 to equator_stitches
        for r in range(increase_rounds):
            remaining_rounds = increase_rounds - r

            # Calculate how many increases needed in this round
            # Distribute remaining increases across remaining rounds
            target_increase = (equator_stitches - current_stitches) // remaining_rounds

            if target_increase > 0:
                # Apply jitter to prevent vertical stacking
                offset = jitter_offset(round_num)

                # Get evenly-distributed positions for increases
                inc_indices = even_distribution(current_stitches, target_increase, offset)

                # Build stitch instructions
                stitch_list: List[StitchInstruction] = []
                inc_set = set(inc_indices)

                for i in range(1, current_stitches + 1):
                    if i in inc_set:
                        # Increase: 2 sc in same stitch
                        stitch_list.append(StitchInstruction(stitch_type="inc", count=1))
                    else:
                        # Regular single crochet
                        stitch_list.append(StitchInstruction(stitch_type="sc", count=1))

                new_stitch_count = current_stitches + target_increase
            else:
                # No increases this round - steady stitching
                stitch_list = [
                    StitchInstruction(stitch_type="sc", count=current_stitches)
                ]
                new_stitch_count = current_stitches

            rounds.append(
                RoundInstruction(
                    round_number=round_num,
                    stitches=stitch_list,
                    total_stitches=new_stitch_count,
                    description=f"Round {round_num}: increase phase",
                )
            )

            current_stitches = new_stitch_count
            round_num += 1

        # 4. Steady phase at equator (1-2 rounds)
        for steady_idx in range(2):
            rounds.append(
                RoundInstruction(
                    round_number=round_num,
                    stitches=[
                        StitchInstruction(stitch_type="sc", count=current_stitches)
                    ],
                    total_stitches=current_stitches,
                    description=f"Round {round_num}: steady at equator",
                )
            )
            round_num += 1

        # 5. Decrease phase - mirror of increase phase
        # Work backwards from equator to 6 stitches
        decrease_rounds = increase_rounds

        for r in range(decrease_rounds):
            remaining_rounds = decrease_rounds - r

            # Calculate how many decreases needed in this round
            # Target: reach 6 stitches by end of decrease phase
            target_decrease = (current_stitches - 6) // remaining_rounds

            if target_decrease > 0:
                # Apply jitter to prevent vertical stacking
                offset = jitter_offset(round_num)

                # Get evenly-distributed positions for decreases
                dec_indices = even_distribution(current_stitches, target_decrease, offset)

                # Build stitch instructions
                # Decreases consume 2 stitches to make 1
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

                new_stitch_count = current_stitches - target_decrease
            else:
                # No decreases this round - steady stitching
                stitch_list = [
                    StitchInstruction(stitch_type="sc", count=current_stitches)
                ]
                new_stitch_count = current_stitches

            rounds.append(
                RoundInstruction(
                    round_number=round_num,
                    stitches=stitch_list,
                    total_stitches=new_stitch_count,
                    description=f"Round {round_num}: decrease phase",
                )
            )

            current_stitches = new_stitch_count
            round_num += 1

        # 6. Calculate yardage estimate
        total_stitches = sum(r.total_stitches for r in rounds)
        stitch_length = gauge_to_stitch_length(gauge, yarn_weight)
        yardage = estimate_yardage(total_stitches, stitch_length)

        # 7. Normalize yarn weight to match GaugeInfo Literal type
        # Valid values: "lace", "fingering", "sport", "DK", "worsted", "bulky", "super_bulky"
        yarn_weight_map = {
            "Baby": "fingering",
            "DK": "DK",
            "Worsted": "worsted",
            "Bulky": "bulky",
        }
        normalized_yarn_weight = yarn_weight_map.get(yarn_weight, yarn_weight.lower())

        # 8. Build complete DSL
        return PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=diameter_cm),
            gauge=GaugeInfo(
                stitches_per_cm=gauge.sts_per_10cm / 10,
                rows_per_cm=gauge.rows_per_10cm / 10,
                yarn_weight=normalized_yarn_weight,
            ),
            rounds=rounds,
            metadata=PatternMetadata(
                total_rounds=len(rounds),
                difficulty="intermediate",
                tags=["sphere", "amigurumi", "3D"],
            ),
        )
