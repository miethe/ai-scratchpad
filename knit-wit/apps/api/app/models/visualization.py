"""
Visualization Data Models for Knit-Wit

Pydantic v2 models for converting PatternDSL to frame-by-frame visualization primitives.
These models represent the circular layout of stitches for interactive round-by-round rendering.
"""

from typing import List, Literal, Tuple
from pydantic import BaseModel, Field, ConfigDict


class RenderNode(BaseModel):
    """
    Single stitch node in visualization.

    Represents one stitch positioned in 2D space using polar coordinates
    converted to Cartesian (x, y) coordinates for SVG rendering.

    Examples:
        - Regular stitch: {"id": "r1s0", "stitch_type": "sc", "position": (100, 0), "highlight": "normal"}
        - Increase: {"id": "r2s5", "stitch_type": "inc", "position": (50, 86.6), "highlight": "increase"}
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    id: str = Field(
        ...,
        description="Unique node identifier in format 'r{round}s{stitch}' (e.g., 'r3s12')",
        pattern=r"^r\d+s\d+$",
        examples=["r1s0", "r2s5", "r10s42"],
    )
    stitch_type: str = Field(
        ...,
        description="Type of stitch operation (sc, inc, dec, etc.)",
        examples=["sc", "inc", "dec", "hdc", "dc"],
    )
    position: Tuple[float, float] = Field(
        ...,
        description="Cartesian (x, y) coordinates in arbitrary units (frontend scales to viewport)",
        examples=[(100.0, 0.0), (50.0, 86.6), (-50.0, 86.6)],
    )
    highlight: Literal["normal", "increase", "decrease"] = Field(
        ..., description="Highlighting mode for visual emphasis of increases/decreases"
    )


class RenderEdge(BaseModel):
    """
    Connection between consecutive stitches.

    Edges form the circular outline of each round by connecting adjacent nodes.
    A closing edge connects the last stitch back to the first to complete the circle.

    Examples:
        - Consecutive: {"source": "r1s0", "target": "r1s1"}
        - Closing: {"source": "r1s5", "target": "r1s0"}
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    source: str = Field(
        ..., description="Source node ID", pattern=r"^r\d+s\d+$", examples=["r1s0", "r2s5"]
    )
    target: str = Field(
        ..., description="Target node ID", pattern=r"^r\d+s\d+$", examples=["r1s1", "r2s6"]
    )


class VisualizationFrame(BaseModel):
    """
    Single round visualization frame.

    Contains all rendering primitives for one round: positioned nodes,
    connecting edges, and highlight information.

    Example:
        Round 1 (magic ring with 6 sc):
        {
            "round_number": 1,
            "nodes": [6 nodes positioned in circle],
            "edges": [6 edges forming closed loop],
            "stitch_count": 6,
            "highlights": []
        }
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    round_number: int = Field(
        ..., ge=1, description="Round number (1-indexed, matching pattern instructions)"
    )
    nodes: List[RenderNode] = Field(
        ..., description="All stitch nodes in this round, ordered sequentially"
    )
    edges: List[RenderEdge] = Field(
        ..., description="Connections between consecutive nodes, including closing edge"
    )
    stitch_count: int = Field(..., ge=0, description="Total number of stitches in this round")
    highlights: List[str] = Field(
        default_factory=list, description="Node IDs with highlighting (increases/decreases)"
    )


class VisualizationResponse(BaseModel):
    """
    Complete visualization data for a pattern.

    Contains all frames (one per round) ready for frontend rendering.
    Frontend can implement step-by-step visualization by iterating through frames.

    Example:
        {
            "frames": [frame1, frame2, ...],
            "total_rounds": 10,
            "shape_type": "sphere"
        }
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    frames: List[VisualizationFrame] = Field(..., description="Round-by-round visualization frames")
    total_rounds: int = Field(..., ge=1, description="Total number of rounds in pattern")
    shape_type: str = Field(
        ...,
        description="Shape type of the pattern (sphere, cylinder, cone)",
        examples=["sphere", "cylinder", "cone"],
    )
