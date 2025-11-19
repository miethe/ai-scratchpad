"""
Frontend DSL Models for Knit-Wit API

Pydantic models matching the frontend TypeScript types for PatternDSL.
This is the format returned by /patterns/generate and consumed by the visualization endpoint.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class GaugeParams(BaseModel):
    """Gauge parameters matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    sts_per_10cm: float = Field(..., description="Stitches per 10cm")
    rows_per_10cm: float = Field(..., description="Rows per 10cm")


class MetaDSL(BaseModel):
    """Pattern metadata matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    version: str = Field(default="0.1", description="DSL version")
    units: Literal["cm", "in"] = Field(..., description="Unit system")
    terms: Literal["US", "UK"] = Field(..., description="Crochet terminology")
    stitch: str = Field(..., description="Primary stitch type")
    round_mode: Literal["spiral", "joined"] = Field(
        default="spiral", description="Round construction mode"
    )
    gauge: GaugeParams = Field(..., description="Gauge information")


class ObjectDSL(BaseModel):
    """Shape/object definition matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True, extra="allow")

    type: str = Field(..., description="Shape type (sphere, cylinder, cone)")
    params: Dict[str, float] = Field(
        default_factory=dict, description="Shape-specific parameters"
    )


class PatternOperation(BaseModel):
    """Single operation within a round matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    op: str = Field(..., description="Operation type (sc, inc, dec, etc.)")
    count: int = Field(..., ge=0, description="Number of stitches")
    repeat: Optional[int] = Field(default=None, description="Repeat count for sequences")


class PatternRound(BaseModel):
    """Round instruction matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    r: int = Field(..., ge=0, description="Round number (0-indexed)")
    ops: List[PatternOperation] = Field(..., description="List of operations")
    stitches: int = Field(..., ge=0, description="Total stitch count")


class MaterialsDSL(BaseModel):
    """Materials information matching frontend format."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    yarn_weight: str = Field(default="worsted", description="Yarn weight category")
    hook_size_mm: float = Field(..., gt=0, description="Hook size in mm")
    yardage_estimate: int = Field(..., ge=0, description="Estimated yardage")


class FrontendPatternDSL(BaseModel):
    """
    Complete pattern representation matching frontend TypeScript types.

    This is the format returned by /patterns/generate and expected by
    visualization and export endpoints.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    meta: MetaDSL = Field(..., description="Pattern metadata")
    object: ObjectDSL = Field(..., description="Shape definition")
    rounds: List[PatternRound] = Field(..., description="Round-by-round instructions")
    materials: MaterialsDSL = Field(..., description="Materials information")
    notes: List[str] = Field(default_factory=list, description="Pattern notes")
