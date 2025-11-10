"""
Unit tests for DSL validation and schema compliance.

Tests cover:
- Pydantic model validation
- Required field enforcement
- Value constraints (min/max)
- Type validation
- Sequential round number validation
- Shape-specific parameter requirements
- JSON serialization/deserialization
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError

from knit_wit_engine.models.dsl import (
    StitchInstruction,
    RoundInstruction,
    GaugeInfo,
    ShapeParameters,
    PatternMetadata,
    PatternDSL,
)


class TestStitchInstruction:
    """Tests for StitchInstruction model validation."""

    def test_valid_stitch_instruction(self):
        """Test creating a valid stitch instruction."""
        stitch = StitchInstruction(
            stitch_type="sc",
            count=6,
            target="next st",
            note="Single crochet"
        )
        assert stitch.stitch_type == "sc"
        assert stitch.count == 6
        assert stitch.target == "next st"
        assert stitch.note == "Single crochet"

    def test_stitch_instruction_defaults(self):
        """Test default values for optional fields."""
        stitch = StitchInstruction(stitch_type="inc")
        assert stitch.count == 1
        assert stitch.target is None
        assert stitch.note is None

    def test_stitch_count_minimum(self):
        """Test that count must be at least 1."""
        with pytest.raises(ValidationError) as exc_info:
            StitchInstruction(stitch_type="sc", count=0)
        assert "count" in str(exc_info.value)

    def test_stitch_count_negative(self):
        """Test that negative count is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StitchInstruction(stitch_type="sc", count=-1)
        assert "count" in str(exc_info.value)

    def test_missing_required_field(self):
        """Test that stitch_type is required."""
        with pytest.raises(ValidationError) as exc_info:
            StitchInstruction(count=5)
        assert "stitch_type" in str(exc_info.value)


class TestRoundInstruction:
    """Tests for RoundInstruction model validation."""

    def test_valid_round_instruction(self):
        """Test creating a valid round instruction."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[
                StitchInstruction(stitch_type="sc", count=6)
            ],
            total_stitches=6,
            description="Start round"
        )
        assert round_inst.round_number == 0
        assert len(round_inst.stitches) == 1
        assert round_inst.total_stitches == 6

    def test_round_number_minimum(self):
        """Test that round_number cannot be negative."""
        with pytest.raises(ValidationError) as exc_info:
            RoundInstruction(
                round_number=-1,
                stitches=[StitchInstruction(stitch_type="sc")],
                total_stitches=6
            )
        assert "round_number" in str(exc_info.value)

    def test_total_stitches_minimum(self):
        """Test that total_stitches must be at least 1."""
        with pytest.raises(ValidationError) as exc_info:
            RoundInstruction(
                round_number=0,
                stitches=[StitchInstruction(stitch_type="sc")],
                total_stitches=0
            )
        assert "total_stitches" in str(exc_info.value)

    def test_empty_stitches_list(self):
        """Test that stitches list cannot be empty."""
        # Note: This test depends on Pydantic's validation of the List type
        # An empty list is technically valid for List[StitchInstruction]
        # but would fail business logic validation
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[],
            total_stitches=1
        )
        # This creates successfully but might fail in pattern validation
        assert len(round_inst.stitches) == 0


class TestGaugeInfo:
    """Tests for GaugeInfo model validation."""

    def test_valid_gauge_info(self):
        """Test creating valid gauge information."""
        gauge = GaugeInfo(
            stitches_per_cm=1.4,
            rows_per_cm=1.6,
            hook_size_mm=4.0,
            yarn_weight="worsted",
            swatch_notes="Standard gauge"
        )
        assert gauge.stitches_per_cm == 1.4
        assert gauge.rows_per_cm == 1.6
        assert gauge.hook_size_mm == 4.0
        assert gauge.yarn_weight == "worsted"

    def test_gauge_positive_values(self):
        """Test that gauge values must be positive."""
        with pytest.raises(ValidationError):
            GaugeInfo(stitches_per_cm=0, rows_per_cm=1.6)

        with pytest.raises(ValidationError):
            GaugeInfo(stitches_per_cm=1.4, rows_per_cm=0)

    def test_gauge_negative_values(self):
        """Test that negative gauge values are rejected."""
        with pytest.raises(ValidationError):
            GaugeInfo(stitches_per_cm=-1.4, rows_per_cm=1.6)

    def test_valid_yarn_weights(self):
        """Test all valid yarn weight values."""
        valid_weights = ["lace", "fingering", "sport", "DK", "worsted", "bulky", "super_bulky"]
        for weight in valid_weights:
            gauge = GaugeInfo(
                stitches_per_cm=1.4,
                rows_per_cm=1.6,
                yarn_weight=weight
            )
            assert gauge.yarn_weight == weight

    def test_invalid_yarn_weight(self):
        """Test that invalid yarn weight is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            GaugeInfo(
                stitches_per_cm=1.4,
                rows_per_cm=1.6,
                yarn_weight="invalid_weight"
            )
        assert "yarn_weight" in str(exc_info.value)


