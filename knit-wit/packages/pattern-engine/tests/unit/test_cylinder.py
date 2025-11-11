"""
Unit Tests for Cylinder Compiler

Comprehensive pytest suite for cylinder pattern generation covering:
- Standard capped cylinders with hemisphere ends
- Uncapped tubes (open cylinders)
- Body section maintains constant stitch count
- Cap sections use hemisphere logic
- Various dimensions and gauge combinations
- Performance requirements (< 150ms)
- JSON serialization/deserialization

Test Coverage Target: 80%+
"""

import time
from typing import List

import pytest

from knit_wit_engine.models.dsl import PatternDSL, RoundInstruction
from knit_wit_engine.models.requests import Gauge
from knit_wit_engine.shapes.cylinder import CylinderCompiler


class TestCylinderBasicGeneration:
    """Basic cylinder generation tests with standard parameters."""

    def test_standard_capped_cylinder_6cm_12cm(self):
        """Test standard capped cylinder: 6cm diameter × 12cm height."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=6, height_cm=12, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        # Verify DSL structure
        assert pattern.shape.shape_type == "cylinder"
        assert pattern.shape.diameter_cm == 6
        assert pattern.shape.height_cm == 12
        assert len(pattern.rounds) > 15  # At least bottom cap + body + top cap

        # Verify circumference calculation
        # Formula: π × d × gauge / 10 = 3.14159 × 6 × 14 / 10 ≈ 26 stitches
        expected_circumference = round(3.14159 * 6 * 14 / 10)

        # Find body rounds (constant stitch count)
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        max_stitches = max(stitch_counts)
        assert abs(max_stitches - expected_circumference) <= 2

        # Verify pattern has caps
        assert "capped" in pattern.metadata.tags
        assert pattern.metadata.difficulty == "intermediate"

    def test_uncapped_tube(self):
        """Test uncapped tube (open cylinder without end caps)."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=8, height_cm=10, gauge=gauge, has_caps=False, yarn_weight="Worsted"
        )

        # Verify structure
        assert pattern.shape.shape_type == "cylinder"
        assert pattern.shape.diameter_cm == 8
        assert pattern.shape.height_cm == 10

        # First round should be chain, not magic ring
        first_round = pattern.rounds[0]
        assert first_round.round_number == 0
        assert any(stitch.stitch_type == "ch" for stitch in first_round.stitches)

        # Verify no caps
        assert "open" in pattern.metadata.tags
        assert pattern.metadata.difficulty == "beginner"

        # All rounds after first should have same stitch count
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        assert all(count == stitch_counts[1] for count in stitch_counts[1:])


class TestCylinderBodySection:
    """Tests for constant stitch count in body section."""

    def test_body_maintains_constant_stitch_count(self):
        """Verify body section maintains constant stitch count throughout."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=8, height_cm=15, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]
        max_count = max(stitch_counts)

        # Find all rounds with max stitch count (body section)
        body_rounds = [
            i for i, count in enumerate(stitch_counts) if count == max_count
        ]

        # Body section should have multiple consecutive rounds with same count
        assert len(body_rounds) >= 3, "Body section should have at least 3 rounds"

        # Verify consecutive body rounds have constant stitch count
        for i in range(len(body_rounds) - 1):
            assert body_rounds[i + 1] - body_rounds[i] == 1, (
                "Body rounds should be consecutive"
            )


class TestCylinderCapSections:
    """Tests for hemisphere cap logic in capped cylinders."""

    def test_caps_use_hemisphere_logic(self):
        """Verify caps use smooth hemisphere increase/decrease."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=8, height_cm=12, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        stitch_counts = [r.total_stitches for r in pattern.rounds]

        # Find equator (max stitch count)
        equator_index = stitch_counts.index(max(stitch_counts))

        # Bottom cap: should start at 6 and increase monotonically
        assert stitch_counts[0] == 6, "Should start with magic ring (6 stitches)"
        for i in range(equator_index):
            assert stitch_counts[i] <= stitch_counts[i + 1], (
                f"Bottom cap should increase monotonically at round {i}"
            )

        # Top cap: should decrease monotonically to 6
        cap_start = equator_index
        for i in range(equator_index, len(stitch_counts) - 1):
            if stitch_counts[i] != stitch_counts[i + 1]:
                # Once decreases start, they should be monotonic
                cap_start = i
                break

        for i in range(cap_start, len(stitch_counts) - 1):
            assert stitch_counts[i] >= stitch_counts[i + 1], (
                f"Top cap should decrease monotonically at round {i}"
            )

        # Should end near 6 stitches (closing)
        assert stitch_counts[-1] <= 10, "Should close to small stitch count"


