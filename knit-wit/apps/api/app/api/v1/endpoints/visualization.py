"""
Visualization API Endpoint for Knit-Wit

Converts PatternDSL to visualization frames for interactive round-by-round rendering.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.visualization import VisualizationResponse
from app.models.frontend_dsl import FrontendPatternDSL
from app.services.visualization_service import VisualizationService
from app.utils.dsl_converter import frontend_dsl_to_pattern_dsl

router = APIRouter(prefix="/visualization", tags=["visualization"])
visualization_service = VisualizationService()


@router.post("/frames", response_model=VisualizationResponse, status_code=status.HTTP_200_OK)
async def generate_visualization_frames(pattern: FrontendPatternDSL) -> VisualizationResponse:
    """
    Convert PatternDSL to visualization frames.

    **Performance:** < 100ms for typical patterns (< 50 rounds)

    **Request Body:** Frontend PatternDSL object (JSON) - matches format returned by /patterns/generate
    **Response:** VisualizationResponse with frames array

    **Example Request:**
    ```json
    {
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
        {"r": 0, "ops": [{"op": "sc", "count": 6}], "stitches": 6},
        {"r": 1, "ops": [{"op": "inc", "count": 6}], "stitches": 12}
      ],
      "materials": {
        "yarn_weight": "worsted",
        "hook_size_mm": 4.0,
        "yardage_estimate": 25
      },
      "notes": ["Work in a spiral; use a stitch marker."]
    }
    ```

    **Example Response:**
    ```json
    {
      "frames": [
        {
          "round_number": 1,
          "nodes": [
            {"id": "r0s0", "stitch_type": "sc", "position": [100.0, 0.0], "highlight": "normal"}
          ],
          "edges": [
            {"source": "r0s0", "target": "r0s1"}
          ],
          "stitch_count": 6,
          "highlights": []
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

    Returns:
        VisualizationResponse: Frame-by-frame visualization data

    Raises:
        HTTPException: 422 for validation errors, 500 for server errors
    """
    try:
        # Convert frontend DSL format to pattern engine format
        pattern_dsl = frontend_dsl_to_pattern_dsl(pattern)

        # Generate visualization frames
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
