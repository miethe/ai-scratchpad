"""
Unit tests for PatternParserService

Tests the parser service for canonical bracket/repeat grammar parsing.
"""

import pytest
import sys
from pathlib import Path

# Add pattern engine to Python path
pattern_engine_path = (
    Path(__file__).resolve().parents[5] / "packages" / "pattern-engine"
)
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from app.services.parser_service import PatternParserService, ParserError
from knit_wit_engine.models.dsl import PatternParseDSL


@pytest.fixture
def parser_service():
    """Create parser service instance."""
    return PatternParserService()


class TestBasicParsing:
    """Test basic pattern parsing functionality."""

    def test_parse_magic_ring(self, parser_service):
        """Test parsing magic ring notation."""
        text = "R1: MR 6 sc (6)"
        result = parser_service.parse(text)

        assert isinstance(result, PatternParseDSL)
        assert len(result.rounds) == 1
        assert result.rounds[0].r == 1
        assert result.rounds[0].stitches == 6
        assert len(result.rounds[0].ops) >= 1
        # First op should be MR
        assert result.rounds[0].ops[0].op == "MR"
        assert result.rounds[0].ops[0].count == 1

    def test_parse_simple_repetition(self, parser_service):
        """Test parsing simple repetition with x syntax."""
        text = "R2: inc x6 (12)"
        result = parser_service.parse(text)

        assert len(result.rounds) == 1
        assert result.rounds[0].r == 2
        assert result.rounds[0].stitches == 12
        assert len(result.rounds[0].ops) == 1
        assert result.rounds[0].ops[0].op == "inc"
        assert result.rounds[0].ops[0].count == 6

    def test_parse_bracket_sequence(self, parser_service):
        """Test parsing bracket sequence notation."""
        text = "R3: [2 sc, inc] x6 (18)"
        result = parser_service.parse(text)

        assert len(result.rounds) == 1
        round_dsl = result.rounds[0]
        assert round_dsl.r == 3
        assert round_dsl.stitches == 18

        # Should have one sequence operation
        assert len(round_dsl.ops) == 1
        seq_op = round_dsl.ops[0]
        assert seq_op.op == "seq"
        assert seq_op.repeat == 6
        assert seq_op.count == 18

        # Check inner operations
        assert len(seq_op.ops) == 2
        assert seq_op.ops[0].op == "sc"
        assert seq_op.ops[0].count == 2
        assert seq_op.ops[1].op == "inc"
        assert seq_op.ops[1].count == 1

    def test_parse_multiple_rounds(self, parser_service):
        """Test parsing multiple rounds."""
        text = """
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
R4: [3 sc, inc] x6 (24)
"""
        result = parser_service.parse(text)

        assert len(result.rounds) == 4
        assert result.rounds[0].r == 1
        assert result.rounds[1].r == 2
        assert result.rounds[2].r == 3
        assert result.rounds[3].r == 4


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_parse_empty_text(self, parser_service):
        """Test parsing empty text raises error."""
        with pytest.raises(ParserError, match="Empty pattern text"):
            parser_service.parse("")

    def test_parse_no_valid_rounds(self, parser_service):
        """Test parsing text with no valid rounds."""
        text = "# Just a comment\n\n"
        with pytest.raises(ParserError, match="No valid rounds found"):
            parser_service.parse(text)

    def test_parse_invalid_round_format(self, parser_service):
        """Test parsing invalid round format."""
        text = "Round 1: sc x6 (6)"  # Wrong format
        with pytest.raises(ParserError, match="Invalid round format"):
            parser_service.parse(text)

    def test_parse_missing_stitch_count(self, parser_service):
        """Test parsing round without stitch count."""
        text = "R1: sc x6"  # Missing (6)
        with pytest.raises(ParserError, match="Invalid round format"):
            parser_service.parse(text)

    def test_parse_invalid_stitch_count(self, parser_service):
        """Test parsing with invalid stitch count."""
        text = "R1: sc x6 (0)"  # Invalid count
        with pytest.raises(ParserError, match="Invalid stitch count"):
            parser_service.parse(text)

    def test_parse_unsupported_stitch(self, parser_service):
        """Test parsing with unsupported stitch type."""
        text = "R1: bobble x6 (6)"  # Unsupported stitch
        with pytest.raises(ParserError, match="Unsupported stitch type"):
            parser_service.parse(text)

    def test_parse_negative_count(self, parser_service):
        """Test parsing with negative count."""
        text = "R1: sc x-6 (6)"
        with pytest.raises(ParserError):
            parser_service.parse(text)

    def test_parse_comments_and_empty_lines(self, parser_service):
        """Test that comments and empty lines are skipped."""
        text = """
# This is a comment
R1: MR 6 sc (6)

# Another comment
R2: inc x6 (12)
"""
        result = parser_service.parse(text)
        assert len(result.rounds) == 2


