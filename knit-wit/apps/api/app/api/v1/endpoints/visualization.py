"""
Visualization API Endpoint for Knit-Wit

Converts PatternDSL to visualization frames for interactive round-by-round rendering.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.visualization import VisualizationResponse
from app.services.visualization_service import VisualizationService
import sys
from pathlib import Path

# Add pattern engine to Python path
pattern_engine_path = Path(__file__).resolve().parents[6] / "packages" / "pattern-engine"
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import PatternDSL

router = APIRouter(prefix="/visualization", tags=["visualization"])
visualization_service = VisualizationService()


@router.post("/frames", response_model=VisualizationResponse, status_code=status.HTTP_200_OK)
async def generate_visualization_frames(pattern: PatternDSL) -> VisualizationResponse:
    """
    Convert PatternDSL to visualization frames.

    **Performance:** < 100ms for typical patterns (< 50 rounds)

    **Request Body:** PatternDSL object (JSON)
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
      "shape": {"shape_type": "sphere", "params": {"diameter": 10}},
      "rounds": [
        {"round_number": 0, "total_stitches": 6, "stitches": [{"stitch_type": "sc", "count": 6}]},
        {"round_number": 1, "total_stitches": 12, "stitches": [{"stitch_type": "inc", "count": 6}]}
      ]
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
        pattern: PatternDSL object from request body

    Returns:
        VisualizationResponse: Frame-by-frame visualization data

    Raises:
        HTTPException: 422 for validation errors, 500 for server errors
    """
    try:
        response = visualization_service.pattern_to_visualization(pattern)
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
