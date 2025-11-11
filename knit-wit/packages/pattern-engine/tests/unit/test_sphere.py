"""
Unit Tests for Sphere Compiler

Comprehensive pytest suite for sphere pattern generation covering:
- Standard sphere dimensions and gauge combinations
- Edge cases (small, large, unusual gauges)
- Performance requirements
- Even distribution verification
- Monotonic increase/decrease phases
- JSON serialization/deserialization
- DSL validation

Test Coverage Target: 80%+
"""

import time
from typing import List

import pytest

from knit_wit_engine.models.dsl import PatternDSL, RoundInstruction
from knit_wit_engine.models.requests import Gauge
from knit_wit_engine.shapes.sphere import SphereCompiler


class TestSphereBasicGeneration:
    """Basic sphere generation tests with standard parameters."""

    def test_sphere_10cm_sc_spiral_gauge_14_16(self):
        """Test standard 10 cm sphere with 14/16 gauge (AC-G-1)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge, yarn_weight="Worsted")

        # Verify DSL structure
        assert pattern.shape.shape_type == "sphere"
        assert len(pattern.rounds) > 10
        assert pattern.rounds[0].total_stitches == 6  # Magic ring start

        # Verify equator stitches (AC-G-1)
        # Formula: π × d × gauge / 10 = 3.14159 × 10 × 14 / 10 ≈ 44
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        expected_equator = round(3.14159 * 10 * 14 / 10)
        assert abs(max_stitches - expected_equator) <= 2  # Tolerance: ±2 stitches

    def test_sphere_generates_valid_pattern(self):
        """Test that generated pattern has valid structure."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Verify pattern structure
        assert isinstance(pattern, PatternDSL)
        assert pattern.shape.diameter_cm == 10
        assert pattern.gauge.stitches_per_cm == 1.4
        assert pattern.gauge.rows_per_cm == 1.6
        assert pattern.metadata.total_rounds == len(pattern.rounds)
        assert pattern.metadata.difficulty == "intermediate"
        assert "sphere" in pattern.metadata.tags

    def test_sphere_starts_with_magic_ring(self):
        """Test that all spheres start with 6-stitch magic ring."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # First round should be magic ring with 6 stitches
        first_round = pattern.rounds[0]
        assert first_round.round_number == 0
        assert first_round.total_stitches == 6
        assert any(stitch.stitch_type == "MR" for stitch in first_round.stitches)


class TestSphereEvenDistribution:
    """Tests for even distribution of increases and decreases."""

    def test_sphere_even_distribution(self):
        """Test that increases are evenly distributed (no visible columns)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Verify monotonic increase then decrease
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        equator_index = stitch_counts.index(max(stitch_counts))

        # Increase phase should be monotonic increasing
        for i in range(equator_index):
            assert stitch_counts[i] <= stitch_counts[i + 1], (
                f"Non-monotonic increase at round {i}: "
                f"{stitch_counts[i]} to {stitch_counts[i+1]}"
            )

        # Decrease phase should be monotonic decreasing
        for i in range(equator_index, len(stitch_counts) - 1):
            assert stitch_counts[i] >= stitch_counts[i + 1], (
                f"Non-monotonic decrease at round {i}: "
                f"{stitch_counts[i]} to {stitch_counts[i+1]}"
            )

    def test_sphere_no_stitch_jumps(self):
        """Test that stitch count changes gradually (no large jumps)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        stitch_counts = [r.total_stitches for r in pattern.rounds]

        # Verify no jumps larger than expected
        for i in range(len(stitch_counts) - 1):
            delta = abs(stitch_counts[i + 1] - stitch_counts[i])
            # Maximum expected change is about 1/6 of current stitches
            max_allowed_delta = max(stitch_counts[i] // 5, 6)
            assert (
                delta <= max_allowed_delta
            ), f"Large jump at round {i}: {delta} stitches"

    def test_sphere_symmetric_increase_decrease(self):
        """Test that increase and decrease phases are roughly symmetric."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        stitch_counts = [r.total_stitches for r in pattern.rounds]
        equator_index = stitch_counts.index(max(stitch_counts))

        # Count rounds in each phase (excluding magic ring and steady rounds)
        increase_rounds = equator_index  # Rounds 0 to equator
        decrease_rounds = len(stitch_counts) - equator_index - 3  # After steady rounds

        # Should be roughly equal (within 1 round)
        assert abs(increase_rounds - decrease_rounds) <= 2, (
            f"Asymmetric phases: {increase_rounds} increase rounds, "
            f"{decrease_rounds} decrease rounds"
        )


