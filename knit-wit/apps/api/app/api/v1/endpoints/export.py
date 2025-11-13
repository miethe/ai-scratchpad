"""
Export API Endpoints for Knit-Wit

Provides PDF and JSON export functionality for crochet patterns.
Implements C3 (PDF Export) and C5 (JSON DSL Export) from Phase 3.
"""

from typing import Literal
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add pattern engine to Python path
pattern_engine_path = Path(__file__).resolve().parents[7] / "packages" / "pattern-engine"
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import PatternDSL
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])
export_service = ExportService()


@router.post("/pdf", status_code=status.HTTP_200_OK)
async def export_pdf(
    pattern: PatternDSL,
    paper_size: Literal["A4", "letter"] = "A4",
) -> Response:
    """
    Export pattern as PDF document.

    Generates a professional PDF with cover page, materials list, and
    round-by-round instructions. Includes proper formatting and styling.

    **Performance:** < 5 seconds generation time, < 5 MB file size

    **Request Body:** PatternDSL object (JSON)
    **Query Parameters:**
        - paper_size: "A4" or "letter" (default: "A4")

    **Response:** PDF file (application/pdf)

    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/export/pdf?paper_size=A4" \\
         -H "Content-Type: application/json" \\
         -d '{
           "shape": {"shape_type": "sphere", "diameter_cm": 10},
           "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6, "hook_size_mm": 4.0},
           "rounds": [...],
           "metadata": {...}
         }' \\
         --output pattern.pdf
    ```

    **Success Response (200 OK):**
    - Content-Type: application/pdf
    - Content-Disposition: attachment; filename="pattern_{timestamp}.pdf"
    - Body: PDF binary data

    **Error Responses:**
    - 400: Invalid paper size parameter
    - 422: Invalid PatternDSL structure
    - 500: PDF generation failed

    Args:
        pattern: PatternDSL object from request body
        paper_size: Paper format ("A4" or "letter")

    Returns:
        Response: PDF file with appropriate headers

    Raises:
        HTTPException: 400/422/500 for various errors
    """
    try:
        # Generate PDF
        pdf_bytes = export_service.generate_pdf(pattern, paper_size=paper_size)

        # Generate filename with timestamp
        timestamp = pattern.metadata.generated_at.strftime("%Y%m%d_%H%M%S")
        shape_type = pattern.shape.shape_type
        filename = f"pattern_{shape_type}_{timestamp}.pdf"

        # Return PDF with appropriate headers
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-cache",
            },
        )

    except ValueError as e:
        # Invalid paper size or validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        # PDF generation failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}",
        )


@router.post("/json", status_code=status.HTTP_200_OK)
async def export_json(pattern: PatternDSL) -> JSONResponse:
    """
    Export pattern as JSON DSL.

    Converts PatternDSL to formatted JSON string that is round-trip
    compatible with PatternDSL.from_json(). Useful for saving patterns
    or transferring between systems.

    **Request Body:** PatternDSL object (JSON)
    **Response:** JSON string (application/json)

    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/export/json" \\
         -H "Content-Type: application/json" \\
         -d '{
           "shape": {"shape_type": "sphere", "diameter_cm": 10},
           "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6},
           "rounds": [...],
           "metadata": {...}
         }'
    ```

    **Success Response (200 OK):**
    ```json
    {
      "json": "{\\n  \\"shape\\": {...},\\n  \\"gauge\\": {...},\\n  ...\\n}",
      "size_bytes": 1234
    }
    ```

    **Error Responses:**
    - 422: Invalid PatternDSL structure
    - 500: JSON export failed

    Args:
        pattern: PatternDSL object from request body

    Returns:
        JSONResponse: Response with JSON string and metadata

    Raises:
        HTTPException: 422/500 for validation or export errors
    """
    try:
        # Generate JSON
        json_str = export_service.generate_json(pattern)

        # Return JSON with metadata
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "json": json_str,
                "size_bytes": len(json_str.encode("utf-8")),
            },
            headers={
                "Cache-Control": "no-cache",
            },
        )

    except ValueError as e:
        # Validation error
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid PatternDSL: {str(e)}",
        )
    except Exception as e:
        # JSON export failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JSON export failed: {str(e)}",
        )
