"""
Unit tests for VisualizationService

Comprehensive test coverage for DSL → RenderPrimitive conversion:
- Simple round conversion
- Increase/decrease highlighting
- Circular layout validation
- Edge generation (consecutive + closing)
- Edge cases (empty, single stitch, large rounds)
- Performance benchmarks
"""

import math
import pytest
from datetime import datetime

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

from app.services.visualization_service import VisualizationService
from app.models.visualization import (
    RenderNode,
    RenderEdge,
    VisualizationFrame,
    VisualizationResponse,
)


class TestVisualizationService:
    """Test suite for VisualizationService."""

    @pytest.fixture
    def service(self):
        """Create VisualizationService instance."""
        return VisualizationService()

    @pytest.fixture
    def sample_gauge(self):
        """Create sample gauge info."""
        return GaugeInfo(
            stitches_per_cm=1.4, rows_per_cm=1.6, hook_size_mm=4.0, yarn_weight="worsted"
        )

    @pytest.fixture
    def sample_shape(self):
        """Create sample shape parameters."""
        return ShapeParameters(shape_type="sphere", diameter_cm=10.0)

    @pytest.fixture
    def sample_metadata(self):
        """Create sample pattern metadata."""
        return PatternMetadata(
            generated_at=datetime.now(),
            engine_version="0.1.0",
            total_rounds=3,
            difficulty="beginner",
        )

    def test_simple_round_conversion(self, service):
        """Test conversion of simple round with 6 sc stitches."""
        # Create round with 6 single crochet stitches
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=6)],
            total_stitches=6,
        )

        frame = service._round_to_frame(round_inst)

        # Verify frame structure
        assert frame.round_number == 1  # 1-indexed
        assert frame.stitch_count == 6
        assert len(frame.nodes) == 6
        assert len(frame.edges) == 6  # 5 consecutive + 1 closing
        assert len(frame.highlights) == 0  # No increases/decreases

        # Verify all nodes have correct stitch type
        for node in frame.nodes:
            assert node.stitch_type == "sc"
            assert node.highlight == "normal"

    def test_increase_highlighting(self, service):
        """Test round with all increases highlights correctly."""
        round_inst = RoundInstruction(
            round_number=1,
            stitches=[StitchInstruction(stitch_type="inc", count=6)],
            total_stitches=6,
        )

        frame = service._round_to_frame(round_inst)

        # All nodes should be highlighted as increases
        assert len(frame.highlights) == 6
        assert frame.stitch_count == 6

        for node in frame.nodes:
            assert node.stitch_type == "inc"
            assert node.highlight == "increase"
            assert node.id in frame.highlights

    def test_decrease_highlighting(self, service):
        """Test round with decreases highlights correctly."""
        round_inst = RoundInstruction(
            round_number=2,
            stitches=[StitchInstruction(stitch_type="dec", count=3)],
            total_stitches=3,
        )

        frame = service._round_to_frame(round_inst)

        # All nodes should be highlighted as decreases
        assert len(frame.highlights) == 3
        assert frame.stitch_count == 3

        for node in frame.nodes:
            assert node.stitch_type == "dec"
            assert node.highlight == "decrease"
            assert node.id in frame.highlights

    def test_circular_layout(self, service):
        """Verify node positions form a circle."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=8)],
            total_stitches=8,
        )

        frame = service._round_to_frame(round_inst)

        # Verify all nodes are equidistant from origin
        for node in frame.nodes:
            x, y = node.position
            distance = math.sqrt(x**2 + y**2)
            assert abs(distance - service.BASE_RADIUS) < 0.001  # Allow floating point error

        # Verify angular spacing is uniform
        expected_angle_step = (2 * math.pi) / 8

        for i, node in enumerate(frame.nodes):
            x, y = node.position
            actual_angle = math.atan2(y, x)
            expected_angle = i * expected_angle_step

            # Normalize angles to [0, 2π]
            actual_angle = actual_angle if actual_angle >= 0 else actual_angle + 2 * math.pi
            expected_angle = expected_angle if expected_angle >= 0 else expected_angle + 2 * math.pi

            assert abs(actual_angle - expected_angle) < 0.001

    def test_edge_generation(self, service):
        """Verify consecutive and closing edges are generated correctly."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=4)],
            total_stitches=4,
        )

        frame = service._round_to_frame(round_inst)

        assert len(frame.edges) == 4

        # Verify consecutive edges
        for i in range(3):
            edge = frame.edges[i]
            assert edge.source == f"r0s{i}"
            assert edge.target == f"r0s{i+1}"

        # Verify closing edge
        closing_edge = frame.edges[-1]
        assert closing_edge.source == "r0s3"
        assert closing_edge.target == "r0s0"

    def test_empty_round_not_allowed(self, service):
        """Test that empty rounds (0 stitches) are rejected by DSL validation."""
        # The PatternDSL correctly validates that rounds must have >= 1 stitch
        # This test verifies the validation works
        with pytest.raises(Exception):  # ValidationError from Pydantic
            round_inst = RoundInstruction(round_number=0, stitches=[], total_stitches=0)

    def test_single_stitch(self, service):
        """Test edge case: round with 1 stitch."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=1)],
            total_stitches=1,
        )

        frame = service._round_to_frame(round_inst)

        assert frame.stitch_count == 1
        assert len(frame.nodes) == 1
        assert len(frame.edges) == 1  # Closing edge only

        # Verify closing edge connects to itself
        edge = frame.edges[0]
        assert edge.source == "r0s0"
        assert edge.target == "r0s0"

    def test_large_round(self, service):
        """Test round with 100+ stitches."""
        round_inst = RoundInstruction(
            round_number=5,
            stitches=[StitchInstruction(stitch_type="sc", count=120)],
            total_stitches=120,
        )

        frame = service._round_to_frame(round_inst)

        assert frame.stitch_count == 120
        assert len(frame.nodes) == 120
        assert len(frame.edges) == 120

        # Verify circular distribution still holds
        for node in frame.nodes:
            x, y = node.position
            distance = math.sqrt(x**2 + y**2)
            assert abs(distance - service.BASE_RADIUS) < 0.001

    def test_mixed_operations(self, service):
        """Test round with sc, inc, dec mixed."""
        round_inst = RoundInstruction(
            round_number=3,
            stitches=[
                StitchInstruction(stitch_type="sc", count=2),
                StitchInstruction(stitch_type="inc", count=1),
                StitchInstruction(stitch_type="sc", count=1),
                StitchInstruction(stitch_type="dec", count=1),
                StitchInstruction(stitch_type="sc", count=1),
            ],
            total_stitches=6,
        )

        frame = service._round_to_frame(round_inst)

        assert frame.stitch_count == 6
        assert len(frame.nodes) == 6

        # Verify node types in order
        expected_types = ["sc", "sc", "inc", "sc", "dec", "sc"]
        actual_types = [node.stitch_type for node in frame.nodes]
        assert actual_types == expected_types

        # Verify only inc and dec are highlighted
        assert len(frame.highlights) == 2
        assert "r3s2" in frame.highlights  # inc
        assert "r3s4" in frame.highlights  # dec

    def test_full_pattern_conversion(self, service, sample_shape, sample_gauge, sample_metadata):
        """Test conversion of complete PatternDSL to frames."""
        pattern = PatternDSL(
            shape=sample_shape,
            gauge=sample_gauge,
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[StitchInstruction(stitch_type="inc", count=6)],
                    total_stitches=12,
                ),
                RoundInstruction(
                    round_number=2,
                    stitches=[
                        StitchInstruction(stitch_type="sc", count=1),
                        StitchInstruction(stitch_type="inc", count=1),
                    ],
                    total_stitches=18,
                ),
            ],
            metadata=sample_metadata,
        )

        frames = service.dsl_to_frames(pattern)

        assert len(frames) == 3
        assert frames[0].stitch_count == 6
        assert frames[1].stitch_count == 12
        assert frames[2].stitch_count == 18

    def test_pattern_to_visualization_response(
        self, service, sample_shape, sample_gauge, sample_metadata
    ):
        """Test high-level pattern_to_visualization method."""
        pattern = PatternDSL(
            shape=sample_shape,
            gauge=sample_gauge,
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                )
            ],
            metadata=sample_metadata,
        )

        response = service.pattern_to_visualization(pattern)

        assert isinstance(response, VisualizationResponse)
        assert response.total_rounds == 1
        assert response.shape_type == "sphere"
        assert len(response.frames) == 1

    def test_node_id_format(self, service):
        """Verify node IDs follow the required format."""
        round_inst = RoundInstruction(
            round_number=10,
            stitches=[StitchInstruction(stitch_type="sc", count=5)],
            total_stitches=5,
        )

        frame = service._round_to_frame(round_inst)

        # Verify ID format: r{round}s{stitch}
        for i, node in enumerate(frame.nodes):
            expected_id = f"r10s{i}"
            assert node.id == expected_id

    def test_position_coordinate_precision(self, service):
        """Verify position coordinates are float tuples."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=3)],
            total_stitches=3,
        )

        frame = service._round_to_frame(round_inst)

        for node in frame.nodes:
            assert isinstance(node.position, tuple)
            assert len(node.position) == 2
            assert isinstance(node.position[0], float)
            assert isinstance(node.position[1], float)

    @pytest.mark.benchmark
    def test_visualization_performance(
        self, service, sample_shape, sample_gauge, sample_metadata, benchmark
    ):
        """Benchmark frame compilation performance."""
        # Create pattern with 50 rounds (typical pattern size)
        rounds = []
        for i in range(50):
            rounds.append(
                RoundInstruction(
                    round_number=i,
                    stitches=[StitchInstruction(stitch_type="sc", count=6 + i)],
                    total_stitches=6 + i,
                )
            )

        pattern = PatternDSL(
            shape=sample_shape, gauge=sample_gauge, rounds=rounds, metadata=sample_metadata
        )

        # Benchmark the conversion
        result = benchmark(service.dsl_to_frames, pattern)

        # Verify result
        assert len(result) == 50

        # Performance requirement: < 100ms for typical patterns
        # pytest-benchmark will report timing statistics

    def test_multiple_stitch_expansion(self, service):
        """Verify stitch instructions with count > 1 expand correctly."""
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[
                StitchInstruction(stitch_type="sc", count=3),
                StitchInstruction(stitch_type="inc", count=2),
            ],
            total_stitches=5,
        )

        frame = service._round_to_frame(round_inst)

        assert len(frame.nodes) == 5

        # First 3 nodes should be "sc"
        for i in range(3):
            assert frame.nodes[i].stitch_type == "sc"
            assert frame.nodes[i].highlight == "normal"

        # Last 2 nodes should be "inc"
        for i in range(3, 5):
            assert frame.nodes[i].stitch_type == "inc"
            assert frame.nodes[i].highlight == "increase"

    def test_round_number_indexing(self, service):
        """Verify round number conversion from 0-indexed to 1-indexed."""
        # DSL uses 0-indexed rounds
        round_inst = RoundInstruction(
            round_number=0,
            stitches=[StitchInstruction(stitch_type="sc", count=6)],
            total_stitches=6,
        )

        frame = service._round_to_frame(round_inst)

        # Visualization uses 1-indexed rounds
        assert frame.round_number == 1

        # Node IDs still use DSL round number (0-indexed)
        assert all(node.id.startswith("r0s") for node in frame.nodes)


