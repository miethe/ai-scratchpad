"""
Unit Tests for Algorithm Modules

Comprehensive pytest suite for core algorithm modules:
- Even Distribution (distribution.py): Bresenham-like spacing for increases/decreases
- Gauge Calculations (gauge.py): Stitch length and yardage estimation
- Terminology Translator (translator.py): US ↔ UK stitch term translation

Test Coverage Target: 80%+
"""

import pytest

from knit_wit_engine.algorithms.distribution import even_distribution, jitter_offset
from knit_wit_engine.algorithms.gauge import (
    gauge_to_stitch_length,
    estimate_yardage,
)
from knit_wit_engine.algorithms.translator import (
    translate_term,
    translate_pattern_dsl,
)
from knit_wit_engine.models.requests import Gauge
from knit_wit_engine.models.dsl import (
    PatternDSL,
    RoundInstruction,
    StitchInstruction,
    GaugeInfo,
    ShapeParameters,
    PatternMetadata,
)


class TestEvenDistribution:
    """Tests for even_distribution algorithm (Bresenham-like spacing)."""

    def test_perfect_division_36_stitches_6_changes(self):
        """Test perfect division: 36 stitches, 6 changes → [6, 12, 18, 24, 30, 36]."""
        indices = even_distribution(total_stitches=36, num_changes=6)

        assert indices == [6, 12, 18, 24, 30, 36], (
            "Perfect division should space changes evenly"
        )
        assert len(indices) == 6
        assert all(i >= 1 and i <= 36 for i in indices)

    def test_imperfect_division_37_stitches_6_changes(self):
        """Test imperfect division: 37 stitches, 6 changes → gaps of 6 and 7."""
        indices = even_distribution(total_stitches=37, num_changes=6)

        assert len(indices) == 6
        assert all(i >= 1 and i <= 37 for i in indices)

        # Calculate gaps between consecutive indices
        gaps = [indices[i + 1] - indices[i] for i in range(len(indices) - 1)]

        # For 37/6, gap should alternate between 6 and 7
        assert all(gap in [6, 7] for gap in gaps), (
            f"Gaps should be 6 or 7 for 37 stitches / 6 changes, got: {gaps}"
        )

        # Verify indices are sorted and unique
        assert indices == sorted(set(indices))

    def test_edge_case_zero_changes(self):
        """Test edge case: 0 changes returns empty list."""
        indices = even_distribution(total_stitches=20, num_changes=0)
        assert indices == []

    def test_edge_case_one_change(self):
        """Test edge case: 1 change in middle of round."""
        indices = even_distribution(total_stitches=20, num_changes=1)
        assert len(indices) == 1
        assert indices[0] >= 1 and indices[0] <= 20

    def test_edge_case_changes_equal_stitches(self):
        """Test edge case: num_changes == total_stitches."""
        indices = even_distribution(total_stitches=5, num_changes=5)
        assert indices == [1, 2, 3, 4, 5]

    def test_edge_case_changes_exceed_stitches(self):
        """Test edge case: num_changes > total_stitches."""
        indices = even_distribution(total_stitches=5, num_changes=10)
        # Should return one change per stitch
        assert indices == [1, 2, 3, 4, 5]

    def test_offset_behavior(self):
        """Test jitter offset shifts positions correctly."""
        # Without offset
        indices_base = even_distribution(total_stitches=36, num_changes=6, offset=0)

        # With offset of 3
        indices_offset = even_distribution(total_stitches=36, num_changes=6, offset=3)

        # All indices should be shifted
        assert indices_base != indices_offset

        # Both should have same length
        assert len(indices_base) == len(indices_offset) == 6

        # With wrapping offset
        indices_wrap = even_distribution(total_stitches=42, num_changes=7, offset=3)
        assert len(indices_wrap) == 7
        assert all(i >= 1 and i <= 42 for i in indices_wrap)

    def test_distribution_variance(self):
        """Test that distribution minimizes variance in spacing."""
        # Test multiple imperfect divisions
        test_cases = [
            (37, 6),
            (50, 7),
            (100, 13),
        ]

        for total_stitches, num_changes in test_cases:
            indices = even_distribution(total_stitches, num_changes)
            assert len(indices) == num_changes

            # Calculate gaps
            gaps = [indices[i + 1] - indices[i] for i in range(len(indices) - 1)]

            # Maximum gap should be at most 1 more than minimum gap
            # (Bresenham property: even distribution)
            if gaps:
                assert max(gaps) - min(gaps) <= 1, (
                    f"Distribution variance too high for {total_stitches}/{num_changes}"
                )


