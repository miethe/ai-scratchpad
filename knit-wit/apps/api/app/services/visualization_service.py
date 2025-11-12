"""
Visualization Service for Knit-Wit

Converts PatternDSL to frame-by-frame visualization primitives using circular layout.
Implements polar-to-Cartesian coordinate conversion for even stitch distribution.
"""

import math
from typing import List

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
)


class VisualizationService:
    """
    Service for converting PatternDSL to visualization primitives.

    Implements circular layout algorithm using polar coordinates:
    - angle = (2π / stitch_count) * index
    - x = radius * cos(angle)
    - y = radius * sin(angle)

    Architecture:
    - dsl_to_frames(): Main entry point, converts entire pattern
    - _round_to_frame(): Converts single round using circular layout
    - _generate_nodes(): Creates positioned nodes from stitch instructions
    - _generate_edges(): Creates consecutive + closing edges
    """

    BASE_RADIUS = 100.0  # Arbitrary units, frontend scales to viewport

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

        angle_step = (2 * math.pi) / stitch_count

        for stitch_inst in round_inst.stitches:
            stitch_type = stitch_inst.stitch_type
            count = stitch_inst.count

            # Expand each stitch instruction into individual nodes
            for _ in range(count):
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
