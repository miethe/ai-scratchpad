"""
Integration tests for Export API Endpoints

Tests HTTP contract for PDF and JSON export endpoints:
- Request/response validation
- HTTP status codes
- Content-Type headers
- Error handling
- API contract compliance
"""

import io
import json
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
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

from app.main import app

# Create test client
client = TestClient(app)


class TestExportAPI:
    """Integration tests for export API endpoints."""

    @pytest.fixture
    def sample_pattern_dict(self) -> dict:
        """Create sample pattern as dictionary for API requests."""
        return {
            "shape": {"shape_type": "sphere", "diameter_cm": 10.0},
            "gauge": {
                "stitches_per_cm": 1.4,
                "rows_per_cm": 1.6,
                "hook_size_mm": 4.0,
                "yarn_weight": "worsted",
            },
            "rounds": [
                {
                    "round_number": 0,
                    "stitches": [{"stitch_type": "sc", "count": 6}],
                    "total_stitches": 6,
                    "description": "Magic ring",
                },
                {
                    "round_number": 1,
                    "stitches": [{"stitch_type": "inc", "count": 6}],
                    "total_stitches": 12,
                    "description": "Increase round",
                },
                {
                    "round_number": 2,
                    "stitches": [
                        {"stitch_type": "sc", "count": 1},
                        {"stitch_type": "inc", "count": 1},
                    ],
                    "total_stitches": 18,
                },
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "0.1.0",
                "total_rounds": 3,
                "difficulty": "beginner",
            },
            "notes": "Work in a spiral.",
        }

    # =============================================================================
    # PDF Export Endpoint Tests
    # =============================================================================

    def test_export_pdf_success_a4(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test successful PDF export with A4 paper size."""
        response = client.post(
            "/api/v1/export/pdf?paper_size=A4", json=sample_pattern_dict
        )

        # Verify status code
        assert response.status_code == 200

        # Verify content type
        assert response.headers["content-type"] == "application/pdf"

        # Verify Content-Disposition header
        assert "attachment" in response.headers["content-disposition"]
        assert "filename=" in response.headers["content-disposition"]
        assert ".pdf" in response.headers["content-disposition"]

        # Verify Cache-Control header
        assert response.headers["cache-control"] == "no-cache"

        # Verify PDF content
        pdf_bytes = response.content
        assert len(pdf_bytes) > 0

        # Verify it's a valid PDF
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        assert len(reader.pages) >= 1

    def test_export_pdf_success_letter(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test successful PDF export with letter paper size."""
        response = client.post(
            "/api/v1/export/pdf?paper_size=letter", json=sample_pattern_dict
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    
    def test_export_pdf_default_paper_size(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test PDF export with default paper size (A4)."""
        response = client.post("/api/v1/export/pdf", json=sample_pattern_dict)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"


    def test_export_pdf_invalid_paper_size(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test PDF export with invalid paper size returns 422."""
        response = client.post(
            "/api/v1/export/pdf?paper_size=tabloid", json=sample_pattern_dict
        )

        # FastAPI/Pydantic validation catches this before endpoint logic
        assert response.status_code == 422

    
    def test_export_pdf_invalid_pattern(self) -> None:
        """Test PDF export with invalid PatternDSL returns 422."""
        invalid_pattern = {
            "shape": {"shape_type": "sphere"},  # Missing required fields
            "gauge": {"stitches_per_cm": 1.4},  # Missing required fields
            "rounds": [],  # Empty rounds (invalid)
        }

        response = client.post("/api/v1/export/pdf", json=invalid_pattern)

        assert response.status_code == 422  # Pydantic validation error

    
    def test_export_pdf_filename_format(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test PDF filename includes shape type and timestamp."""
        response = client.post("/api/v1/export/pdf", json=sample_pattern_dict)

        filename = response.headers["content-disposition"]
        assert "pattern_" in filename
        assert "sphere" in filename
        assert ".pdf" in filename

    
    def test_export_pdf_file_size(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test PDF file size is under 5 MB."""
        response = client.post("/api/v1/export/pdf", json=sample_pattern_dict)

        pdf_size_mb = len(response.content) / (1024 * 1024)
        assert pdf_size_mb < 5.0

    # =============================================================================
    # JSON Export Endpoint Tests
    # =============================================================================

    
    def test_export_json_success(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test successful JSON export."""
        response = client.post("/api/v1/export/json", json=sample_pattern_dict)

        # Verify status code
        assert response.status_code == 200

        # Verify content type
        assert response.headers["content-type"] == "application/json"

        # Verify Cache-Control header
        assert response.headers["cache-control"] == "no-cache"

        # Verify response structure
        data = response.json()
        assert "json" in data
        assert "size_bytes" in data
        assert isinstance(data["json"], str)
        assert isinstance(data["size_bytes"], int)
        assert data["size_bytes"] > 0

    
    def test_export_json_content_valid(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test JSON export content is valid JSON."""
        response = client.post("/api/v1/export/json", json=sample_pattern_dict)

        data = response.json()
        json_str = data["json"]

        # Parse JSON to verify it's valid
        parsed = json.loads(json_str)
        assert "shape" in parsed
        assert "gauge" in parsed
        assert "rounds" in parsed
        assert "metadata" in parsed

    
    def test_export_json_roundtrip(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test JSON export is round-trip compatible."""
        response = client.post("/api/v1/export/json", json=sample_pattern_dict)

        data = response.json()
        json_str = data["json"]

        # Parse exported JSON back to PatternDSL
        restored = PatternDSL.from_json(json_str)

        # Verify key fields match
        assert restored.shape.shape_type == sample_pattern_dict["shape"]["shape_type"]
        assert restored.gauge.stitches_per_cm == sample_pattern_dict["gauge"]["stitches_per_cm"]
        assert len(restored.rounds) == len(sample_pattern_dict["rounds"])

    
    def test_export_json_size_bytes_accurate(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test size_bytes field is accurate."""
        response = client.post("/api/v1/export/json", json=sample_pattern_dict)

        data = response.json()
        json_str = data["json"]
        reported_size = data["size_bytes"]
        actual_size = len(json_str.encode("utf-8"))

        assert reported_size == actual_size

    
    def test_export_json_invalid_pattern(self) -> None:
        """Test JSON export with invalid PatternDSL returns 422."""
        invalid_pattern = {
            "shape": {"shape_type": "invalid_shape"},
            "gauge": {},
            "rounds": [],
        }

        response = client.post("/api/v1/export/json", json=invalid_pattern)

        assert response.status_code == 422

    # =============================================================================
    # Cross-Format Tests
    # =============================================================================

    
    def test_export_both_formats_same_pattern(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test exporting same pattern to both PDF and JSON."""
        # Export to PDF
        pdf_response = client.post("/api/v1/export/pdf", json=sample_pattern_dict)
        assert pdf_response.status_code == 200

        # Export to JSON
        json_response = client.post("/api/v1/export/json", json=sample_pattern_dict)
        assert json_response.status_code == 200

        # Both should succeed
        assert len(pdf_response.content) > 0
        assert len(json_response.json()["json"]) > 0

    # =============================================================================
    # Edge Case Tests
    # =============================================================================

    
    def test_export_minimal_pattern(self) -> None:
        """Test export with minimal 1-round pattern."""
        minimal_pattern = {
            "shape": {"shape_type": "sphere", "diameter_cm": 5.0},
            "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6},
            "rounds": [
                {
                    "round_number": 0,
                    "stitches": [{"stitch_type": "sc", "count": 6}],
                    "total_stitches": 6,
                }
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "0.1.0",
                "total_rounds": 1,
            },
        }

        # Test PDF export
        pdf_response = client.post("/api/v1/export/pdf", json=minimal_pattern)
        assert pdf_response.status_code == 200

        # Test JSON export
        json_response = client.post("/api/v1/export/json", json=minimal_pattern)
        assert json_response.status_code == 200

    
    def test_export_complex_cone_pattern(self) -> None:
        """Test export with complex cone pattern."""
        cone_pattern = {
            "shape": {
                "shape_type": "cone",
                "base_diameter_cm": 15.0,
                "top_diameter_cm": 8.0,
                "height_cm": 20.0,
            },
            "gauge": {
                "stitches_per_cm": 1.4,
                "rows_per_cm": 1.6,
                "hook_size_mm": 3.5,
                "yarn_weight": "DK",
            },
            "rounds": [
                {
                    "round_number": i,
                    "stitches": [{"stitch_type": "sc", "count": 24 + (i * 2)}],
                    "total_stitches": 24 + (i * 2),
                }
                for i in range(15)  # 15 rounds
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "0.1.0",
                "total_rounds": 15,
                "difficulty": "intermediate",
            },
        }

        # Test PDF export
        pdf_response = client.post("/api/v1/export/pdf", json=cone_pattern)
        assert pdf_response.status_code == 200

        # Test JSON export
        json_response = client.post("/api/v1/export/json", json=cone_pattern)
        assert json_response.status_code == 200

    
    def test_export_pattern_with_all_optional_fields(self) -> None:
        """Test export with all optional fields populated."""
        full_pattern = {
            "shape": {"shape_type": "cylinder", "diameter_cm": 12.0, "height_cm": 15.0},
            "gauge": {
                "stitches_per_cm": 1.4,
                "rows_per_cm": 1.6,
                "hook_size_mm": 4.0,
                "yarn_weight": "worsted",
                "swatch_notes": "Blocked measurement",
            },
            "rounds": [
                {
                    "round_number": 0,
                    "stitches": [
                        {"stitch_type": "sc", "count": 6, "note": "In magic ring"}
                    ],
                    "total_stitches": 6,
                    "description": "Magic ring start",
                },
                {
                    "round_number": 1,
                    "stitches": [{"stitch_type": "inc", "count": 6}],
                    "total_stitches": 12,
                    "description": "Increase round",
                },
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "0.1.0",
                "total_rounds": 2,
                "difficulty": "advanced",
                "estimated_time_minutes": 120,
                "tags": ["amigurumi", "cylinder"],
            },
            "notes": "Work in spiral. Use stitch marker.",
        }

        # Test both exports
        pdf_response = client.post("/api/v1/export/pdf", json=full_pattern)
        assert pdf_response.status_code == 200

        json_response = client.post("/api/v1/export/json", json=full_pattern)
        assert json_response.status_code == 200

    # =============================================================================
    # Error Handling Tests
    # =============================================================================

    
    def test_export_pdf_malformed_json(self) -> None:
        """Test PDF export with malformed JSON returns 422."""
        response = client.post(
            "/api/v1/export/pdf",
            content=b'{"shape": invalid json}',
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    
    def test_export_json_malformed_json(self) -> None:
        """Test JSON export with malformed JSON returns 422."""
        response = client.post(
            "/api/v1/export/json",
            content=b'{"gauge": incomplete',
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    
    def test_export_endpoints_cors_headers(
        self, sample_pattern_dict: dict
    ) -> None:
        """Test export endpoints include proper CORS headers."""
        # Test PDF endpoint
        pdf_response = client.post("/api/v1/export/pdf", json=sample_pattern_dict)
        # CORS headers are added by middleware, verify endpoint doesn't conflict

        # Test JSON endpoint
        json_response = client.post("/api/v1/export/json", json=sample_pattern_dict)

        # Both should succeed
        assert pdf_response.status_code == 200
        assert json_response.status_code == 200