class TestJitterOffset:
    """Tests for jitter_offset function."""

    def test_alternating_offset(self):
        """Test that jitter alternates by round number."""
        offset_r1 = jitter_offset(round_number=1)
        offset_r2 = jitter_offset(round_number=2)
        offset_r3 = jitter_offset(round_number=3)
        offset_r4 = jitter_offset(round_number=4)

        # Odd rounds should have +3 offset
        assert offset_r1 == 3
        assert offset_r3 == 3

        # Even rounds should have 0 offset
        assert offset_r2 == 0
        assert offset_r4 == 0

    def test_base_offset_addition(self):
        """Test that base_offset is added to jitter."""
        offset_r1_base5 = jitter_offset(round_number=1, base_offset=5)
        offset_r2_base5 = jitter_offset(round_number=2, base_offset=5)

        assert offset_r1_base5 == 8  # 5 + 3
        assert offset_r2_base5 == 5  # 5 + 0

    def test_consistent_pattern(self):
        """Test that jitter pattern is consistent across rounds."""
        # Generate offsets for rounds 1-10
        offsets = [jitter_offset(i) for i in range(1, 11)]

        # Expected pattern: [3, 0, 3, 0, 3, 0, 3, 0, 3, 0]
        expected = [3, 0, 3, 0, 3, 0, 3, 0, 3, 0]
        assert offsets == expected


class TestGaugeToStitchLength:
    """Tests for gauge_to_stitch_length function."""

    def test_standard_gauge_worsted_yarn(self):
        """Test standard gauge (14 sts/10cm) with worsted yarn."""
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        stitch_length = gauge_to_stitch_length(gauge, "Worsted")

        # Expected: (10 / 14) × 0.7 = 0.5 cm
        assert abs(stitch_length - 0.5) < 0.01

    def test_fine_gauge_dk_yarn(self):
        """Test fine gauge (18 sts/10cm) with DK yarn."""
        gauge = Gauge(sts_per_10cm=18, rows_per_10cm=20)
        stitch_length = gauge_to_stitch_length(gauge, "DK")

        # Expected: (10 / 18) × 0.6 ≈ 0.333 cm
        expected = (10.0 / 18) * 0.6
        assert abs(stitch_length - expected) < 0.01

    def test_coarse_gauge_bulky_yarn(self):
        """Test coarse gauge (10 sts/10cm) with bulky yarn."""
        gauge = Gauge(sts_per_10cm=10, rows_per_10cm=12)
        stitch_length = gauge_to_stitch_length(gauge, "Bulky")

        # Expected: (10 / 10) × 0.9 = 0.9 cm
        assert abs(stitch_length - 0.9) < 0.01

    def test_very_fine_gauge_baby_yarn(self):
        """Test very fine gauge (24 sts/10cm) with baby yarn."""
        gauge = Gauge(sts_per_10cm=24, rows_per_10cm=28)
        stitch_length = gauge_to_stitch_length(gauge, "Baby")

        # Expected: (10 / 24) × 0.5 ≈ 0.208 cm
        expected = (10.0 / 24) * 0.5
        assert abs(stitch_length - expected) < 0.01

    def test_very_coarse_gauge(self):
        """Test very coarse gauge (6 sts/10cm) with bulky yarn."""
        gauge = Gauge(sts_per_10cm=6, rows_per_10cm=8)
        stitch_length = gauge_to_stitch_length(gauge, "Bulky")

        # Expected: (10 / 6) × 0.9 = 1.5 cm
        expected = (10.0 / 6) * 0.9
        assert abs(stitch_length - expected) < 0.01

    def test_unknown_yarn_weight_defaults_to_worsted(self):
        """Test that unknown yarn weight defaults to Worsted factor (0.7)."""
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        stitch_length = gauge_to_stitch_length(gauge, "UnknownWeight")

        # Should use default factor 0.7
        expected = (10.0 / 14) * 0.7
        assert abs(stitch_length - expected) < 0.01


