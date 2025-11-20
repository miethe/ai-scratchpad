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
    # Foundation stitches that don't count toward total_stitches
    foundation_stitches = {"MR", "mr", "Ch", "ch"}

    rounds = []
    for frontend_round in frontend_dsl.rounds:
        stitches = []
        total_count = 0  # Track actual stitch count for validation

        for op in frontend_round.ops:
            # Convert each operation to stitch instruction
            # The count field represents the number of OPERATIONS, not stitches produced
            # Different operations produce different numbers of stitches:
            #   - sc: 1 operation = 1 stitch
            #   - inc: 1 operation = 2 stitches (2 sc in same stitch)
            #   - dec: 1 operation = 1 stitch (sc2tog: consumes 2, produces 1)
            #   - MR: foundation stitch (counts as 0)
            # The repeat field (if present) multiplies the operation count
            # Examples:
            #   - {"op": "sc", "count": 6} → 6 sc operations → 6 stitches
            #   - {"op": "inc", "count": 6} → 6 inc operations → 12 stitches
            #   - {"op": "sc", "count": 2, "repeat": 6} → 12 sc operations → 12 stitches

            # Calculate number of operations
            if op.repeat and op.repeat > 0:
                # Operation with repeat: multiply count by repeat
                num_operations = op.count * op.repeat
            else:
                # Simple operation: use count as-is
                num_operations = op.count

            # Create stitch instruction with the operation count
            # (The pattern engine expects count to be number of operations, not stitches)
            stitch = StitchInstruction(
                stitch_type=op.op,
                count=num_operations,
            )
            stitches.append(stitch)

            # Calculate stitches produced for validation
            # Add to total count only if not a foundation stitch
            if op.op not in foundation_stitches:
                # Calculate stitches based on operation type
                if op.op.lower() == "inc":
                    # Increase: 1 operation produces 2 stitches
                    stitches_produced = num_operations * 2
                elif op.op.lower() == "dec":
                    # Decrease: 1 operation produces 1 stitch (consumes 2)
                    stitches_produced = num_operations * 1
                else:
                    # Regular stitches (sc, hdc, dc, etc.): 1 operation = 1 stitch
                    stitches_produced = num_operations

                total_count += stitches_produced

        # Validate that our conversion matches the expected total
        if total_count != frontend_round.stitches:
            ops_debug = [f"{op.op}(count={op.count}, repeat={op.repeat})" for op in frontend_round.ops]
            raise ValueError(
                f"DSL conversion error in round {frontend_round.r}: "
                f"Converted stitch count ({total_count}) does not match "
                f"expected total ({frontend_round.stitches}). "
                f"Operations: {ops_debug}"
            )

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
