"""
Unit Tests for Cone/Tapered Limb Compiler

Comprehensive pytest suite for cone pattern generation covering:
- AC-G-2: 6cm → 2cm over 8cm with monotonic taper and no stacking
- Decreasing tapers (typical limbs)
- Increasing tapers (tree trunks, bases)
- Steep and gradual tapers
- Bresenham distribution smoothness
- Monotonic progression verification
- Performance requirements (< 150ms)
- JSON serialization/deserialization

Test Coverage Target: 80%+
"""

import time
from typing import List

import pytest

from knit_wit_engine.models.dsl import PatternDSL, RoundInstruction
from knit_wit_engine.models.requests import Gauge
from knit_wit_engine.shapes.cone import ConeCompiler


class TestConeACG2:
    """Critical acceptance criteria test: AC-G-2."""

    def test_ac_g_2_6cm_to_2cm_over_8cm(self):
        """
        AC-G-2: 6cm → 2cm over 8cm must have monotonic taper with no stacking.

        This is the critical acceptance test for cone generation. The taper must:
        1. Be smooth and monotonic (no backtracking in stitch count)
        2. Show no visible stacking or column formation
        3. Distribute decreases evenly using Bresenham algorithm
        """
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=6,
            diameter_end_cm=2,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        # Verify shape parameters
        assert pattern.shape.shape_type == "cone"
        assert pattern.shape.base_diameter_cm == 6
        assert pattern.shape.top_diameter_cm == 2
        assert pattern.shape.height_cm == 8

        # Calculate expected stitch counts
        start_stitches = round(3.14159 * 6 * 14 / 10)  # ≈ 26 stitches
        end_stitches = round(3.14159 * 2 * 14 / 10)  # ≈ 9 stitches

        # Verify starting round (chain)
        first_round = pattern.rounds[0]
        assert first_round.round_number == 0
        assert any(stitch.stitch_type == "ch" for stitch in first_round.stitches)
        assert abs(first_round.total_stitches - start_stitches) <= 1

        # Verify monotonic decreasing taper
        stitch_counts = [r.total_stitches for r in pattern.rounds]

        for i in range(len(stitch_counts) - 1):
            assert stitch_counts[i] >= stitch_counts[i + 1], (
                f"Non-monotonic decrease at round {i}: "
                f"{stitch_counts[i]} to {stitch_counts[i+1]}"
            )

        # Verify ending stitch count
        assert abs(stitch_counts[-1] - end_stitches) <= 2

        # Verify no stacking: check for evenly distributed decreases
        # No two consecutive rounds should have the same decrease positions
        # (This is ensured by jitter_offset in the implementation)
        delta_counts = [
            stitch_counts[i] - stitch_counts[i + 1]
            for i in range(len(stitch_counts) - 1)
        ]

        # Decreases should be relatively evenly distributed
        # Most rounds should have 0 or 1 decreases for smooth taper
        assert all(delta >= 0 for delta in delta_counts), "All deltas should be >= 0"
        assert max(delta_counts) <= 3, "No round should have > 3 decreases at once"


class TestConeBasicGeneration:
    """Basic cone generation tests with standard parameters."""

    def test_decreasing_taper_6cm_to_2cm(self):
        """Test standard decreasing taper (typical amigurumi limb)."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=6,
            diameter_end_cm=2,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        # Verify DSL structure
        assert pattern.shape.shape_type == "cone"
        assert pattern.shape.base_diameter_cm == 6
        assert pattern.shape.top_diameter_cm == 2
        assert pattern.shape.height_cm == 8
        assert len(pattern.rounds) > 8

        # Verify taper direction
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        assert stitch_counts[0] > stitch_counts[-1], "Should decrease from start to end"

        # Verify metadata
        assert pattern.metadata.difficulty == "intermediate"
        assert "cone" in pattern.metadata.tags
        assert "tapered" in pattern.metadata.tags

    def test_increasing_taper_2cm_to_6cm(self):
        """Test increasing taper (tree trunk base, flared shapes)."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=2,
            diameter_end_cm=6,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        # Verify shape parameters
        assert pattern.shape.base_diameter_cm == 2
        assert pattern.shape.top_diameter_cm == 6

        # Verify increasing taper
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        assert stitch_counts[0] < stitch_counts[-1], "Should increase from start to end"

        # Verify monotonic increasing
        for i in range(len(stitch_counts) - 1):
            assert stitch_counts[i] <= stitch_counts[i + 1], (
                f"Non-monotonic increase at round {i}"
            )


