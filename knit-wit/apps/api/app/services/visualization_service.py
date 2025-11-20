"""
Visualization Service for Knit-Wit

Converts PatternDSL to frame-by-frame visualization primitives using circular layout.
Implements polar-to-Cartesian coordinate conversion for even stitch distribution.
Supports 3D coordinate generation for isometric projection visualization.
"""

import math
from typing import List, Tuple, Dict, Literal, Optional

# Import from knit_wit_engine package
import sys
from pathlib import Path

# Add pattern-engine to Python path for imports
pattern_engine_path = (
    Path(__file__).parent.parent.parent.parent.parent / "packages" / "pattern-engine"
)
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import PatternDSL, RoundInstruction, StitchInstruction

from app.models.visualization import (
    RenderNode,
    RenderEdge,
    VisualizationFrame,
    VisualizationResponse,
    ProjectionMetadata,
)


class VisualizationService:
    """
    Service for converting PatternDSL to visualization primitives.

    Implements circular layout algorithm using polar coordinates:
    - angle = (2π / stitch_count) * index
    - x = radius * cos(angle)
    - y = radius * sin(angle)

    For 3D mode, generates shape-aware 3D coordinates:
    - Sphere: Spherical coordinates (latitude/longitude)
    - Cylinder: Cylindrical stacking with constant radius
    - Cone: Tapered cylindrical with linear radius interpolation

    Architecture:
    - dsl_to_frames(): Main entry point, converts entire pattern (2D)
    - dsl_to_frames_3d(): 3D mode entry point with depth ordering
    - _round_to_frame(): Converts single round using circular layout
    - _generate_nodes(): Creates positioned nodes from stitch instructions
    - _generate_nodes_3d(): Creates nodes with 3D coordinates
    - _generate_edges(): Creates consecutive + closing edges
    - _generate_*_3d_coordinates(): Shape-specific 3D coordinate generators
    """

    BASE_RADIUS = 100.0  # Arbitrary units, frontend scales to viewport
    BASE_ROW_HEIGHT = 10.0  # Height between rounds for cylinder/cone

    def dsl_to_frames(self, pattern: PatternDSL) -> List[VisualizationFrame]:
        """
        Convert complete PatternDSL to list of visualization frames.

        Args:
            pattern: PatternDSL instance from pattern engine

        Returns:
            List of VisualizationFrame, one per round

        Example:
            >>> pattern = PatternDSL(...)
            >>> service = VisualizationService()
            >>> frames = service.dsl_to_frames(pattern)
            >>> len(frames) == len(pattern.rounds)
            True
        """
        frames: List[VisualizationFrame] = []

        for round_inst in pattern.rounds:
            frame = self._round_to_frame(round_inst)
            frames.append(frame)

        return frames

    def _round_to_frame(self, round_inst: RoundInstruction) -> VisualizationFrame:
        """
        Convert single round to visualization frame using circular layout.

        Algorithm:
        1. Compute circular layout using polar coordinates
        2. Generate positioned nodes from stitch instructions
        3. Generate edges connecting consecutive nodes
        4. Identify highlighted nodes (increases/decreases)

        Args:
            round_inst: RoundInstruction from PatternDSL

        Returns:
            VisualizationFrame with positioned nodes and edges
        """
        stitch_count = round_inst.total_stitches

        # Generate nodes with circular positioning
        nodes = self._generate_nodes(round_inst, stitch_count)

        # Generate edges (consecutive + closing)
        edges = self._generate_edges(nodes)

        # Identify highlights
        highlights = [node.id for node in nodes if node.highlight != "normal"]

        return VisualizationFrame(
            round_number=round_inst.round_number
            + 1,  # DSL is 0-indexed, visualization is 1-indexed
            nodes=nodes,
            edges=edges,
            stitch_count=stitch_count,
            highlights=highlights,
        )

    def _generate_nodes(self, round_inst: RoundInstruction, stitch_count: int) -> List[RenderNode]:
        """
        Generate positioned nodes from stitch instructions.

        Uses circular layout with even angular distribution:
        - angle_step = 2π / stitch_count
        - position = (radius * cos(angle), radius * sin(angle))

        Args:
            round_inst: RoundInstruction with stitch operations
            stitch_count: Total stitches in round

        Returns:
            List of RenderNode with positions and highlights
        """
        nodes: List[RenderNode] = []
        stitch_idx = 0

        # Handle empty round edge case
        if stitch_count == 0:
            return nodes

        # Validate that stitch instructions match total stitch count
        # Note: Ch is always foundation (0 stitches)
        # Note: MR(count=1) is foundation (0 stitches), MR(count>1) produces count stitches
        # Note: Inc operations produce 2 stitches per operation, dec produces 1
        foundation_stitches = {"Ch", "ch"}
        actual_stitch_count = 0
        for s in round_inst.stitches:
            if s.stitch_type in foundation_stitches:
                continue  # Skip chain foundation stitches
            elif s.stitch_type in {"MR", "mr"}:
                # Magic ring: count > 1 produces stitches, count == 1 is foundation
                if s.count > 1:
                    actual_stitch_count += s.count
                # else: MR(count=1) is foundation, add 0
            elif s.stitch_type.lower() == "inc":
                # Increase: 1 operation produces 2 stitches
                actual_stitch_count += s.count * 2
            elif s.stitch_type.lower() == "dec":
                # Decrease: 1 operation produces 1 stitch (consumes 2)
                actual_stitch_count += s.count * 1
            else:
                # Regular stitches: 1 operation = 1 stitch
                actual_stitch_count += s.count

        if actual_stitch_count != stitch_count:
            # Include diagnostic info in error message
            stitch_breakdown = ", ".join(
                f"{s.stitch_type}({s.count})" for s in round_inst.stitches
            )
            raise ValueError(
                f"Stitch count mismatch in round {round_inst.round_number}: "
                f"total_stitches={stitch_count}, but calculated stitch count={actual_stitch_count}. "
                f"Stitches: [{stitch_breakdown}]"
            )

        angle_step = (2 * math.pi) / stitch_count

        for stitch_inst in round_inst.stitches:
            stitch_type = stitch_inst.stitch_type
            count = stitch_inst.count

            # Skip chain foundation stitches - they don't produce nodes
            # Note: MR(count=1) is foundation and skipped, MR(count>1) produces nodes
            if stitch_type in foundation_stitches:
                continue
            elif stitch_type in {"MR", "mr"} and count <= 1:
                continue  # Skip MR foundation (count=1)

            # Expand each stitch instruction into individual nodes
            for _ in range(count):
                # Defensive check
                if stitch_idx >= stitch_count:
                    raise IndexError(
                        f"Index out of range in round {round_inst.round_number}: "
                        f"stitch_idx={stitch_idx}, stitch_count={stitch_count}"
                    )

                # Compute polar coordinates
                angle = stitch_idx * angle_step

                # Convert to Cartesian
                x = self.BASE_RADIUS * math.cos(angle)
                y = self.BASE_RADIUS * math.sin(angle)

                # Determine highlight based on stitch type
                highlight = self._get_highlight(stitch_type)

                node = RenderNode(
                    id=f"r{round_inst.round_number}s{stitch_idx}",
                    stitch_type=stitch_type,
                    position=(x, y),
                    highlight=highlight,
                )

                nodes.append(node)
                stitch_idx += 1

        return nodes

    def _generate_edges(self, nodes: List[RenderNode]) -> List[RenderEdge]:
        """
        Generate edges connecting consecutive nodes.

        Creates:
        - Consecutive edges: node[i] → node[i+1]
        - Closing edge: node[-1] → node[0]

        Args:
            nodes: List of positioned nodes

        Returns:
            List of RenderEdge forming closed loop
        """
        edges: List[RenderEdge] = []

        if len(nodes) == 0:
            return edges

        # Consecutive edges
        for i in range(len(nodes) - 1):
            edge = RenderEdge(source=nodes[i].id, target=nodes[i + 1].id)
            edges.append(edge)

        # Closing edge (connect last to first)
        if len(nodes) > 0:
            closing_edge = RenderEdge(source=nodes[-1].id, target=nodes[0].id)
            edges.append(closing_edge)

        return edges

    def _get_highlight(self, stitch_type: str) -> str:
        """
        Determine highlight mode based on stitch type.

        Rules:
        - "inc" → "increase"
        - "dec" → "decrease"
        - All others → "normal"

        Args:
            stitch_type: Stitch operation type

        Returns:
            Highlight mode: "normal", "increase", or "decrease"
        """
        if stitch_type == "inc":
            return "increase"
        elif stitch_type == "dec":
            return "decrease"
        else:
            return "normal"

    def pattern_to_visualization(self, pattern: PatternDSL) -> VisualizationResponse:
        """
        Convert PatternDSL to complete VisualizationResponse.

        High-level convenience method that wraps dsl_to_frames() and
        adds metadata from pattern.

        Args:
            pattern: PatternDSL instance

        Returns:
            VisualizationResponse ready for API serialization
        """
        frames = self.dsl_to_frames(pattern)

        return VisualizationResponse(
            frames=frames, total_rounds=len(frames), shape_type=pattern.shape.shape_type
        )

    # ========== 3D Visualization Methods ==========

    def dsl_to_frames_3d(self, pattern: PatternDSL) -> List[VisualizationFrame]:
        """
        Convert complete PatternDSL to list of 3D visualization frames.

        Generates 3D coordinates based on shape type and applies depth ordering
        using painter's algorithm for correct occlusion handling.

        Args:
            pattern: PatternDSL instance from pattern engine

        Returns:
            List of VisualizationFrame with 3D coordinates and projection metadata
        """
        frames: List[VisualizationFrame] = []
        total_rounds = len(pattern.rounds)
        shape_type = pattern.shape.shape_type

        # Collect all nodes across all rounds for global depth ordering
        all_nodes_3d: List[Tuple[RenderNode, int]] = []  # (node, frame_idx)

        for round_idx, round_inst in enumerate(pattern.rounds):
            frame = self._round_to_frame_3d(
                round_inst, round_idx, total_rounds, shape_type
            )
            frames.append(frame)

            # Collect nodes with frame index for global depth sorting
            for node in frame.nodes:
                all_nodes_3d.append((node, round_idx))

        # Apply global depth ordering across all frames
        self._apply_depth_ordering(all_nodes_3d)

        # Calculate 3D bounding box
        bounds_3d = self._calculate_bounds_3d(pattern.shape)

        # Add projection metadata to all frames
        projection = ProjectionMetadata(
            type="isometric", angle_deg=30.0, bounds_3d=bounds_3d
        )

        for frame in frames:
            frame.projection = projection

        return frames

    def _round_to_frame_3d(
        self,
        round_inst: RoundInstruction,
        round_index: int,
        total_rounds: int,
        shape_type: str,
    ) -> VisualizationFrame:
        """
        Convert single round to 3D visualization frame.

        Generates both 2D (for backward compatibility) and 3D coordinates.
        3D coordinates are shape-aware (sphere, cylinder, cone).

        Args:
            round_inst: RoundInstruction from PatternDSL
            round_index: Current round (0-indexed)
            total_rounds: Total rounds in pattern
            shape_type: Shape type ("sphere", "cylinder", "cone")

        Returns:
            VisualizationFrame with 3D coordinates
        """
        stitch_count = round_inst.total_stitches

        # Generate nodes with both 2D and 3D coordinates
        nodes = self._generate_nodes_3d(
            round_inst, round_index, total_rounds, stitch_count, shape_type
        )

        # Generate edges (same as 2D)
        edges = self._generate_edges(nodes)

        # Identify highlights
        highlights = [node.id for node in nodes if node.highlight != "normal"]

        return VisualizationFrame(
            round_number=round_inst.round_number + 1,
            nodes=nodes,
            edges=edges,
            stitch_count=stitch_count,
            highlights=highlights,
            projection=None,  # Will be added later with global bounds
        )

    def _generate_nodes_3d(
        self,
        round_inst: RoundInstruction,
        round_index: int,
        total_rounds: int,
        stitch_count: int,
        shape_type: str,
    ) -> List[RenderNode]:
        """
        Generate nodes with both 2D and 3D coordinates.

        2D coordinates use circular layout (same as existing visualization).
        3D coordinates are generated based on shape type.

        Args:
            round_inst: RoundInstruction with stitch operations
            round_index: Current round (0-indexed)
            total_rounds: Total rounds in pattern
            stitch_count: Total stitches in round
            shape_type: Shape type ("sphere", "cylinder", "cone")

        Returns:
            List of RenderNode with position_3d populated
        """
        nodes: List[RenderNode] = []

        if stitch_count == 0:
            return nodes

        # Validate that stitch instructions match total stitch count
        # Note: Ch is always foundation (0 stitches)
        # Note: MR(count=1) is foundation (0 stitches), MR(count>1) produces count stitches
        # Note: Inc operations produce 2 stitches per operation, dec produces 1
        foundation_stitches = {"Ch", "ch"}
        actual_stitch_count = 0
        for s in round_inst.stitches:
            if s.stitch_type in foundation_stitches:
                continue  # Skip chain foundation stitches
            elif s.stitch_type in {"MR", "mr"}:
                # Magic ring: count > 1 produces stitches, count == 1 is foundation
                if s.count > 1:
                    actual_stitch_count += s.count
                # else: MR(count=1) is foundation, add 0
            elif s.stitch_type.lower() == "inc":
                # Increase: 1 operation produces 2 stitches
                actual_stitch_count += s.count * 2
            elif s.stitch_type.lower() == "dec":
                # Decrease: 1 operation produces 1 stitch (consumes 2)
                actual_stitch_count += s.count * 1
            else:
                # Regular stitches: 1 operation = 1 stitch
                actual_stitch_count += s.count

        if actual_stitch_count != stitch_count:
            # Include diagnostic info in error message
            stitch_breakdown = ", ".join(
                f"{s.stitch_type}({s.count})" for s in round_inst.stitches
            )
            raise ValueError(
                f"Stitch count mismatch in round {round_inst.round_number}: "
                f"total_stitches={stitch_count}, but calculated stitch count={actual_stitch_count}. "
                f"Stitches: [{stitch_breakdown}]"
            )

        # Generate 3D coordinates based on shape type
        coordinates_3d = self._generate_shape_3d_coordinates(
            round_inst, round_index, total_rounds, stitch_count, shape_type
        )

        # Validate coordinates list length
        if len(coordinates_3d) != stitch_count:
            raise ValueError(
                f"3D coordinate count mismatch in round {round_inst.round_number}: "
                f"expected {stitch_count} coordinates, got {len(coordinates_3d)}"
            )

        angle_step = (2 * math.pi) / stitch_count
        stitch_idx = 0

        for stitch_inst in round_inst.stitches:
            stitch_type = stitch_inst.stitch_type
            count = stitch_inst.count

            # Skip chain foundation stitches - they don't produce nodes
            # Note: MR(count=1) is foundation and skipped, MR(count>1) produces nodes
            if stitch_type in foundation_stitches:
                continue
            elif stitch_type in {"MR", "mr"} and count <= 1:
                continue  # Skip MR foundation (count=1)

            for _ in range(count):
                # Defensive check to prevent index out of range
                if stitch_idx >= len(coordinates_3d):
                    raise IndexError(
                        f"Index out of range in round {round_inst.round_number}: "
                        f"stitch_idx={stitch_idx}, coordinates_3d length={len(coordinates_3d)}, "
                        f"stitch_count={stitch_count}"
                    )

                # 2D coordinates (polar → Cartesian)
                angle = stitch_idx * angle_step
                x_2d = self.BASE_RADIUS * math.cos(angle)
                y_2d = self.BASE_RADIUS * math.sin(angle)

                # 3D coordinates from shape-specific generator
                x_3d, y_3d, z_3d = coordinates_3d[stitch_idx]

                # Determine highlight
                highlight = self._get_highlight(stitch_type)

                node = RenderNode(
                    id=f"r{round_inst.round_number}s{stitch_idx}",
                    stitch_type=stitch_type,
                    position=(x_2d, y_2d),
                    highlight=highlight,
                    position_3d=(x_3d, y_3d, z_3d),
                    depth_order=None,  # Will be set during global depth sorting
                    depth_factor=None,  # Will be set during global depth sorting
                )

                nodes.append(node)
                stitch_idx += 1

        return nodes

    def _generate_shape_3d_coordinates(
        self,
        round_inst: RoundInstruction,
        round_index: int,
        total_rounds: int,
        stitch_count: int,
        shape_type: str,
    ) -> List[Tuple[float, float, float]]:
        """
        Generate 3D coordinates based on shape type.

        Delegates to shape-specific generators.

        Args:
            round_inst: Round instruction
            round_index: Current round (0-indexed)
            total_rounds: Total rounds in pattern
            stitch_count: Stitches in this round
            shape_type: Shape type ("sphere", "cylinder", "cone")

        Returns:
            List of (x, y, z) coordinates for each stitch
        """
        if shape_type == "sphere":
            return self._generate_sphere_3d_coordinates(
                round_index, total_rounds, stitch_count
            )
        elif shape_type == "cylinder":
            return self._generate_cylinder_3d_coordinates(round_index, stitch_count)
        elif shape_type == "cone":
            return self._generate_cone_3d_coordinates(
                round_index, total_rounds, stitch_count
            )
        else:
            # Fallback to flat circular layout
            return [(self.BASE_RADIUS * math.cos(i * 2 * math.pi / stitch_count),
                     self.BASE_RADIUS * math.sin(i * 2 * math.pi / stitch_count),
                     0.0) for i in range(stitch_count)]

    def _generate_sphere_3d_coordinates(
        self, round_index: int, total_rounds: int, stitch_count: int
    ) -> List[Tuple[float, float, float]]:
        """
        Generate 3D coordinates for sphere using spherical coordinates.

        Algorithm:
        - Latitude angle θ = (round_index / (total_rounds - 1)) * π
        - For each stitch: longitude angle φ = (stitch_index / stitch_count) * 2π
        - Convert to Cartesian: x = r*sin(θ)*cos(φ), y = r*sin(θ)*sin(φ), z = r*cos(θ)

        Args:
            round_index: Current round (0-indexed)
            total_rounds: Total rounds in pattern
            stitch_count: Stitches in this round

        Returns:
            List of (x, y, z) coordinates
        """
        radius = self.BASE_RADIUS

        # Latitude angle (0 = north pole, π = south pole)
        # Handle edge case: single round
        if total_rounds == 1:
            theta = math.pi / 2  # Equator
        else:
            theta = (round_index / (total_rounds - 1)) * math.pi

        # Radius at this latitude (circular cross-section)
        r_cross_section = radius * math.sin(theta)

        # Height (z-coordinate)
        z = radius * math.cos(theta)

        coordinates = []
        for stitch_idx in range(stitch_count):
            # Longitude angle
            phi = (stitch_idx / stitch_count) * 2 * math.pi

            # Spherical to Cartesian
            x = r_cross_section * math.cos(phi)
            y = r_cross_section * math.sin(phi)

            coordinates.append((x, y, z))

        return coordinates

    def _generate_cylinder_3d_coordinates(
        self, round_index: int, stitch_count: int
    ) -> List[Tuple[float, float, float]]:
        """
        Generate 3D coordinates for cylinder.

        Algorithm:
        - Each round is a circle at height z = round_index * row_height
        - Constant radius for all rounds
        - x = radius * cos(φ), y = radius * sin(φ)

        Args:
            round_index: Current round (0-indexed)
            stitch_count: Stitches in this round

        Returns:
            List of (x, y, z) coordinates
        """
        radius = self.BASE_RADIUS
        z = round_index * self.BASE_ROW_HEIGHT

        coordinates = []
        for stitch_idx in range(stitch_count):
            phi = (stitch_idx / stitch_count) * 2 * math.pi

            x = radius * math.cos(phi)
            y = radius * math.sin(phi)

            coordinates.append((x, y, z))

        return coordinates

    def _generate_cone_3d_coordinates(
        self, round_index: int, total_rounds: int, stitch_count: int
    ) -> List[Tuple[float, float, float]]:
        """
        Generate 3D coordinates for cone (tapered cylinder).

        Algorithm:
        - Linear radius taper from base to tip
        - r(z) = r_base - (r_base - r_tip) * (z / height)
        - For simplicity: r_tip = r_base * 0.2 (80% taper)

        Args:
            round_index: Current round (0-indexed)
            total_rounds: Total rounds in pattern
            stitch_count: Stitches in this round

        Returns:
            List of (x, y, z) coordinates
        """
        r_base = self.BASE_RADIUS
        r_tip = r_base * 0.2  # 80% taper
        total_height = (total_rounds - 1) * self.BASE_ROW_HEIGHT

        # Height at this round
        z = round_index * self.BASE_ROW_HEIGHT

        # Radius at this height (linear interpolation)
        if total_height > 0:
            r = r_base - (r_base - r_tip) * (z / total_height)
        else:
            r = r_base

        coordinates = []
        for stitch_idx in range(stitch_count):
            phi = (stitch_idx / stitch_count) * 2 * math.pi

            x = r * math.cos(phi)
            y = r * math.sin(phi)

            coordinates.append((x, y, z))

        return coordinates

    def _apply_depth_ordering(
        self, all_nodes_3d: List[Tuple[RenderNode, int]]
    ) -> None:
        """
        Apply depth ordering using painter's algorithm.

        Sorts nodes by z-coordinate (ascending = back to front) and assigns
        depth_order and depth_factor for rendering.

        Args:
            all_nodes_3d: List of (node, frame_index) tuples

        Modifies nodes in-place to set depth_order and depth_factor.
        """
        # Sort by z-coordinate (ascending: back to front)
        sorted_nodes = sorted(
            all_nodes_3d,
            key=lambda item: item[0].position_3d[2] if item[0].position_3d else 0,
        )

        # Calculate z-range for normalization
        z_values = [
            node.position_3d[2] for node, _ in sorted_nodes if node.position_3d
        ]
        if z_values:
            z_min = min(z_values)
            z_max = max(z_values)
            z_range = z_max - z_min if z_max > z_min else 1.0
        else:
            z_min = 0.0
            z_range = 1.0

        # Assign depth_order and depth_factor
        for depth_order, (node, _) in enumerate(sorted_nodes):
            node.depth_order = depth_order

            # Normalized depth factor (0 = far, 1 = near)
            if node.position_3d:
                z = node.position_3d[2]
                node.depth_factor = (z - z_min) / z_range

    def _calculate_bounds_3d(self, shape_params) -> Dict[str, float]:
        """
        Calculate 3D bounding box based on shape type.

        For geometric shapes, bounds can be computed analytically.

        Args:
            shape_params: ShapeParameters from PatternDSL

        Returns:
            Dictionary with x_min, x_max, y_min, y_max, z_min, z_max
        """
        shape_type = shape_params.shape_type
        radius = self.BASE_RADIUS

        if shape_type == "sphere":
            return {
                "x_min": -radius,
                "x_max": radius,
                "y_min": -radius,
                "y_max": radius,
                "z_min": -radius,
                "z_max": radius,
            }
        elif shape_type == "cylinder":
            # Assume reasonable number of rounds (will be accurate enough)
            height = 20 * self.BASE_ROW_HEIGHT  # Estimate
            return {
                "x_min": -radius,
                "x_max": radius,
                "y_min": -radius,
                "y_max": radius,
                "z_min": 0.0,
                "z_max": height,
            }
        elif shape_type == "cone":
            height = 20 * self.BASE_ROW_HEIGHT  # Estimate
            return {
                "x_min": -radius,
                "x_max": radius,
                "y_min": -radius,
                "y_max": radius,
                "z_min": 0.0,
                "z_max": height,
            }
        else:
            # Default bounds
            return {
                "x_min": -radius,
                "x_max": radius,
                "y_min": -radius,
                "y_max": radius,
                "z_min": -radius,
                "z_max": radius,
            }

    def pattern_to_visualization_3d(self, pattern: PatternDSL) -> VisualizationResponse:
        """
        Convert PatternDSL to complete VisualizationResponse with 3D coordinates.

        High-level convenience method for 3D visualization.

        Args:
            pattern: PatternDSL instance

        Returns:
            VisualizationResponse with 3D frames
        """
        frames = self.dsl_to_frames_3d(pattern)

        return VisualizationResponse(
            frames=frames, total_rounds=len(frames), shape_type=pattern.shape.shape_type
        )
