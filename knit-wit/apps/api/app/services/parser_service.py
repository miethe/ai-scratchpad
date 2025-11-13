"""
Pattern Parser Service for Knit-Wit API

Parses limited crochet pattern text syntax to PatternParseDSL.
Supports canonical bracket/repeat grammar: R3: [2 sc, inc] x6 (18)
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add pattern engine to Python path
pattern_engine_path = Path(__file__).resolve().parents[5] / "packages" / "pattern-engine"
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import (
    PatternParseDSL,
    RoundDSL,
    OpDSL,
    MetaDSL,
    ObjectDSL,
)


class ParserError(Exception):
    """Exception raised for pattern parsing errors."""

    def __init__(self, message: str, line_number: int = None):
        """
        Initialize parser error.

        Args:
            message: Error description
            line_number: Line number where error occurred (1-indexed)
        """
        self.message = message
        self.line_number = line_number
        super().__init__(
            f"Line {line_number}: {message}" if line_number else message
        )


class PatternParserService:
    """
    Parse limited crochet pattern syntax to PatternParseDSL.

    **Supported Syntax:**
    - Round notation: R1: operations (stitch_count)
    - Magic ring: MR or MR 6 sc
    - Simple stitches: sc, inc, dec, hdc, dc, slst, ch
    - Repetition: op x count (e.g., "inc x6")
    - Bracket sequences: [ops] xN (e.g., "[2 sc, inc] x6")

    **Examples:**
    - R1: MR 6 sc (6)
    - R2: inc x6 (12)
    - R3: [2 sc, inc] x6 (18)
    - R4: [3 sc, inc] x6 (24)

    **Unsupported (MVP):**
    - Nested brackets: [[sc, inc] x2, dec] x3
    - Complex colorwork: "sc with Color A"
    - Stitch modifiers: "sc in back loop only"
    - Joined rounds (spiral only)
    """

    # Regex patterns
    ROUND_PATTERN = r"^R(\d+):\s*(.+?)\s*\((\d+)\)\s*$"
    BRACKET_PATTERN = r"\[([^\]]+)\]\s*x\s*(\d+)"

    # Supported stitch types
    SUPPORTED_STITCHES = {
        "MR",
        "sc",
        "inc",
        "dec",
        "hdc",
        "dc",
        "slst",
        "ch",
    }

    # Stitch count multipliers (stitches produced per operation)
    STITCH_MULTIPLIERS = {
        "MR": 0,   # Magic ring doesn't produce stitches
        "sc": 1,   # Single crochet produces 1 stitch
        "hdc": 1,  # Half double crochet produces 1 stitch
        "dc": 1,   # Double crochet produces 1 stitch
        "inc": 2,  # Increase (2 sc in same stitch) produces 2 stitches
        "dec": 1,  # Decrease (sc2tog) produces 1 stitch
        "slst": 1, # Slip stitch produces 1 stitch
        "ch": 1,   # Chain produces 1 stitch
    }

    def parse(self, text: str) -> PatternParseDSL:
        """
        Parse pattern text to PatternParseDSL.

        Args:
            text: Pattern text with canonical bracket/repeat syntax

        Returns:
            PatternParseDSL: Parsed pattern

        Raises:
            ParserError: If parsing fails or syntax is unsupported
        """
        if not text or not text.strip():
            raise ParserError("Empty pattern text")

        lines = text.strip().split("\n")
        rounds: List[RoundDSL] = []

        for line_idx, line in enumerate(lines, start=1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            try:
                round_dsl = self._parse_round(line, line_idx)
                rounds.append(round_dsl)
            except ParserError:
                raise
            except Exception as e:
                raise ParserError(
                    f"Failed to parse round: {str(e)}", line_idx
                )

        if not rounds:
            raise ParserError("No valid rounds found in pattern")

        # Build PatternParseDSL
        return PatternParseDSL(
            meta=MetaDSL(
                version="0.1",
                units="cm",
                terms="US",
                stitch="sc",
                round_mode="spiral",
                gauge={"sts_per_10cm": 14, "rows_per_10cm": 16},
            ),
            object=ObjectDSL(type="unknown", params={}),
            rounds=rounds,
            materials={},
            notes=[],
        )

    def _parse_round(self, line: str, line_number: int) -> RoundDSL:
        """
        Parse a single round line.

        Args:
            line: Round text (e.g., "R3: [2 sc, inc] x6 (18)")
            line_number: Line number for error reporting

        Returns:
            RoundDSL: Parsed round

        Raises:
            ParserError: If round syntax is invalid
        """
        round_match = re.match(self.ROUND_PATTERN, line)
        if not round_match:
            raise ParserError(
                f"Invalid round format. Expected: R#: operations (count)",
                line_number,
            )

        round_num = int(round_match.group(1))
        ops_text = round_match.group(2).strip()
        expected_stitches = int(round_match.group(3))

        if expected_stitches < 1:
            raise ParserError(
                f"Invalid stitch count: {expected_stitches}. Must be >= 1",
                line_number,
            )

        # Parse operations
        try:
            ops = self._parse_operations(ops_text, line_number)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(
                f"Failed to parse operations: {str(e)}", line_number
            )

        # Create RoundDSL
        return RoundDSL(r=round_num, ops=ops, stitches=expected_stitches)

    def _parse_operations(self, ops_text: str, line_number: int) -> List[OpDSL]:
        """
        Parse operations from round text.

        Handles brackets first: [2 sc, inc] x6
        Then parses remaining simple operations.

        Args:
            ops_text: Operations text (e.g., "[2 sc, inc] x6")
            line_number: Line number for error reporting

        Returns:
            List[OpDSL]: Parsed operations

        Raises:
            ParserError: If operation syntax is invalid
        """
        ops: List[OpDSL] = []

        # Handle brackets first: [2 sc, inc] x6
        bracket_matches = list(re.finditer(self.BRACKET_PATTERN, ops_text))
        for match in bracket_matches:
            inner_ops_text = match.group(1).strip()
            repeat = int(match.group(2))

            if repeat < 1:
                raise ParserError(
                    f"Invalid repeat count: {repeat}. Must be >= 1",
                    line_number,
                )

            # Parse inner operations
            inner_ops = self._parse_simple_ops(inner_ops_text, line_number)

            # Calculate total stitch count for sequence
            total_count = sum(op.count for op in inner_ops) * repeat

            # Create sequence operation
            ops.append(
                OpDSL(op="seq", ops=inner_ops, repeat=repeat, count=total_count)
            )

            # Remove from text to avoid re-parsing
            ops_text = ops_text.replace(match.group(0), "", 1)

        # Parse remaining simple operations
        simple_ops = self._parse_simple_ops(ops_text, line_number)
        ops.extend(simple_ops)

        if not ops:
            raise ParserError(
                "No operations found in round", line_number
            )

        return ops

    def _parse_simple_ops(
        self, text: str, line_number: int
    ) -> List[OpDSL]:
        """
        Parse simple operations (no brackets).

        Supports:
        - "MR" or "MR 6 sc" - Magic ring
        - "inc x6" - Stitch with count
        - "2 sc" - Count and stitch
        - "sc" - Simple stitch

        Args:
            text: Operations text without brackets
            line_number: Line number for error reporting

        Returns:
            List[OpDSL]: Parsed simple operations

        Raises:
            ParserError: If operation syntax is invalid or unsupported
        """
        ops: List[OpDSL] = []
        text = text.strip()

        if not text:
            return ops

        # Special handling for MR followed by other operations
        # "MR 6 sc" should be split into "MR" and "6 sc"
        # Note: MR doesn't contribute to stitch count (count=0)
        if text.upper().startswith("MR "):
            ops.append(OpDSL(op="MR", count=0))
            # Continue parsing the rest
            text = text[2:].strip()

        # Split by commas
        tokens = [t.strip() for t in text.split(",") if t.strip()]

        for token in tokens:
            token = token.strip()
            if not token:
                continue

            try:
                op = self._parse_single_op(token, line_number)
                if op:
                    ops.append(op)
            except ParserError:
                raise
            except Exception as e:
                raise ParserError(
                    f"Invalid operation '{token}': {str(e)}", line_number
                )

        return ops

    def _parse_single_op(self, token: str, line_number: int) -> OpDSL:
        """
        Parse a single operation token.

        Args:
            token: Single operation (e.g., "inc x6", "2 sc", "MR")
            line_number: Line number for error reporting

        Returns:
            OpDSL: Parsed operation

        Raises:
            ParserError: If operation syntax is invalid or unsupported
        """
        token = token.strip()

        # Handle "x" syntax: "inc x6"
        if " x" in token or " x " in token:
            parts = re.split(r"\s*x\s*", token)
            if len(parts) != 2:
                raise ParserError(
                    f"Invalid repetition syntax: '{token}'", line_number
                )
            stitch = parts[0].strip()
            count = int(parts[1].strip())

            if count < 1:
                raise ParserError(
                    f"Invalid count: {count}. Must be >= 1", line_number
                )

            if stitch not in self.SUPPORTED_STITCHES:
                raise ParserError(
                    f"Unsupported stitch type: '{stitch}'. "
                    f"Supported: {', '.join(sorted(self.SUPPORTED_STITCHES))}",
                    line_number,
                )

            return OpDSL(op=stitch, count=count)

        # Handle "MR" (magic ring)
        # Note: MR itself doesn't contribute to stitch count
        if token.upper() == "MR":
            return OpDSL(op="MR", count=0)

        # Handle "2 sc" (count before stitch)
        count_match = re.match(r"^(\d+)\s+(\w+)$", token)
        if count_match:
            count = int(count_match.group(1))
            stitch = count_match.group(2)

            if count < 1:
                raise ParserError(
                    f"Invalid count: {count}. Must be >= 1", line_number
                )

            if stitch not in self.SUPPORTED_STITCHES:
                raise ParserError(
                    f"Unsupported stitch type: '{stitch}'. "
                    f"Supported: {', '.join(sorted(self.SUPPORTED_STITCHES))}",
                    line_number,
                )

            return OpDSL(op=stitch, count=count)

        # Handle simple stitch: "sc", "inc", etc.
        if token in self.SUPPORTED_STITCHES:
            return OpDSL(op=token, count=1)

        # Check if it's an unsupported stitch
        if token.isalpha():
            raise ParserError(
                f"Unsupported stitch type: '{token}'. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_STITCHES))}",
                line_number,
            )

        raise ParserError(
            f"Invalid operation syntax: '{token}'", line_number
        )

    def validate_parse(self, dsl: PatternParseDSL) -> Dict[str, Any]:
        """
        Validate parsed DSL.

        Checks:
        - Stitch count consistency (computed vs. declared)
        - Round numbering (sequential, starting from 1)
        - Operation validity

        Args:
            dsl: Parsed pattern DSL

        Returns:
            Dict with validation results:
            {
                "valid": bool,
                "errors": List[str],
                "warnings": List[str]
            }
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not dsl.rounds:
            errors.append("Pattern has no rounds")
            return {"valid": False, "errors": errors, "warnings": warnings}

        # Check round numbering
        prev_round = 0
        for round_dsl in dsl.rounds:
            if round_dsl.r != prev_round + 1:
                warnings.append(
                    f"Non-sequential round numbers: R{prev_round} → R{round_dsl.r}"
                )
            prev_round = round_dsl.r

        # Check stitch count consistency
        for round_dsl in dsl.rounds:
            computed = self._compute_stitch_count(round_dsl.ops)
            if computed != round_dsl.stitches:
                errors.append(
                    f"R{round_dsl.r}: Stitch count mismatch. "
                    f"Expected {round_dsl.stitches}, computed {computed}"
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def _compute_stitch_count(self, ops: List[OpDSL]) -> int:
        """
        Compute total stitch count from operations.

        Takes into account that different stitch types produce different
        numbers of stitches (e.g., inc produces 2 stitches).

        Args:
            ops: List of operations

        Returns:
            Total stitch count
        """
        total = 0
        for op in ops:
            if op.op == "seq":
                # Sequence: sum inner ops * repeat
                if op.ops and op.repeat:
                    inner_count = self._compute_stitch_count(op.ops)
                    total += inner_count * op.repeat
            else:
                # Simple operation
                # Get multiplier for this stitch type (default to 1 if unknown)
                multiplier = self.STITCH_MULTIPLIERS.get(op.op, 1)
                total += op.count * multiplier
        return total