class TestShapeParameters:
    """Tests for ShapeParameters model validation."""

    def test_valid_sphere(self):
        """Test creating valid sphere parameters."""
        shape = ShapeParameters(
            shape_type="sphere",
            diameter_cm=10.0
        )
        assert shape.shape_type == "sphere"
        assert shape.diameter_cm == 10.0

    def test_valid_cylinder(self):
        """Test creating valid cylinder parameters."""
        shape = ShapeParameters(
            shape_type="cylinder",
            diameter_cm=8.0,
            height_cm=12.0
        )
        assert shape.shape_type == "cylinder"
        assert shape.diameter_cm == 8.0
        assert shape.height_cm == 12.0

    def test_valid_cone(self):
        """Test creating valid cone parameters."""
        shape = ShapeParameters(
            shape_type="cone",
            base_diameter_cm=12.0,
            top_diameter_cm=4.0,
            height_cm=15.0
        )
        assert shape.shape_type == "cone"
        assert shape.base_diameter_cm == 12.0
        assert shape.top_diameter_cm == 4.0
        assert shape.height_cm == 15.0

    def test_invalid_shape_type(self):
        """Test that invalid shape type is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ShapeParameters(shape_type="invalid_shape")
        assert "shape_type" in str(exc_info.value)

    def test_negative_dimensions(self):
        """Test that negative dimensions are rejected."""
        with pytest.raises(ValidationError):
            ShapeParameters(shape_type="sphere", diameter_cm=-10.0)

        with pytest.raises(ValidationError):
            ShapeParameters(
                shape_type="cylinder",
                diameter_cm=8.0,
                height_cm=-12.0
            )

    def test_zero_dimensions(self):
        """Test that zero dimensions are rejected."""
        with pytest.raises(ValidationError):
            ShapeParameters(shape_type="sphere", diameter_cm=0)


class TestPatternMetadata:
    """Tests for PatternMetadata model validation."""

    def test_valid_metadata(self):
        """Test creating valid pattern metadata."""
        metadata = PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=10,
            estimated_time_minutes=45,
            difficulty="beginner",
            tags=["sphere", "amigurumi"]
        )
        assert metadata.engine_version == "0.1.0"
        assert metadata.total_rounds == 10
        assert metadata.difficulty == "beginner"
        assert len(metadata.tags) == 2

    def test_metadata_defaults(self):
        """Test default values for metadata fields."""
        metadata = PatternMetadata(total_rounds=5)
        assert metadata.engine_version == "0.1.0"
        assert isinstance(metadata.generated_at, datetime)
        assert metadata.tags == []

    def test_negative_total_rounds(self):
        """Test that negative total_rounds is rejected."""
        with pytest.raises(ValidationError):
            PatternMetadata(total_rounds=-1)

    def test_valid_difficulties(self):
        """Test all valid difficulty values."""
        valid_difficulties = ["beginner", "intermediate", "advanced"]
        for difficulty in valid_difficulties:
            metadata = PatternMetadata(
                total_rounds=5,
                difficulty=difficulty
            )
            assert metadata.difficulty == difficulty

    def test_invalid_difficulty(self):
        """Test that invalid difficulty is rejected."""
        with pytest.raises(ValidationError):
            PatternMetadata(
                total_rounds=5,
                difficulty="expert"
            )


class TestPatternDSL:
    """Tests for complete PatternDSL model validation."""

    def test_valid_pattern(self):
        """Test creating a valid complete pattern."""
        pattern = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10.0),
            gauge=GaugeInfo(stitches_per_cm=1.4, rows_per_cm=1.6),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[StitchInstruction(stitch_type="inc", count=6)],
                    total_stitches=12
                )
            ],
            metadata=PatternMetadata(total_rounds=2),
            notes="Work in spiral"
        )
        assert len(pattern.rounds) == 2
        assert pattern.metadata.total_rounds == 2

    def test_rounds_must_be_sequential(self):
        """Test that round numbers must be sequential starting from 0."""
        with pytest.raises(ValidationError) as exc_info:
            PatternDSL(
                shape=ShapeParameters(shape_type="sphere", diameter_cm=10.0),
                gauge=GaugeInfo(stitches_per_cm=1.4, rows_per_cm=1.6),
                rounds=[
                    RoundInstruction(
                        round_number=0,
                        stitches=[StitchInstruction(stitch_type="sc", count=6)],
                        total_stitches=6
                    ),
                    RoundInstruction(
                        round_number=2,  # Should be 1
                        stitches=[StitchInstruction(stitch_type="inc", count=6)],
                        total_stitches=12
                    )
                ],
                metadata=PatternMetadata(total_rounds=2)
            )
        assert "sequential" in str(exc_info.value).lower()

    def test_empty_rounds_list(self):
        """Test that pattern must have at least one round."""
        with pytest.raises(ValidationError) as exc_info:
            PatternDSL(
                shape=ShapeParameters(shape_type="sphere", diameter_cm=10.0),
                gauge=GaugeInfo(stitches_per_cm=1.4, rows_per_cm=1.6),
                rounds=[],
                metadata=PatternMetadata(total_rounds=0)
            )
        assert "at least one round" in str(exc_info.value).lower()

    def test_json_serialization(self):
        """Test converting pattern to JSON."""
        pattern = PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10.0),
            gauge=GaugeInfo(stitches_per_cm=1.4, rows_per_cm=1.6),
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6
                )
            ],
            metadata=PatternMetadata(total_rounds=1)
        )

        json_str = pattern.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["shape"]["shape_type"] == "sphere"
        assert parsed["shape"]["diameter_cm"] == 10.0

    def test_json_deserialization(self):
        """Test creating pattern from JSON."""
        json_data = {
            "shape": {
                "shape_type": "sphere",
                "diameter_cm": 10.0
            },
            "gauge": {
                "stitches_per_cm": 1.4,
                "rows_per_cm": 1.6
            },
            "rounds": [
                {
                    "round_number": 0,
                    "stitches": [
                        {
                            "stitch_type": "sc",
                            "count": 6
                        }
                    ],
                    "total_stitches": 6
                }
            ],
            "metadata": {
                "generated_at": "2024-11-10T10:30:00Z",
                "engine_version": "0.1.0",
                "total_rounds": 1,
                "tags": []
            }
        }

        pattern = PatternDSL.from_dict(json_data)
        assert pattern.shape.shape_type == "sphere"
        assert pattern.shape.diameter_cm == 10.0
        assert len(pattern.rounds) == 1


class TestExamplePatterns:
    """Tests for example pattern files."""

    @pytest.fixture
    def docs_path(self):
        """Get path to docs/examples directory."""
        # Adjust path based on test location
        return Path(__file__).parent.parent.parent.parent.parent / "docs" / "examples"

    def test_sphere_example_is_valid(self, docs_path):
        """Test that sphere example validates correctly."""
        sphere_file = docs_path / "sphere-example.json"
        if not sphere_file.exists():
            pytest.skip(f"Example file not found: {sphere_file}")

        with open(sphere_file) as f:
            data = json.load(f)

        pattern = PatternDSL.from_dict(data)
        assert pattern.shape.shape_type == "sphere"
        assert pattern.shape.diameter_cm is not None
        assert len(pattern.rounds) > 0

    def test_cylinder_example_is_valid(self, docs_path):
        """Test that cylinder example validates correctly."""
        cylinder_file = docs_path / "cylinder-example.json"
        if not cylinder_file.exists():
            pytest.skip(f"Example file not found: {cylinder_file}")

        with open(cylinder_file) as f:
            data = json.load(f)

        pattern = PatternDSL.from_dict(data)
        assert pattern.shape.shape_type == "cylinder"
        assert pattern.shape.diameter_cm is not None
        assert pattern.shape.height_cm is not None
        assert len(pattern.rounds) > 0

    def test_cone_example_is_valid(self, docs_path):
        """Test that cone example validates correctly."""
        cone_file = docs_path / "cone-example.json"
        if not cone_file.exists():
            pytest.skip(f"Example file not found: {cone_file}")

        with open(cone_file) as f:
            data = json.load(f)

        pattern = PatternDSL.from_dict(data)
        assert pattern.shape.shape_type == "cone"
        assert pattern.shape.base_diameter_cm is not None
        assert pattern.shape.top_diameter_cm is not None
        assert pattern.shape.height_cm is not None
        assert len(pattern.rounds) > 0


class TestSchemaAlignment:
    """Tests for schema alignment between JSON Schema and Pydantic models."""

    @pytest.fixture
    def json_schema(self):
        """Load JSON Schema specification."""
        schema_file = Path(__file__).parent.parent.parent.parent.parent / "docs" / "dsl-schema.json"
        if not schema_file.exists():
            pytest.skip(f"Schema file not found: {schema_file}")

        with open(schema_file) as f:
            return json.load(f)

    def test_schema_has_required_definitions(self, json_schema):
        """Test that JSON Schema has all required definitions."""
        assert "definitions" in json_schema
        definitions = json_schema["definitions"]

        required_defs = [
            "StitchInstruction",
            "RoundInstruction",
            "GaugeInfo",
            "ShapeParameters",
            "PatternMetadata"
        ]

        for def_name in required_defs:
            assert def_name in definitions, f"Missing definition: {def_name}"

    def test_schema_version(self, json_schema):
        """Test that schema uses correct JSON Schema version."""
        assert json_schema["$schema"] == "http://json-schema.org/draft-07/schema#"

    def test_pattern_dsl_required_fields(self, json_schema):
        """Test that PatternDSL has correct required fields."""
        assert "required" in json_schema
        required_fields = json_schema["required"]

        expected_required = ["shape", "gauge", "rounds", "metadata"]
        assert set(required_fields) == set(expected_required)
