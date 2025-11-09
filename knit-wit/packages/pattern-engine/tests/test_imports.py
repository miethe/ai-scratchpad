"""
Basic import tests for the knit-wit-engine package.

These tests ensure that all core modules and functions can be imported successfully,
which is critical for CI/CD validation and package integrity.
"""

import pytest


class TestPackageImports:
    """Test that core package imports work correctly."""

    def test_import_main_package(self) -> None:
        """Test importing the main package."""
        import knit_wit_engine

        assert hasattr(knit_wit_engine, "__version__")
        assert knit_wit_engine.__version__ == "0.1.0"

    def test_import_version(self) -> None:
        """Test importing version information."""
        from knit_wit_engine import __version__

        assert __version__ == "0.1.0"

    def test_import_algorithms(self) -> None:
        """Test importing algorithm modules."""
        from knit_wit_engine import generate_sphere, generate_cylinder, generate_cone
        from knit_wit_engine.algorithms import (
            generate_sphere as gen_sphere,
            generate_cylinder as gen_cylinder,
            generate_cone as gen_cone,
        )

        # Verify functions are callable
        assert callable(generate_sphere)
        assert callable(generate_cylinder)
        assert callable(generate_cone)
        assert callable(gen_sphere)
        assert callable(gen_cylinder)
        assert callable(gen_cone)

    def test_import_models(self) -> None:
        """Test importing DSL models."""
        from knit_wit_engine import PatternDSL, StitchInstruction
        from knit_wit_engine.models import (
            PatternDSL as PatternDSL2,
            StitchInstruction as StitchInstruction2,
            RoundInstruction,
            GaugeInfo,
            ShapeParameters,
            PatternMetadata,
        )

        # Verify all models are importable classes
        assert PatternDSL is not None
        assert StitchInstruction is not None
        assert PatternDSL2 is not None
        assert StitchInstruction2 is not None
        assert RoundInstruction is not None
        assert GaugeInfo is not None
        assert ShapeParameters is not None
        assert PatternMetadata is not None

    def test_import_utils(self) -> None:
        """Test importing utility functions."""
        from knit_wit_engine import calculate_gauge_adjustments
        from knit_wit_engine.utils import (
            calculate_gauge_adjustments as calc_gauge,
            convert_inches_to_cm,
            convert_cm_to_inches,
            estimate_yarn_length,
        )

        # Verify functions are callable
        assert callable(calculate_gauge_adjustments)
        assert callable(calc_gauge)
        assert callable(convert_inches_to_cm)
        assert callable(convert_cm_to_inches)
        assert callable(estimate_yarn_length)


class TestModuleStructure:
    """Test the module structure and exports."""

    def test_main_package_exports(self) -> None:
        """Test that main package exports expected symbols."""
        import knit_wit_engine

        expected_exports = [
            "__version__",
            "generate_sphere",
            "generate_cylinder",
            "generate_cone",
            "PatternDSL",
            "StitchInstruction",
            "calculate_gauge_adjustments",
        ]

        for export in expected_exports:
            assert hasattr(knit_wit_engine, export), f"Missing export: {export}"

    def test_algorithms_module_exports(self) -> None:
        """Test that algorithms module exports expected functions."""
        from knit_wit_engine import algorithms

        expected_exports = ["generate_sphere", "generate_cylinder", "generate_cone"]

        for export in expected_exports:
            assert hasattr(algorithms, export), f"Missing export: {export}"

    def test_models_module_exports(self) -> None:
        """Test that models module exports expected classes."""
        from knit_wit_engine import models

        expected_exports = [
            "PatternDSL",
            "StitchInstruction",
            "RoundInstruction",
            "GaugeInfo",
            "ShapeParameters",
            "PatternMetadata",
        ]

        for export in expected_exports:
            assert hasattr(models, export), f"Missing export: {export}"

    def test_utils_module_exports(self) -> None:
        """Test that utils module exports expected functions."""
        from knit_wit_engine import utils

        expected_exports = [
            "calculate_gauge_adjustments",
            "convert_inches_to_cm",
            "convert_cm_to_inches",
            "estimate_yarn_length",
        ]

        for export in expected_exports:
            assert hasattr(utils, export), f"Missing export: {export}"


class TestBasicFunctionality:
    """Test basic functionality of stub implementations."""

    def test_unit_conversions(self) -> None:
        """Test basic unit conversion utilities."""
        from knit_wit_engine.utils import convert_inches_to_cm, convert_cm_to_inches

        # Test inch to cm
        assert abs(convert_inches_to_cm(1.0) - 2.54) < 0.01
        assert abs(convert_inches_to_cm(10.0) - 25.4) < 0.01

        # Test cm to inch
        assert abs(convert_cm_to_inches(2.54) - 1.0) < 0.01
        assert abs(convert_cm_to_inches(25.4) - 10.0) < 0.01

        # Test round-trip conversion
        original_cm = 15.0
        converted = convert_cm_to_inches(original_cm)
        back_to_cm = convert_inches_to_cm(converted)
        assert abs(back_to_cm - original_cm) < 0.01

    def test_gauge_adjustments(self) -> None:
        """Test gauge adjustment calculations."""
        from knit_wit_engine.utils import calculate_gauge_adjustments

        result = calculate_gauge_adjustments(3.0, 2.8, 3.5, 3.3)

        assert "stitch_adjustment_factor" in result
        assert "row_adjustment_factor" in result
        assert "recommendation" in result
        assert isinstance(result["stitch_adjustment_factor"], float)
        assert isinstance(result["row_adjustment_factor"], float)
        assert isinstance(result["recommendation"], str)

    def test_sphere_stub(self) -> None:
        """Test sphere generation stub returns expected structure."""
        from knit_wit_engine.algorithms import generate_sphere

        result = generate_sphere(
            diameter_cm=10.0, stitches_per_cm=3.0, rows_per_cm=3.5
        )

        assert result["shape"] == "sphere"
        assert "parameters" in result
        assert "rounds" in result
        assert "metadata" in result
        assert isinstance(result["rounds"], list)
        assert len(result["rounds"]) > 0

    def test_cylinder_stub(self) -> None:
        """Test cylinder generation stub returns expected structure."""
        from knit_wit_engine.algorithms import generate_cylinder

        result = generate_cylinder(
            diameter_cm=8.0, height_cm=12.0, stitches_per_cm=3.0, rows_per_cm=3.5
        )

        assert result["shape"] == "cylinder"
        assert "parameters" in result
        assert "rounds" in result
        assert "metadata" in result

    def test_cone_stub(self) -> None:
        """Test cone generation stub returns expected structure."""
        from knit_wit_engine.algorithms import generate_cone

        result = generate_cone(
            base_diameter_cm=10.0,
            top_diameter_cm=5.0,
            height_cm=15.0,
            stitches_per_cm=3.0,
            rows_per_cm=3.5,
        )

        assert result["shape"] == "cone"
        assert "parameters" in result
        assert "rounds" in result
        assert "metadata" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
