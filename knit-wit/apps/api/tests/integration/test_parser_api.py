"""
Integration tests for Parser API endpoint

Tests the POST /api/v1/parser/parse endpoint with realistic scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestParserEndpoint:
    """Test parser API endpoint."""

    def test_parse_simple_pattern(self, client):
        """Test parsing a simple pattern."""
        response = client.post(
            "/api/v1/parser/parse",
            json={
                "text": "R1: MR 6 sc (6)\nR2: inc x6 (12)"
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "dsl" in data
        assert "validation" in data

        # Check DSL structure
        dsl = data["dsl"]
        assert "meta" in dsl
        assert "rounds" in dsl
        assert len(dsl["rounds"]) == 2

        # Check validation
        validation = data["validation"]
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

    def test_parse_bracket_sequence(self, client):
        """Test parsing pattern with bracket sequences."""
        response = client.post(
            "/api/v1/parser/parse",
            json={
                "text": "R1: MR 6 sc (6)\nR2: inc x6 (12)\nR3: [2 sc, inc] x6 (18)"
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Check round 3 has sequence operation
        rounds = data["dsl"]["rounds"]
        round_3 = next((r for r in rounds if r["r"] == 3), None)
        assert round_3 is not None
        assert round_3["stitches"] == 18

        # Check sequence operation
        seq_op = round_3["ops"][0]
        assert seq_op["op"] == "seq"
        assert seq_op["repeat"] == 6
        assert len(seq_op["ops"]) == 2

    def test_parse_complex_pattern(self, client):
        """Test parsing a complete sphere pattern."""
        pattern = """
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
R4: [3 sc, inc] x6 (24)
R5: [4 sc, inc] x6 (30)
R6: [5 sc, inc] x6 (36)
"""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )

        assert response.status_code == 200
        data = response.json()

        dsl = data["dsl"]
        assert len(dsl["rounds"]) == 6

        # Check stitch progression
        expected_stitches = [6, 12, 18, 24, 30, 36]
        for i, expected in enumerate(expected_stitches):
            assert dsl["rounds"][i]["stitches"] == expected

        # Validation should pass
        assert data["validation"]["valid"] is True

    def test_parse_with_comments(self, client):
        """Test parsing pattern with comments and empty lines."""
        pattern = """
# Sphere pattern
R1: MR 6 sc (6)

# Increase rounds
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
"""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["dsl"]["rounds"]) == 3


class TestParserErrors:
    """Test error handling."""

    def test_parse_empty_text(self, client):
        """Test parsing empty text returns 400."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": ""}
        )

        assert response.status_code == 400
        assert "Empty pattern text" in response.json()["detail"]

    def test_parse_invalid_format(self, client):
        """Test parsing invalid format returns 400."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "Round 1: sc x6 (6)"}  # Wrong format
        )

        assert response.status_code == 400
        assert "Invalid round format" in response.json()["detail"]

    def test_parse_unsupported_stitch(self, client):
        """Test parsing unsupported stitch returns 400 with helpful message."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: bobble x6 (6)"}
        )

        assert response.status_code == 400
        detail = response.json()["detail"]
        assert "Unsupported stitch type" in detail
        assert "bobble" in detail
        # Should suggest alternatives
        assert "Supported:" in detail

    def test_parse_missing_request_body(self, client):
        """Test missing request body returns 422."""
        response = client.post(
            "/api/v1/parser/parse",
            json={}
        )

        assert response.status_code == 422

    def test_parse_invalid_json(self, client):
        """Test invalid JSON returns 422."""
        response = client.post(
            "/api/v1/parser/parse",
            data="not json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422


class TestValidationReporting:
    """Test validation reporting in responses."""

    def test_validation_errors_in_response(self, client):
        """Test that validation errors are included in response."""
        # Pattern with incorrect stitch count
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: inc x6 (10)"}  # Should be 6, not 10
        )

        assert response.status_code == 200  # Parse succeeds
        data = response.json()

        # But validation should fail
        validation = data["validation"]
        assert validation["valid"] is False
        assert len(validation["errors"]) > 0
        assert "stitch count mismatch" in validation["errors"][0].lower()

    def test_validation_warnings_in_response(self, client):
        """Test that validation warnings are included."""
        # Pattern with non-sequential rounds
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: sc x6 (6)\nR5: inc x6 (6)"}
        )

        assert response.status_code == 200
        data = response.json()

        # Should have warnings about skipped rounds
        validation = data["validation"]
        assert len(validation["warnings"]) > 0
        assert "non-sequential" in validation["warnings"][0].lower()

    def test_validation_includes_line_numbers(self, client):
        """Test that validation errors include line numbers."""
        pattern = """
R1: inc x6 (6)
R2: inc x6 (10)
"""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )

        assert response.status_code == 200
        validation = response.json()["validation"]

        # Should have error for R2
        assert len(validation["errors"]) > 0
        assert "R2" in validation["errors"][0]


