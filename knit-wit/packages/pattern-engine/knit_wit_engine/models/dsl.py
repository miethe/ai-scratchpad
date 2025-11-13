"""
Knit-Wit Pattern DSL Data Models

Defines the complete data structure for representing crochet patterns using Pydantic v2.
The DSL (Domain-Specific Language) provides a structured, type-safe way to represent
patterns that can be serialized to JSON and consumed by the frontend visualization.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


class StitchInstruction(BaseModel):
    """
    Represents a single stitch operation within a round.

    Examples:
        - "sc in next st" (single crochet in next stitch)
        - "inc" (increase - 2 sc in same stitch)
        - "dec" (decrease - sc2tog)
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    stitch_type: str = Field(
        ...,
        description="Type of stitch (sc, hdc, dc, inc, dec, etc.)",
        examples=["sc", "inc", "dec", "hdc", "dc"],
    )
    count: int = Field(
        default=1, ge=1, description="Number of times to repeat this stitch"
    )
    target: Optional[str] = Field(
        default=None,
        description="Where to place the stitch (next st, same st, etc.)",
        examples=["next st", "same st", "next 2 sts"],
    )
    note: Optional[str] = Field(
        default=None, description="Additional instruction or clarification"
    )


class RoundInstruction(BaseModel):
    """
    Represents a complete round (row) in the pattern.

    Each round contains one or more stitch instructions and metadata
    about the round number and total stitch count.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    round_number: int = Field(..., ge=0, description="Round number (0-indexed)")
    stitches: List[StitchInstruction] = Field(
        ..., description="List of stitch instructions for this round"
    )
    total_stitches: int = Field(
        ..., ge=1, description="Total stitch count after completing this round"
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable description of the round"
    )

    @field_validator("total_stitches")
    @classmethod
    def validate_total_stitches(cls, v: int, info) -> int:
        """Ensure total_stitches is positive."""
        if v < 1:
            raise ValueError("total_stitches must be at least 1")
        return v


class GaugeInfo(BaseModel):
    """
    Gauge information for the pattern.

    Gauge determines the relationship between physical dimensions
    and stitch/row counts.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    stitches_per_cm: float = Field(
        ..., gt=0, description="Number of stitches per centimeter"
    )
    rows_per_cm: float = Field(..., gt=0, description="Number of rows per centimeter")
    hook_size_mm: Optional[float] = Field(
        default=None, gt=0, description="Recommended crochet hook size in millimeters"
    )
    yarn_weight: Optional[Literal["lace", "fingering", "sport", "DK", "worsted", "bulky", "super_bulky"]] = Field(
        default=None, description="Recommended yarn weight category"
    )
    swatch_notes: Optional[str] = Field(
        default=None, description="Additional gauge swatch notes"
    )


class ShapeParameters(BaseModel):
    """
    Parameters defining the shape dimensions.

    Different shapes require different parameters:
    - Sphere: diameter_cm
    - Cylinder: diameter_cm, height_cm
    - Cone: base_diameter_cm, top_diameter_cm, height_cm
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True, extra="allow")

    shape_type: Literal["sphere", "cylinder", "cone"] = Field(
        ..., description="Type of 3D shape"
    )
    # Common parameters
    diameter_cm: Optional[float] = Field(
        default=None, gt=0, description="Diameter in centimeters (sphere, cylinder)"
    )
    height_cm: Optional[float] = Field(
        default=None, gt=0, description="Height in centimeters (cylinder, cone)"
    )
    # Cone-specific parameters
    base_diameter_cm: Optional[float] = Field(
        default=None, gt=0, description="Base diameter in centimeters (cone)"
    )
    top_diameter_cm: Optional[float] = Field(
        default=None, gt=0, description="Top diameter in centimeters (cone)"
    )


class PatternMetadata(BaseModel):
    """
    Metadata about the pattern generation.

    Includes information about generation time, version, and other
    non-instruction data.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    generated_at: datetime = Field(
        default_factory=datetime.now, description="Pattern generation timestamp"
    )
    engine_version: str = Field(
        default="0.1.0", description="Pattern engine version used"
    )
    total_rounds: int = Field(..., ge=0, description="Total number of rounds")
    estimated_time_minutes: Optional[int] = Field(
        default=None, ge=0, description="Estimated completion time in minutes"
    )
    difficulty: Optional[Literal["beginner", "intermediate", "advanced"]] = Field(
        default=None, description="Pattern difficulty level"
    )
    tags: List[str] = Field(
        default_factory=list, description="Searchable tags for the pattern"
    )