class TestEstimateYardage:
    """Tests for estimate_yardage function."""

    def test_small_project_200_stitches(self):
        """Test yardage estimation for small amigurumi (~200 stitches)."""
        yardage = estimate_yardage(stitch_count=200, stitch_length=0.5)

        # Expected: (200 × 0.5) / 100 × 1.1 = 1.1 meters
        assert abs(yardage - 1.1) < 0.01

    def test_medium_project_1000_stitches(self):
        """Test yardage estimation for medium project (~1000 stitches)."""
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        stitch_len = gauge_to_stitch_length(gauge, "Worsted")
        yardage = estimate_yardage(1000, stitch_len)

        # stitch_len ≈ 0.5, so: (1000 × 0.5) / 100 × 1.1 = 5.5 meters
        assert abs(yardage - 5.5) < 0.1

    def test_large_project_bulky_yarn(self):
        """Test yardage estimation for large project with bulky yarn."""
        gauge = Gauge(sts_per_10cm=10, rows_per_10cm=12)
        stitch_len = gauge_to_stitch_length(gauge, "Bulky")
        yardage = estimate_yardage(800, stitch_len)

        # stitch_len ≈ 0.9, so: (800 × 0.9) / 100 × 1.1 = 7.92 meters
        assert abs(yardage - 7.92) < 0.1

    def test_waste_factor_applied(self):
        """Test that 10% waste factor is correctly applied."""
        # Without waste factor: 100 stitches × 1.0cm = 1.0 meter
        # With 10% waste: 1.0 × 1.1 = 1.1 meters
        yardage = estimate_yardage(stitch_count=100, stitch_length=1.0)
        assert abs(yardage - 1.1) < 0.01

    def test_zero_stitches(self):
        """Test edge case: zero stitches."""
        yardage = estimate_yardage(stitch_count=0, stitch_length=0.5)
        assert yardage == 0.0

    def test_very_large_project(self):
        """Test very large project (10000 stitches)."""
        yardage = estimate_yardage(stitch_count=10000, stitch_length=0.5)
        # Expected: (10000 × 0.5) / 100 × 1.1 = 55 meters
        assert abs(yardage - 55.0) < 0.1