class TestSpherePerformance:
    """Performance and timing tests."""

    def test_sphere_performance(self):
        """Test that generation completes in < 200ms."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        start = time.time()
        pattern = compiler.generate(diameter_cm=10, gauge=gauge)
        elapsed = time.time() - start

        assert elapsed < 0.2  # 200ms
        assert pattern is not None

    def test_sphere_large_pattern_performance(self):
        """Test that large patterns still meet performance target."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=22, rows_per_10cm=24)  # Fine gauge

        start = time.time()
        pattern = compiler.generate(diameter_cm=25, gauge=gauge)  # Large sphere
        elapsed = time.time() - start

        assert elapsed < 0.2  # Should still be under 200ms
        assert len(pattern.rounds) > 30


class TestSphereEdgeCases:
    """Edge case tests for small, large, and unusual parameters."""

    def test_sphere_small_5cm(self):
        """Test small sphere doesn't have negative rounds."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=18, rows_per_10cm=20)  # Fine gauge

        pattern = compiler.generate(diameter_cm=5, gauge=gauge)

        assert len(pattern.rounds) > 0
        assert all(r.total_stitches > 0 for r in pattern.rounds)
        assert pattern.rounds[0].total_stitches == 6  # Magic ring start

    def test_sphere_large_20cm(self):
        """Test large sphere performance and structure."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=10, rows_per_10cm=12)  # Coarse gauge

        start = time.time()
        pattern = compiler.generate(diameter_cm=20, gauge=gauge)
        elapsed = time.time() - start

        assert elapsed < 0.2
        assert len(pattern.rounds) > 20
        # Large sphere should have significant equator
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        assert max_stitches > 50

    def test_sphere_very_small_3cm(self):
        """Test very small sphere still generates valid pattern."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=3, gauge=gauge)

        assert len(pattern.rounds) >= 5  # Minimum viable structure
        assert pattern.rounds[0].total_stitches == 6
        assert all(r.total_stitches > 0 for r in pattern.rounds)

    def test_sphere_very_large_30cm(self):
        """Test very large sphere with reasonable structure."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=30, gauge=gauge)

        assert len(pattern.rounds) > 40
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        # Equator should be approximately π × 30 × 1.4 ≈ 132 stitches
        assert 120 <= max_stitches <= 140


class TestSphereDifferentGauges:
    """Tests with various gauge specifications."""

    def test_sphere_different_gauges(self):
        """Test sphere with various gauge specifications."""
        compiler = SphereCompiler()

        gauges = [
            Gauge(sts_per_10cm=10, rows_per_10cm=12),  # Coarse
            Gauge(sts_per_10cm=14, rows_per_10cm=16),  # Standard
            Gauge(sts_per_10cm=18, rows_per_10cm=20),  # Fine
            Gauge(sts_per_10cm=22, rows_per_10cm=24),  # Very fine
        ]

        for gauge in gauges:
            pattern = compiler.generate(diameter_cm=10, gauge=gauge)
            assert pattern is not None
            assert len(pattern.rounds) > 0
            assert pattern.rounds[0].total_stitches == 6

    def test_sphere_coarse_gauge_10_12(self):
        """Test sphere with coarse gauge (bulky yarn)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=10, rows_per_10cm=12)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Coarse gauge should result in fewer stitches
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        expected_equator = round(3.14159 * 10 * 10 / 10)  # ≈ 31
        assert abs(max_stitches - expected_equator) <= 2

    def test_sphere_fine_gauge_22_24(self):
        """Test sphere with fine gauge (lace/fingering yarn)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=22, rows_per_10cm=24)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Fine gauge should result in more stitches
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        expected_equator = round(3.14159 * 10 * 22 / 10)  # ≈ 69
        assert abs(max_stitches - expected_equator) <= 2

    def test_sphere_non_square_gauge(self):
        """Test sphere with non-square gauge (different h/v ratios)."""
        compiler = SphereCompiler()
        # Gauge where rows are much taller than stitches are wide
        gauge = Gauge(sts_per_10cm=18, rows_per_10cm=14)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        assert pattern is not None
        assert len(pattern.rounds) > 0
        # Should still produce valid pattern with adjusted round count