class PatternDSL(BaseModel):
    """
    Complete pattern representation in the Knit-Wit DSL.

    This is the top-level model that contains all information needed
    to render and execute a crochet pattern.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    shape: ShapeParameters = Field(..., description="Shape parameters")
    gauge: GaugeInfo = Field(..., description="Gauge information")
    rounds: List[RoundInstruction] = Field(
        ..., description="Round-by-round instructions"
    )
    metadata: PatternMetadata = Field(..., description="Pattern metadata")
    notes: Optional[str] = Field(
        default=None, description="General notes and instructions"
    )

    @field_validator("rounds")
    @classmethod
    def validate_rounds_sequential(
        cls, v: List[RoundInstruction]
    ) -> List[RoundInstruction]:
        """Ensure round numbers are sequential starting from 0."""
        if not v:
            raise ValueError("Pattern must have at least one round")

        for idx, round_inst in enumerate(v):
            if round_inst.round_number != idx:
                raise ValueError(
                    f"Round numbers must be sequential. Expected {idx}, got {round_inst.round_number}"
                )
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert pattern to dictionary for JSON serialization."""
        return self.model_dump(mode="json")

    def to_json(self) -> str:
        """Convert pattern to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternDSL":
        """Create pattern from dictionary."""
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str) -> "PatternDSL":
        """Create pattern from JSON string."""
        return cls.model_validate_json(json_str)


# =============================================================================
# Parsing DSL Models (Simplified format for text pattern parsing)
# =============================================================================


class OpDSL(BaseModel):
    """
    Simplified operation model for text pattern parsing.

    Represents a single operation or sequence of operations within a round.
    Used by the pattern parser for bracket/repeat grammar.

    Examples:
        - {"op": "sc", "count": 6} - 6 single crochet stitches
        - {"op": "inc", "count": 1} - 1 increase
        - {"op": "seq", "ops": [...], "repeat": 6} - sequence repeated 6 times
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    op: str = Field(
        ...,
        description="Operation type (sc, inc, dec, MR, seq, etc.)",
        examples=["sc", "inc", "dec", "MR", "seq"]
    )
    count: int = Field(
        default=1,
        ge=0,
        description="Number of stitches produced by this operation (0 for MR)"
    )
    ops: Optional[List["OpDSL"]] = Field(
        default=None,
        description="Child operations for sequence operations (op='seq')"
    )
    repeat: Optional[int] = Field(
        default=None,
        ge=1,
        description="Number of times to repeat sequence (for op='seq')"
    )


class RoundDSL(BaseModel):
    """
    Simplified round model for text pattern parsing.

    Represents a single round with its operations and expected stitch count.
    Used by the pattern parser for bracket/repeat grammar.

    Examples:
        - Round 1: MR 6 sc (6)
          {"r": 1, "ops": [{"op": "MR", "count": 1}, {"op": "sc", "count": 6}], "stitches": 6}
        - Round 3: [2 sc, inc] x6 (18)
          {"r": 3, "ops": [{"op": "seq", "ops": [...], "repeat": 6, "count": 18}], "stitches": 18}
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    r: int = Field(
        ...,
        ge=1,
        description="Round number (1-indexed)"
    )
    ops: List[OpDSL] = Field(
        ...,
        description="List of operations for this round"
    )
    stitches: int = Field(
        ...,
        ge=1,
        description="Expected total stitch count after completing this round"
    )


class MetaDSL(BaseModel):
    """
    Metadata for parsed patterns.

    Contains information about pattern terminology, stitch types, and gauge.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    version: str = Field(
        default="0.1",
        description="DSL version"
    )
    units: Literal["cm", "in"] = Field(
        default="cm",
        description="Unit system (metric or imperial)"
    )
    terms: Literal["US", "UK"] = Field(
        default="US",
        description="Terminology (US or UK crochet terms)"
    )
    stitch: str = Field(
        default="sc",
        description="Primary stitch type"
    )
    round_mode: Literal["spiral", "joined"] = Field(
        default="spiral",
        description="Round construction mode"
    )
    gauge: Optional[Dict[str, float]] = Field(
        default=None,
        description="Gauge information (sts_per_10cm, rows_per_10cm)"
    )


class ObjectDSL(BaseModel):
    """
    Object/shape definition for parsed patterns.

    Describes the geometric shape being crocheted.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True, extra="allow")

    type: str = Field(
        ...,
        description="Shape type (sphere, cylinder, cone, unknown, etc.)"
    )
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Shape-specific parameters (diameter, height, etc.)"
    )


class PatternParseDSL(BaseModel):
    """
    Complete parsed pattern representation.

    This is a simplified DSL format specifically designed for text pattern parsing.
    It uses bracket/repeat grammar and is more lightweight than PatternDSL.

    Example:
        ```json
        {
          "meta": {
            "version": "0.1",
            "terms": "US",
            "stitch": "sc"
          },
          "object": {
            "type": "unknown",
            "params": {}
          },
          "rounds": [
            {
              "r": 1,
              "ops": [{"op": "MR", "count": 1}, {"op": "sc", "count": 6}],
              "stitches": 6
            }
          ],
          "materials": {
            "hook_size_mm": 4.0,
            "yardage_estimate": 25
          },
          "notes": []
        }
        ```
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    meta: MetaDSL = Field(
        ...,
        description="Pattern metadata"
    )
    object: ObjectDSL = Field(
        ...,
        description="Shape/object definition",
        alias="object"
    )
    rounds: List[RoundDSL] = Field(
        ...,
        description="List of rounds with operations"
    )
    materials: Dict[str, Any] = Field(
        default_factory=dict,
        description="Materials information (hook size, yardage, etc.)"
    )
    notes: List[str] = Field(
        default_factory=list,
        description="Pattern notes and instructions"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert pattern to dictionary for JSON serialization."""
        return self.model_dump(mode="json", by_alias=True)

    def to_json(self) -> str:
        """Convert pattern to JSON string."""
        return self.model_dump_json(indent=2, by_alias=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternParseDSL":
        """Create pattern from dictionary."""
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str) -> "PatternParseDSL":
        """Create pattern from JSON string."""
        return cls.model_validate_json(json_str)


# Enable forward references for recursive OpDSL model
OpDSL.model_rebuild()