class TestCylinderDimensions:
    """Tests for various cylinder dimensions."""

    def test_very_tall_cylinder(self):
        """Test very tall cylinder (height >> diameter)."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=4, height_cm=20, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        # Calculate expected body rounds
        expected_body_rounds = round((gauge.rows_per_10cm / 10) * 20)
        assert len(pattern.rounds) > expected_body_rounds

        # Verify tall structure
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        max_count = max(stitch_counts)
        body_rounds = [count for count in stitch_counts if count == max_count]

        # Most rounds should be body rounds for tall cylinder
        assert len(body_rounds) >= expected_body_rounds * 0.8

    def test_short_wide_cylinder(self):
        """Test short wide cylinder (diameter >> height)."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=12, height_cm=4, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        # Verify large circumference
        expected_circumference = round(3.14159 * 12 * 14 / 10)
        max_stitches = max(r.total_stitches for r in pattern.rounds)
        assert abs(max_stitches - expected_circumference) <= 3

        # Body should be relatively short
        stitch_counts = [r.total_stitches for r in pattern.rounds]
        body_rounds = [count for count in stitch_counts if count == max_stitches]
        assert len(body_rounds) <= 10  # Short body


class TestCylinderGauge:
    """Tests for different gauge specifications."""

    def test_different_gauges(self):
        """Test cylinder generation with various gauges."""
        compiler = CylinderCompiler()

        # Fine gauge (DK yarn)
        gauge_fine = Gauge(sts_per_10cm=18, rows_per_10cm=20)
        pattern_fine = compiler.generate(
            diameter_cm=8, height_cm=10, gauge=gauge_fine, has_caps=True, yarn_weight="DK"
        )
        assert pattern_fine.gauge.stitches_per_cm == 1.8
        assert pattern_fine.gauge.rows_per_cm == 2.0

        # Coarse gauge (bulky yarn)
        gauge_coarse = Gauge(sts_per_10cm=10, rows_per_10cm=12)
        pattern_coarse = compiler.generate(
            diameter_cm=8,
            height_cm=10,
            gauge=gauge_coarse,
            has_caps=True,
            yarn_weight="Bulky",
        )
        assert pattern_coarse.gauge.stitches_per_cm == 1.0
        assert pattern_coarse.gauge.rows_per_cm == 1.2

        # Fine gauge should have more rounds than coarse gauge
        assert len(pattern_fine.rounds) > len(pattern_coarse.rounds)


class TestCylinderPerformance:
    """Performance tests for cylinder generation."""

    def test_performance_under_150ms(self):
        """Verify pattern generation completes in < 150ms."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        # Test multiple sizes
        test_cases = [
            (6, 12, True),
            (8, 15, True),
            (10, 20, False),
            (4, 8, True),
        ]

        for diameter, height, has_caps in test_cases:
            start_time = time.perf_counter()
            pattern = compiler.generate(
                diameter_cm=diameter,
                height_cm=height,
                gauge=gauge,
                has_caps=has_caps,
                yarn_weight="Worsted",
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            assert elapsed_ms < 150, (
                f"Generation took {elapsed_ms:.2f}ms for "
                f"{diameter}cm×{height}cm (limit: 150ms)"
            )
            assert len(pattern.rounds) > 0


class TestCylinderSerialization:
    """Tests for JSON serialization and deserialization."""

    def test_json_serialization_roundtrip(self):
        """Test that pattern can be serialized to JSON and back."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        original = compiler.generate(
            diameter_cm=8, height_cm=12, gauge=gauge, has_caps=True, yarn_weight="Worsted"
        )

        # Serialize to JSON
        json_str = original.model_dump_json(indent=2)
        assert len(json_str) > 100

        # Deserialize back to PatternDSL
        restored = PatternDSL.model_validate_json(json_str)

        # Verify structure matches
        assert restored.shape.shape_type == original.shape.shape_type
        assert restored.shape.diameter_cm == original.shape.diameter_cm
        assert restored.shape.height_cm == original.shape.height_cm
        assert len(restored.rounds) == len(original.rounds)
        assert restored.metadata.total_rounds == original.metadata.total_rounds

        # Verify first and last rounds match
        assert (
            restored.rounds[0].total_stitches == original.rounds[0].total_stitches
        )
        assert (
            restored.rounds[-1].total_stitches == original.rounds[-1].total_stitches
        )

    def test_json_contains_expected_fields(self):
        """Test that serialized JSON contains all expected fields."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        pattern = compiler.generate(
            diameter_cm=6, height_cm=10, gauge=gauge, has_caps=False, yarn_weight="Worsted"
        )

        json_str = pattern.model_dump_json()

        # Verify key fields are present (JSON is minified without spaces)
        assert '"shape_type":"cylinder"' in json_str
        assert '"diameter_cm"' in json_str
        assert '"height_cm"' in json_str
        assert '"rounds"' in json_str
        assert '"total_stitches"' in json_str
        assert '"stitch_type"' in json_str
        assert '"metadata"' in json_str