class TestConeTaperVariations:
    """Tests for various taper steepness and gradualness."""

    def test_steep_taper_8cm_to_2cm_over_5cm(self):
        """Test steep taper: large diameter change over short height."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=8,
            diameter_end_cm=2,
            height_cm=5,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]

        # Steep taper should have significant stitch changes
        total_delta = stitch_counts[0] - stitch_counts[-1]
        assert total_delta >= 15, "Steep taper should have large total decrease"

        # Verify monotonic despite steepness
        for i in range(len(stitch_counts) - 1):
            assert stitch_counts[i] >= stitch_counts[i + 1], (
                f"Non-monotonic at round {i} in steep taper"
            )

    def test_gradual_taper_10cm_to_9cm_over_20cm(self):
        """Test gradual taper: small diameter change over long height."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=10,
            diameter_end_cm=9,
            height_cm=20,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]

        # Gradual taper should have small stitch changes
        total_delta = abs(stitch_counts[0] - stitch_counts[-1])
        assert total_delta <= 6, "Gradual taper should have small total change"

        # Most rounds should have no change (0 delta)
        deltas = [
            abs(stitch_counts[i] - stitch_counts[i + 1])
            for i in range(len(stitch_counts) - 1)
        ]
        zero_delta_count = deltas.count(0)
        assert zero_delta_count > len(deltas) * 0.7, (
            "Gradual taper should have many rounds with no change"
        )

        # Verify monotonic
        for i in range(len(stitch_counts) - 1):
            assert stitch_counts[i] >= stitch_counts[i + 1], (
                f"Non-monotonic at round {i} in gradual taper"
            )


class TestConeMonotonicVerification:
    """Tests specifically for monotonic progression verification."""

    def test_monotonic_decreasing_progression(self):
        """Verify decreasing taper has strictly monotonic non-increasing progression."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        # Test multiple decreasing tapers
        test_cases = [
            (8, 3, 10),
            (10, 4, 15),
            (6, 2, 8),
            (12, 6, 12),
        ]

        for start_d, end_d, height in test_cases:
            pattern = compiler.generate(
                diameter_start_cm=start_d,
                diameter_end_cm=end_d,
                height_cm=height,
                gauge=gauge,
                yarn_weight="Worsted",
            )

            stitch_counts = [r.total_stitches for r in pattern.rounds]

            # Verify strictly non-increasing (monotonic decreasing)
            for i in range(len(stitch_counts) - 1):
                assert stitch_counts[i] >= stitch_counts[i + 1], (
                    f"Non-monotonic at round {i} for {start_d}→{end_d} over {height}cm"
                )

    def test_monotonic_increasing_progression(self):
        """Verify increasing taper has strictly monotonic non-decreasing progression."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        # Test multiple increasing tapers
        test_cases = [
            (3, 8, 10),
            (4, 10, 15),
            (2, 6, 8),
            (6, 12, 12),
        ]

        for start_d, end_d, height in test_cases:
            pattern = compiler.generate(
                diameter_start_cm=start_d,
                diameter_end_cm=end_d,
                height_cm=height,
                gauge=gauge,
                yarn_weight="Worsted",
            )

            stitch_counts = [r.total_stitches for r in pattern.rounds]

            # Verify strictly non-decreasing (monotonic increasing)
            for i in range(len(stitch_counts) - 1):
                assert stitch_counts[i] <= stitch_counts[i + 1], (
                    f"Non-monotonic at round {i} for {start_d}→{end_d} over {height}cm"
                )