class TestTranslateTerm:
    """Tests for translate_term function (US ↔ UK translation)."""

    def test_us_to_uk_sc_becomes_dc(self):
        """Test US → UK: 'sc' becomes 'dc'."""
        translated = translate_term("sc", from_convention="US", to_convention="UK")
        assert translated == "dc"

    def test_uk_to_us_dc_becomes_sc(self):
        """Test UK → US: 'dc' becomes 'sc'."""
        translated = translate_term("dc", from_convention="UK", to_convention="US")
        assert translated == "sc"

    def test_same_terms_inc(self):
        """Test that 'inc' is the same in both conventions."""
        translated_us_to_uk = translate_term("inc", from_convention="US", to_convention="UK")
        translated_uk_to_us = translate_term("inc", from_convention="UK", to_convention="US")

        assert translated_us_to_uk == "inc"
        assert translated_uk_to_us == "inc"

    def test_same_terms_dec(self):
        """Test that 'dec' is the same in both conventions."""
        translated = translate_term("dec", from_convention="US", to_convention="UK")
        assert translated == "dec"

    def test_same_terms_ch(self):
        """Test that 'ch' is the same in both conventions."""
        translated = translate_term("ch", from_convention="US", to_convention="UK")
        assert translated == "ch"

    def test_same_terms_mr(self):
        """Test that 'MR' is the same in both conventions."""
        translated = translate_term("MR", from_convention="US", to_convention="UK")
        assert translated == "MR"

    def test_slst_us_to_uk(self):
        """Test US → UK: 'slst' becomes 'ss'."""
        translated = translate_term("slst", from_convention="US", to_convention="UK")
        assert translated == "ss"

    def test_ss_uk_to_us(self):
        """Test UK → US: 'ss' becomes 'slst'."""
        translated = translate_term("ss", from_convention="UK", to_convention="US")
        assert translated == "slst"

    def test_same_convention_returns_unchanged(self):
        """Test that same convention returns unchanged term (no-op)."""
        term_us = translate_term("sc", from_convention="US", to_convention="US")
        term_uk = translate_term("dc", from_convention="UK", to_convention="UK")

        assert term_us == "sc"
        assert term_uk == "dc"

    def test_unknown_us_term_raises_error(self):
        """Test that unknown US term raises ValueError."""
        with pytest.raises(ValueError, match="Unknown US term"):
            translate_term("hdc", from_convention="US", to_convention="UK")

    def test_unknown_uk_term_raises_error(self):
        """Test that unknown UK term raises ValueError."""
        with pytest.raises(ValueError, match="Unknown UK term"):
            translate_term("htr", from_convention="UK", to_convention="US")

    def test_invalid_convention_raises_error(self):
        """Test that invalid convention raises ValueError."""
        with pytest.raises(ValueError, match="Invalid source convention"):
            translate_term("sc", from_convention="INVALID", to_convention="UK")

        with pytest.raises(ValueError, match="Invalid target convention"):
            translate_term("sc", from_convention="US", to_convention="INVALID")


