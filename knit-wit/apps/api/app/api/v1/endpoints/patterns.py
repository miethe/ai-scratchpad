"""
Pattern Generation API Endpoint for Knit-Wit

Generates parametric crochet patterns for 3D shapes (sphere, cylinder, cone).
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
import sys
import os

# Add pattern engine to path (monorepo structure)
pattern_engine_path = os.path.join(
    os.path.dirname(__file__), "../../../../../packages/pattern-engine"
)
sys.path.insert(0, pattern_engine_path)

from knit_wit_engine.shapes.sphere import SphereCompiler
from knit_wit_engine.shapes.cylinder import CylinderCompiler
from knit_wit_engine.shapes.cone import ConeCompiler
from knit_wit_engine.models.requests import Gauge


router = APIRouter(prefix="/patterns", tags=["patterns"])


class PatternRequest(BaseModel):
    """Request model for pattern generation."""

    shape: Literal["sphere", "cylinder", "cone"] = Field(
        ...,
        description="Shape type to generate"
    )
    diameter: Optional[float] = Field(
        None,
        gt=0,
        description="Diameter in specified units (required for sphere and cylinder)"
    )
    height: Optional[float] = Field(
        None,
        gt=0,
        description="Height in specified units (required for cylinder and cone)"
    )
    units: Literal["cm", "in"] = Field(
        ...,
        description="Unit of measurement for dimensions"
    )
    gauge: Dict[str, float] = Field(
        ...,
        description="Gauge specification with sts_per_10cm and rows_per_10cm"
    )
    stitch: Literal["sc", "inc", "dec", "slst", "ch"] = Field(
        ...,
        description="Primary stitch type"
    )
    terms: Literal["US", "UK"] = Field(
        ...,
        description="Crochet terminology (US or UK)"
    )


class PatternResponse(BaseModel):
    """Response model for pattern generation."""

    dsl: Dict[str, Any] = Field(
        ...,
        description="Generated pattern in DSL format"
    )


def _convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between cm and inches."""
    if from_unit == to_unit:
        return value
    if from_unit == "in" and to_unit == "cm":
        return value * 2.54
    if from_unit == "cm" and to_unit == "in":
        return value / 2.54
    return value


def _convert_pattern_to_frontend_dsl(
    pattern_dsl,
    shape: str,
    diameter: Optional[float],
    height: Optional[float],
    units: str,
    gauge_input: Dict[str, float],
    stitch: str,
    terms: str
) -> Dict[str, Any]:
    """
    Convert pattern engine DSL to frontend-expected format.

    The pattern engine uses a different DSL structure than what the frontend expects,
    so we need to map between them.
    """
    # Build shape params based on shape type
    shape_params = {}
    if shape == "sphere" and diameter:
        shape_params["diameter"] = diameter
    elif shape == "cylinder" and diameter and height:
        shape_params["diameter"] = diameter
        shape_params["height"] = height
    elif shape == "cone" and height:
        if diameter:
            shape_params["top_diameter"] = diameter
        shape_params["height"] = height

    # Convert rounds to frontend format
    rounds = []
    for round_instr in pattern_dsl.rounds:
        ops = []
        for stitch_instr in round_instr.stitches:
            ops.append({
                "op": stitch_instr.stitch_type,
                "count": stitch_instr.count
            })

        rounds.append({
            "r": round_instr.round_number,
            "ops": ops,
            "stitches": round_instr.total_stitches
        })

    # Estimate hook size and yardage from gauge
    # Standard hook size for worsted: 4.0mm, adjust for gauge
    base_hook_mm = 4.0
    gauge_ratio = gauge_input["sts_per_10cm"] / 14.0  # 14 sts/10cm is standard worsted
    hook_size_mm = base_hook_mm / (gauge_ratio ** 0.5) if gauge_ratio > 0 else 4.0

    # Estimate yardage (simplified - actual calculation in pattern engine)
    total_stitches = sum(r["stitches"] for r in rounds)
    yardage_estimate = int(total_stitches * 0.4)  # Rough estimate: 0.4 yards per stitch

    return {
        "meta": {
            "version": "0.1",
            "units": units,
            "terms": terms,
            "stitch": stitch,
            "round_mode": "spiral",
            "gauge": gauge_input
        },
        "object": {
            "type": shape,
            "params": shape_params
        },
        "rounds": rounds,
        "materials": {
            "yarn_weight": pattern_dsl.gauge.yarn_weight or "worsted",
            "hook_size_mm": round(hook_size_mm, 1),
            "yardage_estimate": yardage_estimate
        },
        "notes": [
            "Work in a spiral; use a stitch marker to track rounds.",
            "Stuff firmly before closing if creating a 3D object."
        ]
    }