class TestComplexPatterns:
    """Test complex pattern parsing scenarios."""

    def test_parse_mixed_operations(self, parser_service):
        """Test parsing round with mixed operations."""
        text = "R5: sc, inc x5, sc (7)"
        result = parser_service.parse(text)

        round_dsl = result.rounds[0]
        assert round_dsl.r == 5
        assert round_dsl.stitches == 7
        # Should have 3 operations: sc, inc x5, sc
        assert len(round_dsl.ops) == 3

    def test_parse_count_before_stitch(self, parser_service):
        """Test parsing with count before stitch."""
        text = "R1: 6 sc (6)"
        result = parser_service.parse(text)

        round_dsl = result.rounds[0]
        assert round_dsl.stitches == 6
        assert round_dsl.ops[0].op == "sc"
        assert round_dsl.ops[0].count == 6

    def test_parse_multiple_brackets(self, parser_service):
        """Test parsing multiple bracket sequences in one round."""
        text = "R1: [sc, inc] x3, [2 sc, inc] x2 (12)"
        result = parser_service.parse(text)

        round_dsl = result.rounds[0]
        # Should have 2 sequence operations
        assert len(round_dsl.ops) == 2
        assert round_dsl.ops[0].op == "seq"
        assert round_dsl.ops[0].repeat == 3
        assert round_dsl.ops[1].op == "seq"
        assert round_dsl.ops[1].repeat == 2

    def test_parse_no_spaces_in_brackets(self, parser_service):
        """Test parsing brackets with no spaces."""
        text = "R1: [sc,inc]x6 (12)"
        result = parser_service.parse(text)

        round_dsl = result.rounds[0]
        assert round_dsl.ops[0].op == "seq"
        assert round_dsl.ops[0].repeat == 6


class TestValidation:
    """Test validation functionality."""

    def test_validate_correct_stitch_count(self, parser_service):
        """Test validation passes for correct stitch count."""
        text = "R1: MR 6 sc (6)\nR2: inc x6 (12)"
        dsl = parser_service.parse(text)
        validation = parser_service.validate_parse(dsl)

        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

    def test_validate_incorrect_stitch_count(self, parser_service):
        """Test validation fails for incorrect stitch count."""
        # Parse text with intentionally wrong stitch count
        text = "R1: inc x6 (10)"  # Should be 6, not 10
        dsl = parser_service.parse(text)
        validation = parser_service.validate_parse(dsl)

        assert validation["valid"] is False
        assert len(validation["errors"]) > 0
        assert "stitch count mismatch" in validation["errors"][0].lower()

    def test_validate_bracket_sequence_count(self, parser_service):
        """Test validation of bracket sequence stitch counts."""
        text = "R1: [2 sc, inc] x6 (18)"
        dsl = parser_service.parse(text)
        validation = parser_service.validate_parse(dsl)

        assert validation["valid"] is True
        # 2 sc + 1 inc = 3 stitches per sequence
        # 3 * 6 repeats = 18 total

    def test_validate_non_sequential_rounds(self, parser_service):
        """Test validation warns about non-sequential round numbers."""
        text = "R1: sc x6 (6)\nR5: inc x6 (12)"  # Skips rounds 2-4
        dsl = parser_service.parse(text)
        validation = parser_service.validate_parse(dsl)

        # Should have warnings but still be valid
        assert len(validation["warnings"]) > 0
        assert "non-sequential" in validation["warnings"][0].lower()

    def test_validate_empty_pattern(self, parser_service):
        """Test validation of pattern with no rounds."""
        # Create pattern manually with no rounds
        from knit_wit_engine.models.dsl import MetaDSL, ObjectDSL

        dsl = PatternParseDSL(
            meta=MetaDSL(),
            object=ObjectDSL(type="unknown", params={}),
            rounds=[],
            materials={},
            notes=[],
        )
        validation = parser_service.validate_parse(dsl)

        assert validation["valid"] is False
        assert any("no rounds" in err.lower() for err in validation["errors"])


