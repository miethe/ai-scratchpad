"""
DSL Conversion Utilities

Converts between frontend DSL format and pattern engine DSL format.
"""

from datetime import datetime
from typing import Optional
import sys
from pathlib import Path

# Add pattern engine to Python path
pattern_engine_path = Path(__file__).resolve().parents[5] / "packages" / "pattern-engine"
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import (
    PatternDSL,
    PatternMetadata,
    ShapeParameters,
    GaugeInfo,
    RoundInstruction,
    StitchInstruction,
)

from app.models.frontend_dsl import FrontendPatternDSL


def frontend_dsl_to_pattern_dsl(frontend_dsl: FrontendPatternDSL) -> PatternDSL:
    """
    Convert frontend DSL format to pattern engine PatternDSL format.

    The frontend uses a simplified DSL structure (meta, object, rounds, materials, notes)
    while the pattern engine uses a more structured format (shape, gauge, rounds, metadata, notes).

    Args:
        frontend_dsl: Frontend pattern format

    Returns:
        PatternDSL: Pattern engine format

    Example:
        >>> frontend = FrontendPatternDSL(...)
        >>> pattern = frontend_dsl_to_pattern_dsl(frontend)
        >>> pattern.shape.shape_type
        'sphere'
    """
    # Convert shape parameters
    # Map frontend params (diameter, height) to shape-specific fields (diameter_cm, height_cm)
    shape_params_dict = {
        "shape_type": frontend_dsl.object.type,
    }

    # Map params to correct field names
    for key, value in frontend_dsl.object.params.items():
        if key == "diameter":
            shape_params_dict["diameter_cm"] = value
        elif key == "height":
            shape_params_dict["height_cm"] = value
        elif key == "base_diameter":
            shape_params_dict["base_diameter_cm"] = value
        elif key == "top_diameter":
            shape_params_dict["top_diameter_cm"] = value
        else:
            # Pass through any other params with _cm suffix if not already present
            if not key.endswith("_cm"):
                shape_params_dict[f"{key}_cm"] = value
            else:
                shape_params_dict[key] = value

    shape_params = ShapeParameters(**shape_params_dict)

    # Convert gauge info
    gauge = GaugeInfo(
        stitches_per_cm=frontend_dsl.meta.gauge.sts_per_10cm / 10.0,
        rows_per_cm=frontend_dsl.meta.gauge.rows_per_10cm / 10.0,
        hook_size_mm=frontend_dsl.materials.hook_size_mm,
        yarn_weight=_normalize_yarn_weight(frontend_dsl.materials.yarn_weight),
    )

    # Convert rounds
    rounds = []
    for frontend_round in frontend_dsl.rounds:
        stitches = []
        for op in frontend_round.ops:
            # Convert each operation to stitch instruction
            # Handle repeat by expanding into individual stitches
            count = op.count
            if op.repeat:
                # For sequences with repeats, multiply the count
                count = op.count * op.repeat

            stitch = StitchInstruction(
                stitch_type=op.op,
                count=count,
            )
            stitches.append(stitch)

        round_inst = RoundInstruction(
            round_number=frontend_round.r,
            stitches=stitches,
            total_stitches=frontend_round.stitches,
        )
        rounds.append(round_inst)

    # Create metadata
    metadata = PatternMetadata(
        generated_at=datetime.now(),
        engine_version="0.1.0",
        total_rounds=len(rounds),
        difficulty=_infer_difficulty(len(rounds)),
        tags=[frontend_dsl.object.type, frontend_dsl.meta.terms],
    )

    # Combine notes into single string
    notes_str = "\n".join(frontend_dsl.notes) if frontend_dsl.notes else None

    return PatternDSL(
        shape=shape_params,
        gauge=gauge,
        rounds=rounds,
        metadata=metadata,
        notes=notes_str,
    )


def _normalize_yarn_weight(yarn_weight: str) -> Optional[str]:
    """
    Normalize yarn weight to match GaugeInfo enum.

    Args:
        yarn_weight: Yarn weight string (case-insensitive)

    Returns:
        Normalized yarn weight or None if invalid
    """
    valid_weights = {
        "lace",
        "fingering",
        "sport",
        "DK",
        "worsted",
        "bulky",
        "super_bulky",
    }

    # Try exact match first
    if yarn_weight in valid_weights:
        return yarn_weight

    # Try case-insensitive match
    normalized = yarn_weight.lower()
    for weight in valid_weights:
        if weight.lower() == normalized:
            return weight

    # Default to worsted if unknown
    return "worsted"


def _infer_difficulty(total_rounds: int) -> str:
    """
    Infer pattern difficulty based on round count.

    Args:
        total_rounds: Number of rounds in pattern

    Returns:
        Difficulty level: "beginner", "intermediate", or "advanced"
    """
    if total_rounds <= 10:
        return "beginner"
    elif total_rounds <= 30:
        return "intermediate"
    else:
        return "advanced"
