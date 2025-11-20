"""
Visualization Data Models for Knit-Wit

Pydantic v2 models for converting PatternDSL to frame-by-frame visualization primitives.
These models represent the circular layout of stitches for interactive round-by-round rendering.
Supports both 2D (circular layout) and 3D (isometric projection) visualization modes.
"""

from typing import List, Literal, Tuple, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class RenderNode(BaseModel):
    """
    Single stitch node in visualization.

    Represents one stitch positioned in 2D space using polar coordinates
    converted to Cartesian (x, y) coordinates for SVG rendering.
    Optionally includes 3D coordinates and depth ordering for isometric projection.

    Examples:
        - Regular stitch (2D): {"id": "r1s0", "stitch_type": "sc", "position": (100, 0), "highlight": "normal"}
        - Increase (2D): {"id": "r2s5", "stitch_type": "inc", "position": (50, 86.6), "highlight": "increase"}
        - 3D mode: {"id": "r1s0", "position": (100, 0), "position_3d": (100, 0, 50), "depth_order": 10, ...}
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

    # 3D visualization fields (optional, only present when mode=3d)
    position_3d: Optional[Tuple[float, float, float]] = Field(
        default=None,
        description="3D Cartesian coordinates (x, y, z) for isometric projection",
        examples=[(100.0, 0.0, 50.0), (50.0, 86.6, 25.0)],
    )
    depth_order: Optional[int] = Field(
        default=None,
        ge=0,
        description="Depth sorting index for painter's algorithm (0=back, higher=front)",
    )
    depth_factor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Normalized depth factor (0=far, 1=near) for size/opacity scaling",
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


class ProjectionMetadata(BaseModel):
    """
    Metadata for 3D projection rendering.

    Provides information needed by frontend to render 3D coordinates using
    isometric projection. Includes projection type, angle, and 3D bounding box
    for normalization and viewport scaling.
    """

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    type: Literal["isometric", "dimetric", "perspective"] = Field(
        default="isometric",
        description="Projection type for 3D rendering",
    )
    angle_deg: float = Field(
        default=30.0,
        ge=0.0,
        le=90.0,
        description="Projection angle in degrees (30° for isometric, 35.26° for dimetric)",
    )
    bounds_3d: Dict[str, float] = Field(
        ...,
        description="3D bounding box for normalization: {x_min, x_max, y_min, y_max, z_min, z_max}",
        examples=[
            {
                "x_min": -100.0,
                "x_max": 100.0,
                "y_min": -100.0,
                "y_max": 100.0,
                "z_min": -50.0,
                "z_max": 50.0,
            }
        ],
    )


class VisualizationFrame(BaseModel):
    """
    Single round visualization frame.

    Contains all rendering primitives for one round: positioned nodes,
    connecting edges, and highlight information.
    Optionally includes projection metadata for 3D rendering.

    Example (2D):
        Round 1 (magic ring with 6 sc):
        {
            "round_number": 1,
            "nodes": [6 nodes positioned in circle],
            "edges": [6 edges forming closed loop],
            "stitch_count": 6,
            "highlights": []
        }

    Example (3D):
        {
            "round_number": 1,
            "nodes": [nodes with position_3d, depth_order],
            "edges": [...],
            "stitch_count": 6,
            "highlights": [],
            "projection": {
                "type": "isometric",
                "angle_deg": 30.0,
                "bounds_3d": {...}
            }
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

    # 3D visualization metadata (optional, only present when mode=3d)
    projection: Optional[ProjectionMetadata] = Field(
        default=None,
        description="3D projection metadata (isometric angle, bounding box) - only present in 3D mode",
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