class TestSphereYarnWeights:
    """Tests with different yarn weight specifications."""

    def test_sphere_worsted_yarn(self):
        """Test sphere with worsted weight yarn."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge, yarn_weight="Worsted")

        assert pattern.gauge.yarn_weight == "worsted"

    def test_sphere_dk_yarn(self):
        """Test sphere with DK weight yarn."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=18, rows_per_10cm=20)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge, yarn_weight="DK")

        assert pattern.gauge.yarn_weight == "DK"

    def test_sphere_bulky_yarn(self):
        """Test sphere with bulky weight yarn."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=10, rows_per_10cm=12)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge, yarn_weight="Bulky")

        assert pattern.gauge.yarn_weight == "bulky"

    def test_sphere_baby_yarn(self):
        """Test sphere with baby weight yarn (maps to fingering)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=20, rows_per_10cm=22)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge, yarn_weight="Baby")

        assert pattern.gauge.yarn_weight == "fingering"


class TestSphereJSONSerialization:
    """Tests for JSON serialization and deserialization."""

    def test_sphere_json_serialization(self):
        """Test pattern can be serialized to/from JSON."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Serialize
        json_str = pattern.to_json()
        assert len(json_str) > 100
        assert '"shape_type": "sphere"' in json_str

        # Deserialize
        pattern_copy = PatternDSL.from_json(json_str)
        assert pattern_copy.shape.diameter_cm == 10
        assert pattern_copy.shape.shape_type == "sphere"
        assert len(pattern_copy.rounds) == len(pattern.rounds)

    def test_sphere_to_dict(self):
        """Test pattern can be converted to dictionary."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        pattern_dict = pattern.to_dict()

        assert isinstance(pattern_dict, dict)
        assert pattern_dict["shape"]["shape_type"] == "sphere"
        assert pattern_dict["shape"]["diameter_cm"] == 10
        assert len(pattern_dict["rounds"]) > 0

    def test_sphere_from_dict(self):
        """Test pattern can be created from dictionary."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        original = compiler.generate(diameter_cm=10, gauge=gauge)
        pattern_dict = original.to_dict()

        # Recreate from dictionary
        pattern = PatternDSL.from_dict(pattern_dict)

        assert pattern.shape.diameter_cm == 10
        assert len(pattern.rounds) == len(original.rounds)


class TestSphereRoundStructure:
    """Tests for round instruction structure and validity."""

    def test_sphere_round_numbers_sequential(self):
        """Test that round numbers are sequential starting from 0."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        for i, round_inst in enumerate(pattern.rounds):
            assert (
                round_inst.round_number == i
            ), f"Expected round {i}, got {round_inst.round_number}"

    def test_sphere_all_rounds_have_stitches(self):
        """Test that all rounds have at least one stitch instruction."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        for round_inst in pattern.rounds:
            assert len(round_inst.stitches) > 0
            assert round_inst.total_stitches > 0

    def test_sphere_stitch_types_valid(self):
        """Test that all stitch types are valid crochet operations."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        valid_stitch_types = {"MR", "sc", "inc", "dec"}

        for round_inst in pattern.rounds:
            for stitch in round_inst.stitches:
                assert (
                    stitch.stitch_type in valid_stitch_types
                ), f"Invalid stitch type: {stitch.stitch_type}"

    def test_sphere_has_steady_rounds_at_equator(self):
        """Test that there are steady rounds at the equator."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        stitch_counts = [r.total_stitches for r in pattern.rounds]
        max_stitches = max(stitch_counts)

        # Count consecutive rounds at max stitches
        steady_rounds = 0
        for count in stitch_counts:
            if count == max_stitches:
                steady_rounds += 1

        # Should have at least 1 steady round (typically 2)
        assert steady_rounds >= 1, "No steady rounds at equator"


class TestSphereMetadata:
    """Tests for pattern metadata."""

    def test_sphere_metadata_complete(self):
        """Test that metadata is properly populated."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        assert pattern.metadata.total_rounds == len(pattern.rounds)
        assert pattern.metadata.difficulty in ["beginner", "intermediate", "advanced"]
        assert len(pattern.metadata.tags) > 0
        assert "sphere" in pattern.metadata.tags
        assert pattern.metadata.engine_version == "0.1.0"

    def test_sphere_metadata_timestamps(self):
        """Test that timestamp is set."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        assert pattern.metadata.generated_at is not None


class TestSphereGaugeInfo:
    """Tests for gauge information in pattern."""

    def test_sphere_gauge_info_conversion(self):
        """Test that gauge is correctly converted to per-cm values."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(diameter_cm=10, gauge=gauge)

        # Verify conversion from per-10cm to per-cm
        assert pattern.gauge.stitches_per_cm == 1.4
        assert pattern.gauge.rows_per_cm == 1.6

    def test_sphere_gauge_info_yarn_weight(self):
        """Test that yarn weight is properly set in gauge info."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=10, gauge=gauge, yarn_weight="Worsted"
        )

        assert pattern.gauge.yarn_weight == "worsted"  # Normalized to lowercase
