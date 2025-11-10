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