class TestTranslatePatternDSL:
    """Tests for translate_pattern_dsl function."""

    def test_translate_simple_pattern_us_to_uk(self):
        """Test translating a simple pattern from US to UK."""
        # Create simple US pattern
        us_pattern = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="MR", count=6)],
                    total_stitches=6,
                    description="Magic ring",
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[
                        StitchInstruction(stitch_type="inc", count=6),
                    ],
                    total_stitches=12,
                    description="Increase round",
                ),
                RoundInstruction(
                    round_number=2,
                    stitches=[
                        StitchInstruction(stitch_type="sc", count=1),
                        StitchInstruction(stitch_type="inc", count=1),
                    ],
                    total_stitches=18,
                    description="Pattern round",
                ),
            ],
            metadata=PatternMetadata(
                total_rounds=3, difficulty="beginner", tags=["sphere"]
            ),
        )

        # Translate to UK
        uk_pattern = translate_pattern_dsl(us_pattern, "US", "UK")

        # Verify translations
        assert uk_pattern.rounds[0].stitches[0].stitch_type == "MR"  # MR stays same
        assert uk_pattern.rounds[1].stitches[0].stitch_type == "inc"  # inc stays same
        assert uk_pattern.rounds[2].stitches[0].stitch_type == "dc"  # sc → dc
        assert uk_pattern.rounds[2].stitches[1].stitch_type == "inc"  # inc stays same

        # Verify structure unchanged
        assert len(uk_pattern.rounds) == len(us_pattern.rounds)
        assert uk_pattern.shape.diameter_cm == us_pattern.shape.diameter_cm

    def test_translate_pattern_uk_to_us(self):
        """Test translating a pattern from UK to US."""
        # Create UK pattern with 'dc' (which is 'sc' in US)
        uk_pattern = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="dc", count=12)],
                    total_stitches=12,
                    description="UK double crochet round",
                ),
            ],
            metadata=PatternMetadata(
                total_rounds=1, difficulty="beginner", tags=["sphere"]
            ),
        )

        # Translate to US
        us_pattern = translate_pattern_dsl(uk_pattern, "UK", "US")

        # Verify translation: UK 'dc' → US 'sc'
        assert us_pattern.rounds[0].stitches[0].stitch_type == "sc"

    def test_translate_same_convention_returns_copy(self):
        """Test that same convention returns deep copy (no-op)."""
        original = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                    description="Round",
                ),
            ],
            metadata=PatternMetadata(
                total_rounds=1, difficulty="beginner", tags=["sphere"]
            ),
        )

        # Translate US to US (no-op)
        copy = translate_pattern_dsl(original, "US", "US")

        # Should have same structure but be different object
        assert copy is not original
        assert copy.rounds[0].stitches[0].stitch_type == "sc"
        assert len(copy.rounds) == len(original.rounds)

    def test_translate_does_not_modify_original(self):
        """Test that translation creates new object without modifying original."""
        original = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                    description="Round",
                ),
            ],
            metadata=PatternMetadata(
                total_rounds=1, difficulty="beginner", tags=["sphere"]
            ),
        )

        # Translate to UK
        uk_pattern = translate_pattern_dsl(original, "US", "UK")

        # Original should still have 'sc'
        assert original.rounds[0].stitches[0].stitch_type == "sc"

        # Translated should have 'dc'
        assert uk_pattern.rounds[0].stitches[0].stitch_type == "dc"

    def test_translate_invalid_convention_raises_error(self):
        """Test that invalid convention raises ValueError."""
        pattern = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                    description="Test round",
                )
            ],
            metadata=PatternMetadata(
                total_rounds=1, difficulty="beginner", tags=["sphere"]
            ),
        )

        with pytest.raises(ValueError, match="Invalid source convention"):
            translate_pattern_dsl(pattern, "INVALID", "UK")

        with pytest.raises(ValueError, match="Invalid target convention"):
            translate_pattern_dsl(pattern, "US", "INVALID")

    def test_translate_multiple_rounds_with_mixed_stitches(self):
        """Test translating pattern with multiple rounds and mixed stitch types."""
        us_pattern = PatternDSL(
            shape=ShapeParameters(shape_type="cylinder", diameter_cm=8, height_cm=12),
            gauge=GaugeInfo(
                stitches_per_cm=1.4, rows_per_cm=1.6, yarn_weight="worsted"
            ),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[
                        StitchInstruction(stitch_type="ch", count=24),
                        StitchInstruction(stitch_type="slst", count=1),
                    ],
                    total_stitches=24,
                    description="Chain and join",
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[StitchInstruction(stitch_type="sc", count=24)],
                    total_stitches=24,
                    description="Body round",
                ),
                RoundInstruction(
                    round_number=2,
                    stitches=[
                        StitchInstruction(stitch_type="sc", count=10),
                        StitchInstruction(stitch_type="dec", count=2),
                        StitchInstruction(stitch_type="sc", count=10),
                    ],
                    total_stitches=22,
                    description="Decrease round",
                ),
            ],
            metadata=PatternMetadata(
                total_rounds=3, difficulty="intermediate", tags=["cylinder"]
            ),
        )

        # Translate to UK
        uk_pattern = translate_pattern_dsl(us_pattern, "US", "UK")

        # Verify all translations
        assert uk_pattern.rounds[0].stitches[0].stitch_type == "ch"  # ch stays same
        assert uk_pattern.rounds[0].stitches[1].stitch_type == "ss"  # slst → ss
        assert uk_pattern.rounds[1].stitches[0].stitch_type == "dc"  # sc → dc
        assert uk_pattern.rounds[2].stitches[0].stitch_type == "dc"  # sc → dc
        assert uk_pattern.rounds[2].stitches[1].stitch_type == "dec"  # dec stays same
        assert uk_pattern.rounds[2].stitches[2].stitch_type == "dc"  # sc → dc
