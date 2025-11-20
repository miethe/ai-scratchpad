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


class TestVisualizationAPI3D:
    """Integration tests for 3D visualization mode"""

    def test_3d_mode_query_parameter(self):
        """POST /visualization/frames?mode=3d returns 3D coordinates"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")
        pattern_json = pattern.model_dump(mode="json")

        # Request with mode=3d
        response = client.post(
            "/api/v1/visualization/frames?mode=3d",
            json=pattern_json
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response has 3D data
        assert "frames" in data
        assert len(data["frames"]) > 0

        frame = data["frames"][0]
        node = frame["nodes"][0]

        # 3D mode should have position_3d
        assert "position_3d" in node
        assert len(node["position_3d"]) == 3
        assert all(isinstance(coord, (int, float)) for coord in node["position_3d"])

        # Should have depth ordering
        assert "depth_order" in node
        assert isinstance(node["depth_order"], int)

        # Should have depth factor
        assert "depth_factor" in node
        assert 0.0 <= node["depth_factor"] <= 1.0

        # Should have projection metadata
        assert "projection" in frame
        assert frame["projection"]["type"] == "isometric"
        assert frame["projection"]["angle_deg"] == 30.0
        assert "bounds_3d" in frame["projection"]

    def test_2d_mode_backward_compatible(self):
        """POST /visualization/frames?mode=2d (or default) does NOT include 3D fields"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")
        pattern_json = pattern.model_dump(mode="json")

        # Test default (no mode parameter)
        response = client.post("/api/v1/visualization/frames", json=pattern_json)
        assert response.status_code == 200
        data = response.json()

        frame = data["frames"][0]
        node = frame["nodes"][0]

        # 2D mode should NOT have 3D fields
        assert "position_3d" not in node or node["position_3d"] is None
        assert "depth_order" not in node or node["depth_order"] is None
        assert "depth_factor" not in node or node["depth_factor"] is None
        assert "projection" not in frame or frame["projection"] is None

        # Should still have 2D position
        assert "position" in node
        assert len(node["position"]) == 2

    def test_3d_mode_explicit_2d(self):
        """POST /visualization/frames?mode=2d explicitly returns 2D data"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")
        pattern_json = pattern.model_dump(mode="json")

        response = client.post(
            "/api/v1/visualization/frames?mode=2d",
            json=pattern_json
        )

        assert response.status_code == 200
        data = response.json()

        frame = data["frames"][0]
        node = frame["nodes"][0]

        # Explicit 2D should not have 3D fields
        assert "position_3d" not in node or node["position_3d"] is None

    def test_3d_sphere_coordinates_valid(self):
        """Verify sphere 3D coordinates lie on sphere surface"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames?mode=3d",
            json=pattern.model_dump(mode="json")
        )

        data = response.json()

        # Get first frame nodes
        frame = data["frames"][0]
        nodes = frame["nodes"]

        # All nodes should lie approximately on sphere surface
        # Use BASE_RADIUS from service (100.0)
        expected_radius = 100.0

        for node in nodes:
            x, y, z = node["position_3d"]
            distance = (x**2 + y**2 + z**2) ** 0.5
            # Allow some tolerance for floating point
            assert abs(distance - expected_radius) < 1.0

    def test_3d_depth_ordering_valid(self):
        """Verify depth_order is consistent across frames"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames?mode=3d",
            json=pattern.model_dump(mode="json")
        )

        data = response.json()

        # Collect all nodes
        all_nodes = []
        for frame in data["frames"]:
            all_nodes.extend(frame["nodes"])

        # Verify depth_order values are unique and sequential
        depth_orders = [node["depth_order"] for node in all_nodes]
        assert len(set(depth_orders)) == len(depth_orders)  # All unique
        assert min(depth_orders) == 0
        assert max(depth_orders) == len(all_nodes) - 1

    def test_3d_projection_metadata_complete(self):
        """Verify projection metadata has all required fields"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=10.0, gauge=gauge, yarn_weight="Worsted")

        response = client.post(
            "/api/v1/visualization/frames?mode=3d",
            json=pattern.model_dump(mode="json")
        )

        data = response.json()
        frame = data["frames"][0]
        projection = frame["projection"]

        # Verify all required fields
        assert "type" in projection
        assert projection["type"] in ["isometric", "dimetric", "perspective"]

        assert "angle_deg" in projection
        assert 0 <= projection["angle_deg"] <= 90

        assert "bounds_3d" in projection
        bounds = projection["bounds_3d"]
        assert all(key in bounds for key in ["x_min", "x_max", "y_min", "y_max", "z_min", "z_max"])
        assert bounds["x_min"] < bounds["x_max"]
        assert bounds["y_min"] < bounds["y_max"]
        assert bounds["z_min"] < bounds["z_max"]

    def test_3d_mode_performance(self):
        """Verify 3D mode meets performance target (< 150ms)"""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14.0, rows_per_10cm=16.0)
        pattern = compiler.generate(diameter_cm=15.0, gauge=gauge, yarn_weight="Worsted")
        pattern_json = pattern.model_dump(mode="json")

        # Measure 3D mode response time
        start = time.perf_counter()
        response = client.post(
            "/api/v1/visualization/frames?mode=3d",
            json=pattern_json
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 150.0  # Performance target: < 150ms for 3D

        print(f"\n3D Performance: {elapsed_ms:.2f}ms for {len(pattern.rounds)} rounds")
