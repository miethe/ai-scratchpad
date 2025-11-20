"""
Visualization API Endpoint for Knit-Wit

Converts PatternDSL to visualization frames for interactive round-by-round rendering.
Supports both 2D (circular layout) and 3D (isometric projection) visualization modes.
"""

from typing import Literal
from fastapi import APIRouter, HTTPException, Query, status
from app.models.visualization import VisualizationResponse
from app.models.frontend_dsl import FrontendPatternDSL
from app.services.visualization_service import VisualizationService
from app.utils.dsl_converter import frontend_dsl_to_pattern_dsl

router = APIRouter(prefix="/visualization", tags=["visualization"])
visualization_service = VisualizationService()


@router.post("/frames", response_model=VisualizationResponse, status_code=status.HTTP_200_OK)
async def generate_visualization_frames(
    pattern: FrontendPatternDSL,
    mode: Literal["2d", "3d"] = Query(
        default="2d",
        description="Visualization mode: '2d' for circular layout, '3d' for isometric projection",
    ),
) -> VisualizationResponse:
    """
    Convert PatternDSL to visualization frames.

    **Performance:**
    - 2D mode: < 100ms for typical patterns (< 50 rounds)
    - 3D mode: < 150ms for typical patterns (50% overhead for depth sorting)

    **Query Parameters:**
    - `mode`: Visualization mode ("2d" or "3d", default: "2d")
      - "2d": Circular layout with polar coordinates
      - "3d": Shape-aware 3D coordinates with isometric projection metadata

    **Request Body:** Frontend PatternDSL object (JSON) - matches format returned by /patterns/generate

    **Example Request (2D mode):**
    ```
    POST /api/v1/visualization/frames?mode=2d
    ```

    **Example Request (3D mode):**
    ```
    POST /api/v1/visualization/frames?mode=3d
    ```

    **Example Response (2D mode):**
    ```json
    {
      "frames": [
        {
          "round_number": 1,
          "nodes": [
            {"id": "r0s0", "stitch_type": "sc", "position": [100.0, 0.0], "highlight": "normal"}
          ],
          "edges": [{"source": "r0s0", "target": "r0s1"}],
          "stitch_count": 6,
          "highlights": []
        }
      ],
      "total_rounds": 2,
      "shape_type": "sphere"
    }
    ```

    **Example Response (3D mode):**
    ```json
    {
      "frames": [
        {
          "round_number": 1,
          "nodes": [
            {
              "id": "r0s0",
              "stitch_type": "sc",
              "position": [100.0, 0.0],
              "position_3d": [100.0, 0.0, 50.0],
              "depth_order": 10,
              "depth_factor": 0.75,
              "highlight": "normal"
            }
          ],
          "edges": [{"source": "r0s0", "target": "r0s1"}],
          "stitch_count": 6,
          "highlights": [],
          "projection": {
            "type": "isometric",
            "angle_deg": 30.0,
            "bounds_3d": {
              "x_min": -100.0, "x_max": 100.0,
              "y_min": -100.0, "y_max": 100.0,
              "z_min": -100.0, "z_max": 100.0
            }
          }
        }
      ],
      "total_rounds": 2,
      "shape_type": "sphere"
    }
    ```

    **Error Responses:**
    - 422: Invalid PatternDSL structure
    - 500: Visualization generation failed

    Args:
        pattern: Frontend PatternDSL object from request body
        mode: Visualization mode ("2d" or "3d")

    Returns:
        VisualizationResponse: Frame-by-frame visualization data

    Raises:
        HTTPException: 422 for validation errors, 500 for server errors
    """
    try:
        # Convert frontend DSL format to pattern engine format
        pattern_dsl = frontend_dsl_to_pattern_dsl(pattern)

        # Generate visualization frames based on mode
        if mode == "3d":
            response = visualization_service.pattern_to_visualization_3d(pattern_dsl)
        else:
            response = visualization_service.pattern_to_visualization(pattern_dsl)

        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid pattern DSL: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Visualization generation failed: {str(e)}",
        )
