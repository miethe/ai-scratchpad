"""
Pattern Parser API Endpoint for Knit-Wit

Converts text patterns with canonical bracket/repeat grammar to PatternParseDSL.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from app.services.parser_service import PatternParserService, ParserError


router = APIRouter(prefix="/parser", tags=["parser"])
parser_service = PatternParserService()


class ParseRequest(BaseModel):
    """Request model for pattern parsing."""

    text: str = Field(
        ...,
        description="Pattern text with canonical bracket/repeat syntax",
        examples=[
            "R1: MR 6 sc (6)\nR2: inc x6 (12)\nR3: [2 sc, inc] x6 (18)"
        ],
    )


class ValidationResult(BaseModel):
    """Validation result for parsed pattern."""

    valid: bool = Field(
        ...,
        description="Whether the parsed pattern is valid"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="List of validation errors"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="List of validation warnings"
    )


class ParseResponse(BaseModel):
    """Response model for pattern parsing."""

    dsl: Dict[str, Any] = Field(
        ...,
        description="Parsed PatternParseDSL as dictionary"
    )
    validation: ValidationResult = Field(
        ...,
        description="Validation results"
    )


@router.post(
    "/parse",
    response_model=ParseResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse text pattern to DSL",
    description="""
    Parse crochet pattern text to PatternParseDSL.

    **Supported Syntax:**
    - Round notation: `R1: operations (stitch_count)`
    - Magic ring: `MR` or `MR 6 sc`
    - Simple stitches: `sc`, `inc`, `dec`, `hdc`, `dc`, `slst`, `ch`
    - Repetition: `op x count` (e.g., `inc x6`)
    - Bracket sequences: `[ops] xN` (e.g., `[2 sc, inc] x6`)

    **Examples:**
    ```
    R1: MR 6 sc (6)
    R2: inc x6 (12)
    R3: [2 sc, inc] x6 (18)
    R4: [3 sc, inc] x6 (24)
    ```

    **Unsupported (MVP):**
    - Nested brackets
    - Complex colorwork
    - Stitch modifiers (e.g., "in back loop only")
    - Joined rounds (spiral only)

    **Response Time:** < 200ms for typical patterns
    """,
    responses={
        200: {
            "description": "Pattern parsed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "dsl": {
                            "meta": {
                                "version": "0.1",
                                "terms": "US",
                                "stitch": "sc"
                            },
                            "object": {"type": "unknown", "params": {}},
                            "rounds": [
                                {
                                    "r": 1,
                                    "ops": [
                                        {"op": "MR", "count": 1},
                                        {"op": "sc", "count": 6}
                                    ],
                                    "stitches": 6
                                }
                            ],
                            "materials": {},
                            "notes": []
                        },
                        "validation": {
                            "valid": True,
                            "errors": [],
                            "warnings": []
                        }
                    }
                }
            }
        },
        400: {
            "description": "Parse error (invalid syntax or unsupported features)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Line 3: Unsupported stitch type: 'dc'. Supported: ch, dec, hdc, inc, MR, sc, slst"
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
async def parse_pattern(request: ParseRequest) -> ParseResponse:
    """
    Parse crochet pattern text to PatternParseDSL.

    Converts text patterns using canonical bracket/repeat grammar to structured DSL format.
    Includes validation of stitch counts and round numbering.

    Args:
        request: ParseRequest with pattern text

    Returns:
        ParseResponse: Parsed DSL and validation results

    Raises:
        HTTPException: 400 for parse errors, 500 for server errors
    """
    try:
        # Parse text to DSL
        dsl = parser_service.parse(request.text)

        # Validate parsed DSL
        validation_result = parser_service.validate_parse(dsl)

        # Convert to response format
        return ParseResponse(
            dsl=dsl.to_dict(),
            validation=ValidationResult(**validation_result)
        )

    except ParserError as e:
        # User-facing parse errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        # Unexpected server errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pattern parsing failed: {str(e)}"
        )