class TestStitchTypes:
    """Test parsing of different stitch types."""

    @pytest.mark.parametrize(
        "stitch",
        ["sc", "inc", "dec", "hdc", "dc", "slst", "ch", "MR"],
    )
    def test_parse_supported_stitches(self, parser_service, stitch):
        """Test parsing all supported stitch types."""
        text = f"R1: {stitch} x6 (6)" if stitch != "MR" else "R1: MR (1)"
        result = parser_service.parse(text)

        assert len(result.rounds) == 1
        assert result.rounds[0].ops[0].op == stitch

    def test_parse_case_insensitive_mr(self, parser_service):
        """Test that MR is case-insensitive."""
        text = "R1: mr (1)"
        result = parser_service.parse(text)

        assert result.rounds[0].ops[0].op == "MR"


class TestPerformance:
    """Test parser performance."""

    def test_parse_large_pattern(self, parser_service):
        """Test parsing a large pattern completes quickly."""
        import time

        # Generate a 50-round pattern
        rounds = [f"R{i}: [2 sc, inc] x6 (18)" for i in range(1, 51)]
        text = "\n".join(rounds)

        start = time.time()
        result = parser_service.parse(text)
        duration = time.time() - start

        assert len(result.rounds) == 50
        # Should complete in < 200ms as per requirement
        assert duration < 0.2, f"Parse took {duration:.3f}s, expected < 0.2s"


class TestDSLStructure:
    """Test generated DSL structure."""

    def test_dsl_has_required_fields(self, parser_service):
        """Test that generated DSL has all required fields."""
        text = "R1: MR 6 sc (6)"
        result = parser_service.parse(text)

        assert result.meta is not None
        assert result.object is not None
        assert result.rounds is not None
        assert result.materials is not None
        assert result.notes is not None

    def test_dsl_meta_defaults(self, parser_service):
        """Test that DSL meta has correct defaults."""
        text = "R1: sc x6 (6)"
        result = parser_service.parse(text)

        assert result.meta.version == "0.1"
        assert result.meta.terms == "US"
        assert result.meta.stitch == "sc"
        assert result.meta.round_mode == "spiral"

    def test_dsl_serialization(self, parser_service):
        """Test that DSL can be serialized to dict/JSON."""
        text = "R1: MR 6 sc (6)\nR2: inc x6 (12)"
        result = parser_service.parse(text)

        # Test to_dict
        dsl_dict = result.to_dict()
        assert isinstance(dsl_dict, dict)
        assert "meta" in dsl_dict
        assert "rounds" in dsl_dict

        # Test to_json
        dsl_json = result.to_json()
        assert isinstance(dsl_json, str)
        assert "meta" in dsl_json


class TestErrorMessages:
    """Test error message quality."""

    def test_error_includes_line_number(self, parser_service):
        """Test that errors include line numbers."""
        text = "R1: sc x6 (6)\nR2: invalid syntax here (12)"
        with pytest.raises(ParserError) as exc_info:
            parser_service.parse(text)

        assert "Line 2" in str(exc_info.value)

    def test_error_suggests_supported_stitches(self, parser_service):
        """Test that unsupported stitch errors suggest alternatives."""
        text = "R1: bobble x6 (6)"
        with pytest.raises(ParserError) as exc_info:
            parser_service.parse(text)

        error_msg = str(exc_info.value)
        assert "Unsupported stitch type" in error_msg
        assert "Supported:" in error_msg
        # Should list some supported stitches
        assert "sc" in error_msg or "inc" in error_msg

    def test_error_clear_for_missing_bracket(self, parser_service):
        """Test clear error for missing closing bracket."""
        text = "R1: [sc, inc x6 (6)"  # Missing ]
        with pytest.raises(ParserError):
            parser_service.parse(text)
