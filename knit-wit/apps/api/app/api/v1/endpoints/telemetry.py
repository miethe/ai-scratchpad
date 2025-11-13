"""
Telemetry API Endpoint for Knit-Wit

Anonymous event logging for product analytics.
NO PII collected - privacy-respecting telemetry only.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.services.telemetry_service import telemetry_service, TelemetryError


router = APIRouter(prefix="/telemetry", tags=["telemetry"])


class TelemetryEventRequest(BaseModel):
    """Request model for telemetry event tracking."""

    event: str = Field(
        ...,
        description="Event name (pattern_generated, pattern_visualized, pattern_exported)",
        examples=["pattern_generated"],
    )
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Event properties (will be scrubbed for PII)",
        examples=[
            {
                "shape_type": "sphere",
                "stitch_type": "sc",
                "terms": "US",
            }
        ],
    )


@router.post(
    "/events",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Track anonymous telemetry event",
    description="""
    Track anonymous telemetry events for product analytics.

    **Privacy Guarantee:**
    - NO personally identifiable information (PII) is logged
    - NO pattern content, dimensions, or user-specific data
    - NO IP addresses, user agents, or session identifiers
    - All properties are validated and scrubbed before logging

    **Supported Events:**
    - `pattern_generated`: Pattern compilation completed
    - `pattern_visualized`: Visualization rendered
    - `pattern_exported`: Pattern exported to PDF/JSON/SVG

    **Allowed Properties by Event:**

    **pattern_generated:**
    - `shape_type`: Shape type (e.g., "sphere", "cylinder")
    - `stitch_type`: Stitch type (e.g., "sc", "dc")
    - `terms`: Terminology (e.g., "US", "UK")
    - `units`: Units (e.g., "cm", "in")
    - `round_mode`: Round mode (e.g., "spiral", "joined")

    **pattern_visualized:**
    - `shape_type`: Shape type
    - `highlight_changes`: Whether changes are highlighted
    - `terms`: Terminology

    **pattern_exported:**
    - `export_format`: Export format (e.g., "pdf", "json", "svg")
    - `include_diagram`: Whether diagram is included
    - `paper_size`: Paper size (e.g., "A4", "Letter")
    - `terms`: Terminology

    **Silent Failures:**
    This endpoint returns 204 No Content even if logging fails internally.
    Telemetry errors never block user experience.

    **Response Time:** < 50ms (async logging)
    """,
    responses={
        204: {
            "description": "Event logged successfully (or silently failed)"
        },
        400: {
            "description": "Invalid event type",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid event type: 'invalid_event'. Supported: pattern_exported, pattern_generated, pattern_visualized"
                    }
                }
            },
        },
        422: {
            "description": "Validation error (malformed request body)"
        },
    },
)
async def track_event(request: TelemetryEventRequest) -> None:
    """
    Track anonymous telemetry event.

    Validates event type and scrubs properties for PII before logging.
    Returns 204 No Content for all cases (silent success/failure).

    Args:
        request: TelemetryEventRequest with event name and properties

    Raises:
        HTTPException: 400 for invalid event types

    Note:
        This endpoint returns 204 even if internal logging fails.
        Telemetry must never block the user experience.
    """
    try:
        # Track event (validates and scrubs properties)
        telemetry_service.track_event(
            event=request.event,
            properties=request.properties,
        )

        # Return 204 No Content (silent success)
        return None

    except TelemetryError as e:
        # Invalid event type - return 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception:
        # All other errors: silent failure (return 204)
        # Telemetry errors must never block user experience
        return None
