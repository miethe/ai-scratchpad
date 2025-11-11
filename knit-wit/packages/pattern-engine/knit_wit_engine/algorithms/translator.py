"""
US ↔ UK Crochet Terminology Translator

Provides functions to translate stitch terminology between US and UK crochet conventions.
MVP scope includes only basic stitches: sc, inc, dec, ch, slst, MR.
"""

from typing import Dict, Literal
from knit_wit_engine.models.dsl import PatternDSL

# Convention type alias for clarity
Convention = Literal["US", "UK"]

# US → UK mappings (for MVP stitches only)
US_TO_UK: Dict[str, str] = {
    "sc": "dc",  # single crochet → double crochet
    "inc": "inc",  # increase (same term)
    "dec": "dec",  # decrease (same term)
    "ch": "ch",  # chain (same term)
    "slst": "ss",  # slip stitch → slip stitch (ss)
    "MR": "MR",  # magic ring (same term)
}

# UK → US reverse mapping
UK_TO_US: Dict[str, str] = {v: k for k, v in US_TO_UK.items()}


def translate_term(
    term: str, from_convention: Convention, to_convention: Convention
) -> str:
    """
    Translate a single crochet term between US and UK conventions.

    Args:
        term: The stitch term to translate (e.g., 'sc', 'dc', 'inc')
        from_convention: Source convention ('US' or 'UK')
        to_convention: Target convention ('US' or 'UK')

    Returns:
        Translated term in the target convention

    Raises:
        ValueError: If term is unknown in source convention or conventions are invalid

    Examples:
        >>> translate_term('sc', 'US', 'UK')
        'dc'
        >>> translate_term('dc', 'UK', 'US')
        'sc'
        >>> translate_term('inc', 'US', 'UK')
        'inc'
        >>> translate_term('sc', 'US', 'US')
        'sc'

    Notes:
        - Same convention returns unchanged term (no-op)
        - Only MVP stitches are supported (sc, inc, dec, ch, slst, MR)
        - HDC/DC translations deferred to v1.1
    """
    # No translation needed if conventions match
    if from_convention == to_convention:
        return term

    # Validate convention values
    if from_convention not in ("US", "UK"):
        raise ValueError(
            f"Invalid source convention: {from_convention}. Must be 'US' or 'UK'"
        )
    if to_convention not in ("US", "UK"):
        raise ValueError(
            f"Invalid target convention: {to_convention}. Must be 'US' or 'UK'"
        )

    # Translate US → UK
    if from_convention == "US" and to_convention == "UK":
        if term not in US_TO_UK:
            raise ValueError(
                f"Unknown US term: '{term}'. "
                f"Supported terms: {', '.join(sorted(US_TO_UK.keys()))}"
            )
        return US_TO_UK[term]

    # Translate UK → US
    if from_convention == "UK" and to_convention == "US":
        if term not in UK_TO_US:
            raise ValueError(
                f"Unknown UK term: '{term}'. "
                f"Supported terms: {', '.join(sorted(UK_TO_US.keys()))}"
            )
        return UK_TO_US[term]

    # This should be unreachable due to earlier validation
    raise ValueError(
        f"Invalid convention combination: {from_convention} → {to_convention}"
    )


def translate_pattern_dsl(
    dsl: PatternDSL, from_convention: Convention, to_convention: Convention
) -> PatternDSL:
    """
    Translate all stitch terms in a PatternDSL to target convention.

    Creates a deep copy of the input DSL and translates all stitch_type fields
    in every round to the target convention.

    Args:
        dsl: PatternDSL object to translate
        from_convention: Source convention of the pattern ('US' or 'UK')
        to_convention: Target convention for translation ('US' or 'UK')

    Returns:
        New PatternDSL instance with all terms translated to target convention

    Raises:
        ValueError: If any stitch term cannot be translated or conventions are invalid

    Examples:
        >>> # Translate US sphere pattern to UK
        >>> uk_pattern = translate_pattern_dsl(us_pattern, 'US', 'UK')
        >>> # All 'sc' stitches become 'dc' in UK convention

    Notes:
        - Original DSL is not modified (uses deep copy)
        - All rounds and stitches are translated
        - Metadata and other fields remain unchanged
        - No-op if from_convention == to_convention (still returns deep copy)
    """
    # Validate conventions
    if from_convention not in ("US", "UK"):
        raise ValueError(
            f"Invalid source convention: {from_convention}. Must be 'US' or 'UK'"
        )
    if to_convention not in ("US", "UK"):
        raise ValueError(
            f"Invalid target convention: {to_convention}. Must be 'US' or 'UK'"
        )

    # Create deep copy to avoid mutating original
    translated_dsl = dsl.model_copy(deep=True)

    # No translation needed if conventions match
    if from_convention == to_convention:
        return translated_dsl

    # Translate all stitch types in all rounds
    for round_inst in translated_dsl.rounds:
        for stitch in round_inst.stitches:
            try:
                stitch.stitch_type = translate_term(
                    stitch.stitch_type, from_convention, to_convention
                )
            except ValueError as e:
                # Re-raise with context about which round failed
                raise ValueError(
                    f"Translation failed in round {round_inst.round_number}: {e}"
                ) from e

    return translated_dsl