class TestVisualizationService3D:
    """Test suite for 3D visualization features."""

    @pytest.fixture
    def service(self):
        """Create VisualizationService instance."""
        return VisualizationService()

    @pytest.fixture
    def sample_gauge(self):
        """Create sample gauge info."""
        return GaugeInfo(
            stitches_per_cm=1.4, rows_per_cm=1.6, hook_size_mm=4.0, yarn_weight="worsted"
        )

    @pytest.fixture
    def sphere_pattern(self, sample_gauge):
        """Create sample sphere pattern."""
        return PatternDSL(
            shape=ShapeParameters(shape_type="sphere", diameter_cm=10.0),
            gauge=sample_gauge,
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=6)],
                    total_stitches=6,
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[StitchInstruction(stitch_type="inc", count=6)],
                    total_stitches=12,
                ),
                RoundInstruction(
                    round_number=2,
                    stitches=[StitchInstruction(stitch_type="sc", count=12)],
                    total_stitches=12,
                ),
            ],
            metadata=PatternMetadata(
                generated_at=datetime.now(),
                engine_version="0.1.0",
                total_rounds=3,
            ),
        )

    @pytest.fixture
    def cylinder_pattern(self, sample_gauge):
        """Create sample cylinder pattern."""
        return PatternDSL(
            shape=ShapeParameters(shape_type="cylinder", diameter_cm=8.0, height_cm=12.0),
            gauge=sample_gauge,
            rounds=[
                RoundInstruction(
                    round_number=0,
                    stitches=[StitchInstruction(stitch_type="sc", count=8)],
                    total_stitches=8,
                ),
                RoundInstruction(
                    round_number=1,
                    stitches=[StitchInstruction(stitch_type="sc", count=8)],
                    total_stitches=8,
                ),
            ],
            metadata=PatternMetadata(
                generated_at=datetime.now(),
                engine_version="0.1.0",
                total_rounds=2,
            ),
        )

    def test_sphere_3d_coordinates_on_surface(self, service):
        """Verify sphere 3D coordinates lie on sphere surface."""
        radius = service.BASE_RADIUS
        total_rounds = 10
        stitch_count = 12

        for round_index in range(total_rounds):
            coords = service._generate_sphere_3d_coordinates(
                round_index, total_rounds, stitch_count
            )

            assert len(coords) == stitch_count

            for x, y, z in coords:
                distance = math.sqrt(x**2 + y**2 + z**2)
                # All points should be on sphere surface
                assert abs(distance - radius) < 0.01

    def test_cylinder_3d_coordinates_constant_radius(self, service):
        """Verify cylinder coordinates maintain constant radius."""
        radius = service.BASE_RADIUS
        stitch_count = 8

        for round_index in range(5):
            coords = service._generate_cylinder_3d_coordinates(round_index, stitch_count)

            assert len(coords) == stitch_count

            for x, y, z in coords:
                radial_distance = math.sqrt(x**2 + y**2)
                # All points should have same radius
                assert abs(radial_distance - radius) < 0.01
                # Z should match round index
                expected_z = round_index * service.BASE_ROW_HEIGHT
                assert abs(z - expected_z) < 0.01

    def test_cone_3d_coordinates_taper(self, service):
        """Verify cone coordinates taper correctly."""
        total_rounds = 10
        stitch_count = 12

        # Get coordinates at different heights
        coords_base = service._generate_cone_3d_coordinates(0, total_rounds, stitch_count)
        coords_mid = service._generate_cone_3d_coordinates(5, total_rounds, stitch_count)
        coords_top = service._generate_cone_3d_coordinates(9, total_rounds, stitch_count)

        # Calculate radii at each level
        def get_radius(coords):
            x, y, z = coords[0]
            return math.sqrt(x**2 + y**2)

        r_base = get_radius(coords_base)
        r_mid = get_radius(coords_mid)
        r_top = get_radius(coords_top)

        # Radius should decrease from base to top
        assert r_base > r_mid > r_top

    def test_3d_frame_has_position_3d(self, service, sphere_pattern):
        """Verify 3D frames have position_3d field populated."""
        frames = service.dsl_to_frames_3d(sphere_pattern)

        for frame in frames:
            for node in frame.nodes:
                # All nodes should have 3D coordinates
                assert node.position_3d is not None
                assert len(node.position_3d) == 3
                assert all(isinstance(coord, float) for coord in node.position_3d)

                # All nodes should have depth ordering
                assert node.depth_order is not None
                assert isinstance(node.depth_order, int)
                assert node.depth_order >= 0

                # All nodes should have depth factor
                assert node.depth_factor is not None
                assert 0.0 <= node.depth_factor <= 1.0

    def test_3d_frame_has_projection_metadata(self, service, sphere_pattern):
        """Verify 3D frames include projection metadata."""
        frames = service.dsl_to_frames_3d(sphere_pattern)

        for frame in frames:
            assert frame.projection is not None
            assert frame.projection.type == "isometric"
            assert frame.projection.angle_deg == 30.0
            assert "x_min" in frame.projection.bounds_3d
            assert "x_max" in frame.projection.bounds_3d
            assert "y_min" in frame.projection.bounds_3d
            assert "y_max" in frame.projection.bounds_3d
            assert "z_min" in frame.projection.bounds_3d
            assert "z_max" in frame.projection.bounds_3d

    def test_depth_ordering_correct(self, service, sphere_pattern):
        """Verify depth_order increases with z-coordinate."""
        frames = service.dsl_to_frames_3d(sphere_pattern)

        # Collect all nodes
        all_nodes = []
        for frame in frames:
            all_nodes.extend(frame.nodes)

        # Sort by depth_order
        sorted_by_depth = sorted(all_nodes, key=lambda n: n.depth_order)

        # Verify z-coordinates are non-decreasing
        for i in range(len(sorted_by_depth) - 1):
            z1 = sorted_by_depth[i].position_3d[2]
            z2 = sorted_by_depth[i + 1].position_3d[2]
            assert z1 <= z2 + 0.01  # Allow small floating point errors

    def test_2d_mode_backward_compatible(self, service, sphere_pattern):
        """Verify 2D mode does not include 3D fields."""
        frames_2d = service.dsl_to_frames(sphere_pattern)

        for frame in frames_2d:
            # Should not have projection metadata
            assert frame.projection is None

            for node in frame.nodes:
                # Should not have 3D fields
                assert node.position_3d is None
                assert node.depth_order is None
                assert node.depth_factor is None

    def test_pattern_to_visualization_3d(self, service, sphere_pattern):
        """Test high-level 3D visualization method."""
        response = service.pattern_to_visualization_3d(sphere_pattern)

        assert isinstance(response, VisualizationResponse)
        assert response.total_rounds == 3
        assert response.shape_type == "sphere"
        assert len(response.frames) == 3

        # Verify all frames have 3D data
        for frame in response.frames:
            assert frame.projection is not None
            assert all(node.position_3d is not None for node in frame.nodes)

    def test_cylinder_3d_coordinates(self, service, cylinder_pattern):
        """Test cylinder-specific 3D coordinate generation."""
        frames = service.dsl_to_frames_3d(cylinder_pattern)

        # Cylinder should stack rounds vertically
        for i, frame in enumerate(frames):
            for node in frame.nodes:
                x, y, z = node.position_3d
                expected_z = i * service.BASE_ROW_HEIGHT
                assert abs(z - expected_z) < 0.01

    def test_depth_factor_normalization(self, service, sphere_pattern):
        """Verify depth_factor is normalized to [0, 1]."""
        frames = service.dsl_to_frames_3d(sphere_pattern)

        # Collect all depth factors
        depth_factors = []
        for frame in frames:
            for node in frame.nodes:
                depth_factors.append(node.depth_factor)

        # Should have at least one near 0 and one near 1
        assert min(depth_factors) < 0.1  # Close to 0
        assert max(depth_factors) > 0.9  # Close to 1

        # All should be in [0, 1]
        assert all(0.0 <= df <= 1.0 for df in depth_factors)

    def test_sphere_north_pole_coordinates(self, service):
        """Verify north pole (first round) has correct z-coordinate."""
        total_rounds = 10
        stitch_count = 6

        coords = service._generate_sphere_3d_coordinates(0, total_rounds, stitch_count)

        # North pole should have z ≈ radius
        z_values = [z for _, _, z in coords]
        expected_z = service.BASE_RADIUS
        assert all(abs(z - expected_z) < 0.01 for z in z_values)

    def test_sphere_south_pole_coordinates(self, service):
        """Verify south pole (last round) has correct z-coordinate."""
        total_rounds = 10
        stitch_count = 6

        coords = service._generate_sphere_3d_coordinates(
            total_rounds - 1, total_rounds, stitch_count
        )

        # South pole should have z ≈ -radius
        z_values = [z for _, _, z in coords]
        expected_z = -service.BASE_RADIUS
        assert all(abs(z - expected_z) < 0.01 for z in z_values)