class TestConeNoStacking:
    """Tests to verify no visible stacking or column formation."""

    def test_no_stacking_verification(self):
        """Verify Bresenham distribution prevents stacking."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=6,
            diameter_end_cm=2,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]

        # Calculate deltas between rounds
        deltas = [
            stitch_counts[i] - stitch_counts[i + 1]
            for i in range(len(stitch_counts) - 1)
        ]

        # No single round should have excessive deltas (which would create stacking)
        assert max(deltas) <= 3, "No round should have > 3 deltas (would create stacking)"

        # Deltas should be evenly distributed (most should be 0, 1, or 2)
        delta_variety = set(deltas)
        assert delta_variety.issubset(
            {0, 1, 2, 3}
        ), f"Deltas should be small and even, got: {delta_variety}"

        # Count consecutive rounds with same delta
        max_consecutive_same_delta = 0
        current_consecutive = 1

        for i in range(1, len(deltas)):
            if deltas[i] == deltas[i - 1] and deltas[i] > 0:
                current_consecutive += 1
                max_consecutive_same_delta = max(
                    max_consecutive_same_delta, current_consecutive
                )
            else:
                current_consecutive = 1

        # Jitter should prevent long runs of same delta
        assert max_consecutive_same_delta <= 3, (
            f"Too many consecutive rounds with same delta: {max_consecutive_same_delta}"
        )


class TestConeBresenhamDistribution:
    """Tests for Bresenham-like distribution algorithm."""

    def test_bresenham_smoothness(self):
        """Verify Bresenham algorithm distributes deltas evenly."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        # Test case: 27 stitches → 18 stitches over 10 rounds (9 total decreases)
        pattern = compiler.generate(
            diameter_start_cm=6.12,  # ≈ 27 stitches
            diameter_end_cm=4.08,  # ≈ 18 stitches
            height_cm=6.25,  # ≈ 10 rounds
            gauge=gauge,
            yarn_weight="Worsted",
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]
        deltas = [
            stitch_counts[i] - stitch_counts[i + 1]
            for i in range(len(stitch_counts) - 1)
        ]

        # Bresenham should distribute evenly: most rounds get 0 or 1 delta
        delta_distribution = {d: deltas.count(d) for d in set(deltas)}

        # The distribution should be dominated by 0s and 1s
        small_deltas = delta_distribution.get(0, 0) + delta_distribution.get(1, 0)
        total_rounds = len(deltas)

        assert small_deltas / total_rounds > 0.8, (
            f"Bresenham should produce mostly 0/1 deltas, got: {delta_distribution}"
        )


class TestConePerformance:
    """Performance tests for cone generation."""

    def test_performance_under_150ms(self):
        """Verify pattern generation completes in < 150ms."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        # Test multiple sizes and taper types
        test_cases = [
            (6, 2, 8),  # AC-G-2 case
            (8, 3, 10),  # Steep taper
            (10, 9, 20),  # Gradual taper
            (2, 6, 8),  # Increasing taper
            (12, 4, 15),  # Large with steep taper
        ]

        for start_d, end_d, height in test_cases:
            start_time = time.perf_counter()
            pattern = compiler.generate(
                diameter_start_cm=start_d,
                diameter_end_cm=end_d,
                height_cm=height,
                gauge=gauge,
                yarn_weight="Worsted",
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            assert elapsed_ms < 150, (
                f"Generation took {elapsed_ms:.2f}ms for "
                f"{start_d}cm→{end_d}cm over {height}cm (limit: 150ms)"
            )
            assert len(pattern.rounds) > 0


class TestConeSerialization:
    """Tests for JSON serialization and deserialization."""

    def test_json_serialization_roundtrip(self):
        """Test that cone pattern can be serialized to JSON and back."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        original = compiler.generate(
            diameter_start_cm=6,
            diameter_end_cm=2,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        # Serialize to JSON
        json_str = original.model_dump_json(indent=2)
        assert len(json_str) > 100

        # Deserialize back to PatternDSL
        restored = PatternDSL.model_validate_json(json_str)

        # Verify structure matches
        assert restored.shape.shape_type == original.shape.shape_type
        assert restored.shape.base_diameter_cm == original.shape.base_diameter_cm
        assert restored.shape.top_diameter_cm == original.shape.top_diameter_cm
        assert restored.shape.height_cm == original.shape.height_cm
        assert len(restored.rounds) == len(original.rounds)

        # Verify stitch counts match
        original_counts = [r.total_stitches for r in original.rounds]
        restored_counts = [r.total_stitches for r in restored.rounds]
        assert original_counts == restored_counts

    def test_json_contains_expected_fields(self):
        """Test that serialized JSON contains all expected fields."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_start_cm=6,
            diameter_end_cm=2,
            height_cm=8,
            gauge=gauge,
            yarn_weight="Worsted",
        )

        json_str = pattern.model_dump_json()

        # Verify key fields are present (JSON is minified without spaces)
        assert '"shape_type":"cone"' in json_str
        assert '"base_diameter_cm"' in json_str
        assert '"top_diameter_cm"' in json_str
        assert '"height_cm"' in json_str
        assert '"rounds"' in json_str
        assert '"total_stitches"' in json_str
        assert '"stitch_type"' in json_str
        assert '"metadata"' in json_str
        assert '"difficulty"' in json_str
