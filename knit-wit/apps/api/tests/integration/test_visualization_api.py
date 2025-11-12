"""
Integration tests for Visualization API endpoint.

Tests the POST /api/v1/visualization/frames endpoint with real PatternDSL
data generated from the pattern engine.
"""

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
import sys
from pathlib import Path

# Add pattern engine to Python path
pattern_engine_path = Path(__file__).resolve().parents[5] / "packages" / "pattern-engine"
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.shapes.sphere import SphereCompiler
from knit_wit_engine.models.requests import Gauge

client = TestClient(app)


class TestVisualizationAPI:
    """Integration tests for visualization API endpoint"""

    def test_generate_frames_success(self):
        """POST /visualization/frames with valid PatternDSL returns 200 OK"""
        # Generate test pattern using Phase 1 compiler
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        # Convert to JSON
        pattern_json = pattern.model_dump(mode="json")

        # POST to API
        response = client.post("/api/v1/visualization/frames", json=pattern_json)

        # Validate response
        assert response.status_code == 200
        data = response.json()

        # Verify response schema
        assert "frames" in data
        assert "total_rounds" in data
        assert "shape_type" in data
        assert isinstance(data["frames"], list)
        assert len(data["frames"]) > 0

        # Verify first frame structure
        frame = data["frames"][0]
        assert "round_number" in frame
        assert "nodes" in frame
        assert "edges" in frame
        assert "stitch_count" in frame
        assert "highlights" in frame

        # Verify node structure
        assert len(frame["nodes"]) > 0
        node = frame["nodes"][0]
        assert "id" in node
        assert "stitch_type" in node
        assert "position" in node
        assert "highlight" in node
        assert len(node["position"]) == 2  # (x, y) tuple

        # Verify edge structure
        assert len(frame["edges"]) > 0
        edge = frame["edges"][0]
        assert "source" in edge
        assert "target" in edge

    def test_generate_frames_invalid_dsl(self):
        """POST /visualization/frames with invalid DSL returns 422"""
        invalid_dsl = {
            "meta": {"gauge": "invalid"},  # Invalid gauge type
            "rounds": [],
        }

        response = client.post("/api/v1/visualization/frames", json=invalid_dsl)
        assert response.status_code == 422

    def test_generate_frames_performance(self):
        """Verify frame generation completes within performance target"""
        # Generate 50-round pattern (large test)
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=25.0, gauge=gauge, yarn_weight="Worsted")

        pattern_json = pattern.model_dump(mode="json")

        # Measure API response time
        start = time.perf_counter()
        response = client.post("/api/v1/visualization/frames", json=pattern_json)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 100.0  # Performance target: < 100ms

        # Log performance for visibility
        print(f"\nPerformance: {elapsed_ms:.2f}ms for {len(pattern.rounds)} rounds")

    def test_response_schema_matches_spec(self):
        """Verify response matches VisualizationResponse schema exactly"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames", json=pattern.model_dump(mode="json")
        )
        data = response.json()

        # Validate top-level schema
        assert set(data.keys()) == {"frames", "total_rounds", "shape_type"}

        # Validate frame schema
        for frame in data["frames"]:
            assert set(frame.keys()) == {
                "round_number",
                "nodes",
                "edges",
                "stitch_count",
                "highlights",
            }

            # Validate node schema
            for node in frame["nodes"]:
                assert set(node.keys()) == {"id", "stitch_type", "position", "highlight"}
                assert len(node["position"]) == 2  # (x, y) tuple
                assert node["highlight"] in ["normal", "increase", "decrease"]

            # Validate edge schema
            for edge in frame["edges"]:
                assert set(edge.keys()) == {"source", "target"}

    def test_empty_pattern_handling(self):
        """Verify API handles edge case of pattern with no rounds gracefully"""
        # Create minimal pattern (though pattern engine wouldn't generate this)
        minimal_pattern = {
            "meta": {
                "version": "0.1",
                "units": "cm",
                "terms": "US",
                "stitch": "sc",
                "round_mode": "spiral",
                "gauge": {"sts_per_10cm": 14.0, "rows_per_10cm": 16.0},
            },
            "shape": {"shape_type": "sphere", "params": {"diameter": 10}},
            "rounds": [],
            "materials": {
                "yarn_weight": "Worsted",
                "hook_size_mm": 4.0,
                "yardage_estimate": 0,
            },
        }

        response = client.post("/api/v1/visualization/frames", json=minimal_pattern)

        # Should handle gracefully (either 200 with empty frames or 422)
        assert response.status_code in [200, 422]

    def test_highlight_detection(self):
        """Verify increases and decreases are properly highlighted"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames", json=pattern.model_dump(mode="json")
        )
        data = response.json()

        # Find frames with increase/decrease operations
        has_increases = False
        has_decreases = False

        for frame in data["frames"]:
            for node in frame["nodes"]:
                if node["stitch_type"] == "inc":
                    assert node["highlight"] == "increase"
                    has_increases = True
                elif node["stitch_type"] == "dec":
                    assert node["highlight"] == "decrease"
                    has_decreases = True

        # Sphere patterns should have increases (and possibly decreases)
        assert has_increases, "Expected to find increase nodes in sphere pattern"

    def test_circular_layout_closure(self):
        """Verify edges form proper circular layout with closing edge"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames", json=pattern.model_dump(mode="json")
        )
        data = response.json()

        # Check first frame's edges
        frame = data["frames"][0]
        nodes = frame["nodes"]
        edges = frame["edges"]

        # Should have N edges for N nodes (including closing edge)
        assert len(edges) == len(nodes)

        # Verify consecutive edges
        for i in range(len(nodes) - 1):
            expected_source = nodes[i]["id"]
            expected_target = nodes[i + 1]["id"]
            edge = edges[i]
            assert edge["source"] == expected_source
            assert edge["target"] == expected_target

        # Verify closing edge
        closing_edge = edges[-1]
        assert closing_edge["source"] == nodes[-1]["id"]
        assert closing_edge["target"] == nodes[0]["id"]

    def test_openapi_documentation(self):
        """Verify endpoint is documented in OpenAPI schema"""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()

        # Check endpoint exists in spec
        assert "/api/v1/visualization/frames" in openapi_spec["paths"]

        # Check POST method exists
        endpoint_spec = openapi_spec["paths"]["/api/v1/visualization/frames"]
        assert "post" in endpoint_spec

        # Check response schema is documented
        post_spec = endpoint_spec["post"]
        assert "200" in post_spec["responses"]

        # Check tags
        assert "visualization" in post_spec["tags"]