class TestDSLOutput:
    """Test DSL output structure."""

    def test_dsl_contains_metadata(self, client):
        """Test DSL output contains metadata."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: sc x6 (6)"}
        )

        assert response.status_code == 200
        dsl = response.json()["dsl"]

        # Check meta fields
        assert "meta" in dsl
        meta = dsl["meta"]
        assert meta["version"] == "0.1"
        assert meta["terms"] == "US"
        assert meta["stitch"] == "sc"
        assert meta["round_mode"] == "spiral"

    def test_dsl_contains_object(self, client):
        """Test DSL output contains object definition."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: sc x6 (6)"}
        )

        assert response.status_code == 200
        dsl = response.json()["dsl"]

        # Check object field
        assert "object" in dsl
        obj = dsl["object"]
        assert obj["type"] == "unknown"  # Parser doesn't infer shape
        assert "params" in obj

    def test_dsl_rounds_structure(self, client):
        """Test DSL rounds have correct structure."""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": "R1: [2 sc, inc] x6 (18)"}
        )

        assert response.status_code == 200
        rounds = response.json()["dsl"]["rounds"]

        assert len(rounds) == 1
        round_data = rounds[0]

        # Check round structure
        assert "r" in round_data
        assert "ops" in round_data
        assert "stitches" in round_data

        assert round_data["r"] == 1
        assert round_data["stitches"] == 18

        # Check ops structure
        ops = round_data["ops"]
        assert len(ops) > 0
        assert "op" in ops[0]
        assert "count" in ops[0]


class TestAPIDocumentation:
    """Test API documentation and OpenAPI spec."""

    def test_endpoint_in_openapi_spec(self, client):
        """Test that parser endpoint appears in OpenAPI spec."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi = response.json()
        paths = openapi["paths"]

        # Check endpoint exists
        assert "/api/v1/parser/parse" in paths

        # Check it's a POST endpoint
        endpoint = paths["/api/v1/parser/parse"]
        assert "post" in endpoint

        # Check it has proper description
        post_spec = endpoint["post"]
        assert "summary" in post_spec
        assert "description" in post_spec

    def test_endpoint_has_examples(self, client):
        """Test that endpoint documentation includes examples."""
        response = client.get("/openapi.json")
        openapi = response.json()

        endpoint = openapi["paths"]["/api/v1/parser/parse"]["post"]

        # Should have response examples
        assert "responses" in endpoint
        assert "200" in endpoint["responses"]


class TestPerformance:
    """Test API performance."""

    def test_response_time_under_200ms(self, client):
        """Test that typical patterns parse in < 200ms."""
        import time

        pattern = """
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
R4: [3 sc, inc] x6 (24)
R5: [4 sc, inc] x6 (30)
"""

        start = time.time()
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 0.2, f"Parse took {duration:.3f}s, expected < 0.2s"

    def test_large_pattern_performance(self, client):
        """Test parsing a large pattern (50 rounds) performs acceptably."""
        import time

        # Generate 50-round pattern
        rounds = [f"R{i}: [2 sc, inc] x6 (18)" for i in range(1, 51)]
        pattern = "\n".join(rounds)

        start = time.time()
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )
        duration = time.time() - start

        assert response.status_code == 200
        data = response.json()
        assert len(data["dsl"]["rounds"]) == 50

        # Should still be reasonable for large patterns
        assert duration < 0.5, f"Large parse took {duration:.3f}s"


class TestRealWorldPatterns:
    """Test with realistic crochet patterns."""

    def test_amigurumi_sphere_pattern(self, client):
        """Test parsing a typical amigurumi sphere pattern."""
        pattern = """
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
R4: [3 sc, inc] x6 (24)
R5: [4 sc, inc] x6 (30)
R6: [5 sc, inc] x6 (36)
R7: sc x36 (36)
R8: sc x36 (36)
R9: [5 sc, dec] x6 (30)
R10: [4 sc, dec] x6 (24)
R11: [3 sc, dec] x6 (18)
R12: [2 sc, dec] x6 (12)
R13: dec x6 (6)
"""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )

        assert response.status_code == 200
        data = response.json()

        # Should parse all rounds
        assert len(data["dsl"]["rounds"]) == 13

        # Validation should pass
        assert data["validation"]["valid"] is True

    def test_simple_coaster_pattern(self, client):
        """Test parsing a flat coaster pattern."""
        pattern = """
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [sc, inc] x6 (18)
R4: [2 sc, inc] x6 (24)
R5: [3 sc, inc] x6 (30)
"""
        response = client.post(
            "/api/v1/parser/parse",
            json={"text": pattern}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["dsl"]["rounds"]) == 5
        assert data["validation"]["valid"] is True

        # Check final stitch count
        final_round = data["dsl"]["rounds"][-1]
        assert final_round["stitches"] == 30
