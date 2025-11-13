"""
Unit tests for ExportService

Comprehensive test coverage for PDF and JSON export functionality:
- PDF generation with cover, materials, and pattern sections
- JSON export with round-trip compatibility
- Error handling for invalid inputs
- Performance validation (< 5s, < 5MB)
- Edge cases (minimal patterns, large patterns)
"""

import io
import json
import pytest
from datetime import datetime
from PyPDF2 import PdfReader

# Import from knit_wit_engine package
import sys
from pathlib import Path

pattern_engine_path = (
    Path(__file__).parent.parent.parent.parent.parent / "packages" / "pattern-engine"
)
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import (
    PatternDSL,
    RoundInstruction,
    StitchInstruction,
    ShapeParameters,
    GaugeInfo,
    PatternMetadata,
)

from app.services.export_service import ExportService


class TestExportService:
    """Test suite for ExportService."""

    @pytest.fixture
    def service(self) -> ExportService:
        """Create ExportService instance."""
        return ExportService()

    @pytest.fixture
    def sample_gauge(self) -> GaugeInfo:
        """Create sample gauge info."""
        return GaugeInfo(
            stitches_per_cm=1.4,
            rows_per_cm=1.6,
            hook_size_mm=4.0,
            yarn_weight="worsted",
        )

    @pytest.fixture
    def sample_shape(self) -> ShapeParameters:
        """Create sample shape parameters."""
        return ShapeParameters(shape_type="sphere", diameter_cm=10.0)

    @pytest.fixture
    def sample_metadata(self) -> PatternMetadata:
        """Create sample pattern metadata."""
        return PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=3,
            difficulty="beginner",
        )

    @pytest.fixture
    def simple_pattern(
        self, sample_gauge: GaugeInfo, sample_shape: ShapeParameters, sample_metadata: PatternMetadata
    ) -> PatternDSL:
        """Create simple 3-round sphere pattern."""
        rounds = [
            RoundInstruction(
                round_number=0,
                stitches=[StitchInstruction(stitch_type="sc", count=6)],
                total_stitches=6,
                description="Magic ring",
            ),
            RoundInstruction(
                round_number=1,
                stitches=[StitchInstruction(stitch_type="inc", count=6)],
                total_stitches=12,
                description="Increase round",
            ),
            RoundInstruction(
                round_number=2,
                stitches=[
                    StitchInstruction(stitch_type="sc", count=1),
                    StitchInstruction(stitch_type="inc", count=1),
                ],
                total_stitches=18,
                description="[sc, inc] x6",
            ),
        ]

        return PatternDSL(
            shape=sample_shape,
            gauge=sample_gauge,
            rounds=rounds,
            metadata=sample_metadata,
            notes="Work in a spiral. Use a stitch marker.",
        )

    @pytest.fixture
    def complex_pattern(
        self, sample_gauge: GaugeInfo, sample_metadata: PatternMetadata
    ) -> PatternDSL:
        """Create more complex cone pattern."""
        shape = ShapeParameters(
            shape_type="cone",
            base_diameter_cm=15.0,
            top_diameter_cm=8.0,
            height_cm=20.0,
        )

        # Create 10 rounds for a more substantial pattern
        rounds = []
        for i in range(10):
            stitch_count = 24 + (i * 2)  # Increasing stitch count
            rounds.append(
                RoundInstruction(
                    round_number=i,
                    stitches=[StitchInstruction(stitch_type="sc", count=stitch_count)],
                    total_stitches=stitch_count,
                    description=f"Round {i + 1}",
                )
            )

        metadata = PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=10,
            difficulty="intermediate",
            estimated_time_minutes=120,
        )

        return PatternDSL(
            shape=shape,
            gauge=sample_gauge,
            rounds=rounds,
            metadata=metadata,
            notes="Cone shape. Work in spiral.",
        )

    # =============================================================================
    # JSON Export Tests
    # =============================================================================

    def test_json_export_simple(self, service: ExportService, simple_pattern: PatternDSL) -> None:
        """Test JSON export of simple pattern."""
        json_str = service.generate_json(simple_pattern)

        # Verify it's valid JSON
        assert json_str is not None
        assert isinstance(json_str, str)
        assert len(json_str) > 0

        # Parse JSON to verify structure
        data = json.loads(json_str)
        assert "shape" in data
        assert "gauge" in data
        assert "rounds" in data
        assert "metadata" in data
        assert len(data["rounds"]) == 3

    def test_json_roundtrip_compatibility(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test JSON round-trip: DSL -> JSON -> DSL."""
        # Export to JSON
        json_str = service.generate_json(simple_pattern)

        # Import back to PatternDSL
        restored = PatternDSL.from_json(json_str)

        # Verify key fields match
        assert restored.shape.shape_type == simple_pattern.shape.shape_type
        assert restored.shape.diameter_cm == simple_pattern.shape.diameter_cm
        assert restored.gauge.stitches_per_cm == simple_pattern.gauge.stitches_per_cm
        assert len(restored.rounds) == len(simple_pattern.rounds)
        assert restored.metadata.total_rounds == simple_pattern.metadata.total_rounds

    def test_json_export_complex(
        self, service: ExportService, complex_pattern: PatternDSL
    ) -> None:
        """Test JSON export of complex pattern."""
        json_str = service.generate_json(complex_pattern)

        # Parse and verify
        data = json.loads(json_str)
        assert data["shape"]["shape_type"] == "cone"
        assert "base_diameter_cm" in data["shape"]
        assert "top_diameter_cm" in data["shape"]
        assert len(data["rounds"]) == 10

    # =============================================================================
    # PDF Export Tests
    # =============================================================================

    def test_pdf_generation_a4(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test PDF generation with A4 paper size."""
        pdf_bytes = service.generate_pdf(simple_pattern, paper_size="A4")

        # Verify PDF was generated
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

        # Verify it's a valid PDF
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        assert len(reader.pages) >= 1  # At least cover + pattern pages

    def test_pdf_generation_letter(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test PDF generation with letter paper size."""
        pdf_bytes = service.generate_pdf(simple_pattern, paper_size="letter")

        # Verify PDF was generated
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

        # Verify it's a valid PDF
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        assert len(reader.pages) >= 1

    def test_pdf_invalid_paper_size(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test PDF generation with invalid paper size raises ValueError."""
        with pytest.raises(ValueError, match="Invalid paper size"):
            service.generate_pdf(simple_pattern, paper_size="tabloid")  # type: ignore

    def test_pdf_file_size_constraint(
        self, service: ExportService, complex_pattern: PatternDSL
    ) -> None:
        """Test PDF file size is under 5 MB constraint."""
        pdf_bytes = service.generate_pdf(complex_pattern, paper_size="A4")

        size_mb = len(pdf_bytes) / (1024 * 1024)
        assert size_mb < 5.0, f"PDF size {size_mb:.2f} MB exceeds 5 MB limit"

    def test_pdf_generation_performance(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test PDF generation completes within 5 seconds."""
        import time

        start_time = time.time()
        service.generate_pdf(simple_pattern, paper_size="A4")
        elapsed = time.time() - start_time

        assert elapsed < 5.0, f"PDF generation took {elapsed:.2f}s (limit: 5s)"

    def test_pdf_contains_pattern_data(
        self, service: ExportService, simple_pattern: PatternDSL
    ) -> None:
        """Test PDF contains pattern text content."""
        pdf_bytes = service.generate_pdf(simple_pattern, paper_size="A4")

        # Parse PDF and extract text
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)

        # Collect all text from PDF
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text()

        # Verify key content is present
        assert "Sphere" in all_text  # Shape type
        assert "Materials" in all_text  # Materials section
        assert "Pattern Instructions" in all_text  # Instructions section
        assert "Round 1" in all_text  # At least one round
        assert "6 sts" in all_text  # Stitch count

    def test_pdf_complex_pattern(
        self, service: ExportService, complex_pattern: PatternDSL
    ) -> None:
        """Test PDF generation for complex cone pattern."""
        pdf_bytes = service.generate_pdf(complex_pattern, paper_size="A4")

        # Verify PDF was generated
        assert len(pdf_bytes) > 0

        # Parse and verify content
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text()

        assert "Cone" in all_text
        assert "Round 10" in all_text  # Last round

    # =============================================================================
    # Helper Method Tests
    # =============================================================================

    def test_format_round_simple(self, service: ExportService) -> None:
        """Test round formatting for simple round."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=6)],
            total_stitches=6,
        )

        formatted = service._format_round(round_inst)

        assert "Round 1:" in formatted  # 1-indexed
        assert "6 sc" in formatted
        assert "(6 sts)" in formatted

    def test_format_round_with_description(self, service: ExportService) -> None:
        """Test round formatting includes description."""
        round_inst = RoundInstruction(
            round_number=1,
            stitches=[StitchInstruction(stitch_type="inc", count=6)],
            total_stitches=12,
            description="Increase round",
        )

        formatted = service._format_round(round_inst)

        assert "Round 2:" in formatted
        assert "6 inc" in formatted
        assert "(12 sts)" in formatted
        assert "Increase round" in formatted

    def test_format_round_multiple_stitches(self, service: ExportService) -> None:
        """Test round formatting with multiple stitch types."""
        round_inst = RoundInstruction(
            round_number=2,
            stitches=[
                StitchInstruction(stitch_type="sc", count=2),
                StitchInstruction(stitch_type="inc", count=1),
            ],
            total_stitches=18,
        )

        formatted = service._format_round(round_inst)

        assert "Round 3:" in formatted
        assert "2 sc" in formatted
        assert "inc" in formatted  # Single stitch (count=1)
        assert "(18 sts)" in formatted

    # =============================================================================
    # Edge Case Tests
    # =============================================================================

    def test_pdf_minimal_pattern(self, service: ExportService, sample_gauge: GaugeInfo) -> None:
        """Test PDF generation with minimal 1-round pattern."""
        shape = ShapeParameters(shape_type="sphere", diameter_cm=5.0)
        metadata = PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=1,
        )
        rounds = [
            RoundInstruction(
                round_number=0,
                stitches=[StitchInstruction(stitch_type="sc", count=6)],
                total_stitches=6,
            )
        ]

        pattern = PatternDSL(shape=shape, gauge=sample_gauge, rounds=rounds, metadata=metadata)

        pdf_bytes = service.generate_pdf(pattern, paper_size="A4")
        assert len(pdf_bytes) > 0

    def test_json_export_no_optional_fields(
        self, service: ExportService, sample_gauge: GaugeInfo
    ) -> None:
        """Test JSON export with minimal required fields only."""
        shape = ShapeParameters(shape_type="cylinder", diameter_cm=8.0, height_cm=12.0)
        metadata = PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=2,
        )
        rounds = [
            RoundInstruction(
                round_number=0,
                stitches=[StitchInstruction(stitch_type="sc", count=6)],
                total_stitches=6,
            ),
            RoundInstruction(
                round_number=1,
                stitches=[StitchInstruction(stitch_type="sc", count=6)],
                total_stitches=6,
            ),
        ]

        pattern = PatternDSL(
            shape=shape, gauge=sample_gauge, rounds=rounds, metadata=metadata  # No notes
        )

        json_str = service.generate_json(pattern)
        assert json_str is not None
        assert len(json_str) > 0

        # Verify round-trip
        restored = PatternDSL.from_json(json_str)
        assert restored.notes is None

    def test_pdf_with_all_optional_fields(
        self, service: ExportService, sample_shape: ShapeParameters
    ) -> None:
        """Test PDF generation with all optional fields populated."""
        gauge = GaugeInfo(
            stitches_per_cm=1.4,
            rows_per_cm=1.6,
            hook_size_mm=4.0,
            yarn_weight="worsted",
            swatch_notes="Blocked swatch measurement",
        )

        metadata = PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=2,
            difficulty="advanced",
            estimated_time_minutes=180,
            tags=["amigurumi", "sphere", "intermediate"],
        )

        rounds = [
            RoundInstruction(
                round_number=0,
                stitches=[StitchInstruction(stitch_type="sc", count=6, note="In magic ring")],
                total_stitches=6,
                description="Magic ring start",
            ),
            RoundInstruction(
                round_number=1,
                stitches=[StitchInstruction(stitch_type="inc", count=6)],
                total_stitches=12,
                description="Full increase round",
            ),
        ]

        pattern = PatternDSL(
            shape=sample_shape,
            gauge=gauge,
            rounds=rounds,
            metadata=metadata,
            notes="Advanced pattern. Requires stitch marker and tapestry needle.",
        )

        pdf_bytes = service.generate_pdf(pattern, paper_size="A4")
        assert len(pdf_bytes) > 0

        # Verify content includes optional fields
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text()

        assert "Advanced" in all_text
        assert "180 minutes" in all_text
        assert "Blocked swatch" in all_text
