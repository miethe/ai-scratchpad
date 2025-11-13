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


@router.post("/svg", status_code=status.HTTP_200_OK)
async def export_svg(
    pattern: PatternDSL,
    mode: Literal["per-round", "composite"] = "composite",
) -> Response:
    """
    Export pattern as SVG diagram(s).

    Generates vector graphics showing circular stitch layout with color-coded
    increases/decreases. Supports two export modes:
    - per-round: Individual SVG files (one per round) as ZIP archive
    - composite: Single SVG with all rounds stacked vertically

    **Performance:** < 1 second generation time, < 1 MB per round

    **Request Body:** PatternDSL object (JSON)
    **Query Parameters:**
        - mode: "per-round" or "composite" (default: "composite")

    **Response:** SVG file (image/svg+xml) or ZIP archive (application/zip)

    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/export/svg?mode=composite" \\
         -H "Content-Type: application/json" \\
         -d '{
           "shape": {"shape_type": "sphere", "diameter_cm": 10},
           "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6},
           "rounds": [...],
           "metadata": {...}
         }' \\
         --output pattern.svg
    ```

    **Success Response (200 OK):**
    - Content-Type: image/svg+xml (composite) or application/zip (per-round)
    - Content-Disposition: attachment; filename="pattern_{timestamp}.svg"
    - Body: SVG XML or ZIP archive

    **Error Responses:**
    - 400: Invalid mode parameter
    - 422: Invalid PatternDSL structure
    - 500: SVG generation failed

    Args:
        pattern: PatternDSL object from request body
        mode: Export mode ("per-round" or "composite")

    Returns:
        Response: SVG file or ZIP archive with appropriate headers

    Raises:
        HTTPException: 400/422/500 for various errors
    """
    try:
        # Generate SVG(s)
        svg_result = export_service.generate_svg(pattern, mode=mode)

        # Generate filename with timestamp
        timestamp = pattern.metadata.generated_at.strftime("%Y%m%d_%H%M%S")
        shape_type = pattern.shape.shape_type

        if mode == "per-round":
            # Create ZIP archive with individual SVG files
            import zipfile
            import io as io_module

            zip_buffer = io_module.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, svg_str in enumerate(svg_result):
                    filename = f"round_{idx + 1}.svg"
                    zip_file.writestr(filename, svg_str)

            zip_bytes = zip_buffer.getvalue()
            zip_buffer.close()

            return Response(
                content=zip_bytes,
                media_type="application/zip",
                headers={
                    "Content-Disposition": f'attachment; filename="pattern_{shape_type}_{timestamp}_rounds.zip"',
                    "Cache-Control": "no-cache",
                },
            )
        else:
            # Return single SVG
            filename = f"pattern_{shape_type}_{timestamp}.svg"

            return Response(
                content=svg_result,
                media_type="image/svg+xml",
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"',
                    "Cache-Control": "no-cache",
                },
            )

    except ValueError as e:
        # Invalid mode or validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        # SVG generation failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SVG generation failed: {str(e)}",
        )


@router.post("/png", status_code=status.HTTP_200_OK)
async def export_png(
    pattern: PatternDSL,
    dpi: int = 72,
) -> Response:
    """
    Export pattern as PNG rasterized image.

    Generates high-quality PNG from SVG visualization with specified DPI:
    - 72 DPI: Screen display (smaller file size)
    - 300 DPI: Print quality (larger file size)

    **Performance:** < 2 seconds generation time, < 5 MB file size

    **Request Body:** PatternDSL object (JSON)
    **Query Parameters:**
        - dpi: 72 or 300 (default: 72)

    **Response:** PNG file (image/png)

    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/export/png?dpi=300" \\
         -H "Content-Type: application/json" \\
         -d '{
           "shape": {"shape_type": "sphere", "diameter_cm": 10},
           "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6},
           "rounds": [...],
           "metadata": {...}
         }' \\
         --output pattern.png
    ```

    **Success Response (200 OK):**
    - Content-Type: image/png
    - Content-Disposition: attachment; filename="pattern_{timestamp}.png"
    - Body: PNG binary data

    **Error Responses:**
    - 400: Invalid DPI parameter
    - 422: Invalid PatternDSL structure
    - 500: PNG generation failed

    Args:
        pattern: PatternDSL object from request body
        dpi: Dots per inch (72 for screen, 300 for print)

    Returns:
        Response: PNG file with appropriate headers

    Raises:
        HTTPException: 400/422/500 for various errors
    """
    try:
        # Validate DPI
        if dpi not in [72, 300]:
            raise ValueError(f"Invalid DPI: {dpi}. Must be 72 or 300")

        # Generate composite SVG first
        svg_str = export_service.generate_svg(pattern, mode="composite")

        # Convert to PNG
        png_bytes = export_service.generate_png(svg_str, dpi=dpi)

        # Generate filename with timestamp
        timestamp = pattern.metadata.generated_at.strftime("%Y%m%d_%H%M%S")
        shape_type = pattern.shape.shape_type
        filename = f"pattern_{shape_type}_{timestamp}_{dpi}dpi.png"

        # Return PNG with appropriate headers
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-cache",
            },
        )

    except ValueError as e:
        # Invalid DPI or validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        # PNG generation failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PNG generation failed: {str(e)}",
        )