@router.post(
    "/generate",
    response_model=PatternResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate parametric crochet pattern",
    description="""
    Generate a parametric crochet pattern for a 3D geometric shape.

    **Supported Shapes:**
    - **sphere**: Requires `diameter`
    - **cylinder**: Requires `diameter` and `height`
    - **cone**: Requires `height` (optionally `diameter` for top)

    **Gauge Format:**
    ```json
    {
      "sts_per_10cm": 14.0,
      "rows_per_10cm": 16.0
    }
    ```

    **Example Request:**
    ```json
    {
      "shape": "sphere",
      "diameter": 10,
      "units": "cm",
      "gauge": {"sts_per_10cm": 14, "rows_per_10cm": 16},
      "stitch": "sc",
      "terms": "US"
    }
    ```

    **Response Time:** < 300ms for typical patterns
    """,
    responses={
        201: {
            "description": "Pattern generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "dsl": {
                            "meta": {
                                "version": "0.1",
                                "units": "cm",
                                "terms": "US",
                                "stitch": "sc",
                                "round_mode": "spiral",
                                "gauge": {"sts_per_10cm": 14, "rows_per_10cm": 16}
                            },
                            "object": {"type": "sphere", "params": {"diameter": 10}},
                            "rounds": [
                                {"r": 0, "ops": [{"op": "MR", "count": 6}], "stitches": 6},
                                {"r": 1, "ops": [{"op": "inc", "count": 6}], "stitches": 12}
                            ],
                            "materials": {
                                "yarn_weight": "worsted",
                                "hook_size_mm": 4.0,
                                "yardage_estimate": 25
                            },
                            "notes": ["Work in a spiral; use a stitch marker."]
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid parameters or missing required fields",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sphere requires diameter parameter"
                    }
                }
            }
        },
        422: {
            "description": "Validation error (malformed request body)"
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def generate_pattern(request: PatternRequest) -> PatternResponse:
    """
    Generate a parametric crochet pattern for a geometric shape.

    Validates input parameters, calls the appropriate shape compiler,
    and returns the pattern in DSL format.

    Args:
        request: PatternRequest with shape parameters and gauge

    Returns:
        PatternResponse: Generated pattern DSL

    Raises:
        HTTPException: 400 for invalid parameters, 500 for server errors
    """
    try:
        # Convert units to cm for pattern engine (it expects cm)
        diameter_cm = None
        height_cm = None

        if request.diameter:
            diameter_cm = _convert_units(request.diameter, request.units, "cm")
        if request.height:
            height_cm = _convert_units(request.height, request.units, "cm")

        # Validate shape-specific requirements
        if request.shape == "sphere":
            if not diameter_cm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sphere requires diameter parameter"
                )
        elif request.shape == "cylinder":
            if not diameter_cm or not height_cm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cylinder requires both diameter and height parameters"
                )
        elif request.shape == "cone":
            if not height_cm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cone requires height parameter"
                )

        # Create gauge object
        gauge = Gauge(
            sts_per_10cm=request.gauge["sts_per_10cm"],
            rows_per_10cm=request.gauge["rows_per_10cm"]
        )

        # Generate pattern based on shape
        if request.shape == "sphere":
            compiler = SphereCompiler()
            pattern_dsl = compiler.generate(diameter_cm, gauge)
        elif request.shape == "cylinder":
            compiler = CylinderCompiler()
            pattern_dsl = compiler.generate(diameter_cm, height_cm, gauge, has_caps=True)
        elif request.shape == "cone":
            compiler = ConeCompiler()
            # For cone: taper from larger base to smaller top
            # Default: base is provided diameter (or 8cm), top is 3cm
            base_diameter_cm = diameter_cm if diameter_cm else 8.0
            top_diameter_cm = 3.0  # Fixed small top for MVP
            pattern_dsl = compiler.generate(base_diameter_cm, top_diameter_cm, height_cm, gauge)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported shape: {request.shape}"
            )

        # Convert pattern engine DSL to frontend format
        frontend_dsl = _convert_pattern_to_frontend_dsl(
            pattern_dsl,
            request.shape,
            request.diameter,
            request.height,
            request.units,
            request.gauge,
            request.stitch,
            request.terms
        )

        return PatternResponse(dsl=frontend_dsl)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise

    except Exception as e:
        # Log unexpected errors and return 500
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pattern generation failed: {str(e)}"
        )
