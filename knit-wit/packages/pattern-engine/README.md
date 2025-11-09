# Knit-Wit Pattern Engine

A parametric crochet pattern generation library for creating 3D geometric shapes.

## Overview

The Knit-Wit Pattern Engine is a Python library that generates stitch-by-stitch crochet instructions for 3D geometric shapes (spheres, cylinders, cones) based on parametric inputs. It uses gauge measurements and mathematical algorithms to produce accurate, customizable patterns.

## Features

- **Parametric Pattern Generation**: Generate patterns based on physical dimensions and gauge
- **Multiple Shape Support**: Spheres, cylinders, and cones with various customization options
- **Type-Safe DSL**: Pydantic v2-based domain-specific language for pattern representation
- **Gauge Calculations**: Utilities for gauge adjustments and unit conversions
- **JSON Serialization**: Export patterns to JSON for use in web applications

## Installation

### Using uv (Recommended)

```bash
# Install in development mode
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"

# Install with test dependencies only
uv pip install -e ".[test]"
```

### Using pip

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.11 or higher
- NumPy >= 1.24.0
- Pydantic >= 2.0.0

## Quick Start

### Generate a Sphere Pattern

```python
from knit_wit_engine import generate_sphere

pattern = generate_sphere(
    diameter_cm=10.0,
    stitches_per_cm=3.0,
    rows_per_cm=3.5,
    stitch_type="sc"
)

print(pattern)
```

### Generate a Cylinder Pattern

```python
from knit_wit_engine import generate_cylinder

pattern = generate_cylinder(
    diameter_cm=8.0,
    height_cm=12.0,
    stitches_per_cm=3.0,
    rows_per_cm=3.5,
    stitch_type="sc",
    end_type="closed"
)
```

### Generate a Cone Pattern

```python
from knit_wit_engine import generate_cone

pattern = generate_cone(
    base_diameter_cm=10.0,
    top_diameter_cm=5.0,
    height_cm=15.0,
    stitches_per_cm=3.0,
    rows_per_cm=3.5,
    stitch_type="sc"
)
```

### Working with the Pattern DSL

```python
from knit_wit_engine.models import (
    PatternDSL,
    ShapeParameters,
    GaugeInfo,
    RoundInstruction,
    StitchInstruction,
    PatternMetadata
)

# Create a pattern manually
pattern = PatternDSL(
    shape=ShapeParameters(
        shape_type="sphere",
        diameter_cm=10.0
    ),
    gauge=GaugeInfo(
        stitches_per_cm=3.0,
        rows_per_cm=3.5,
        hook_size_mm=4.0,
        yarn_weight="worsted"
    ),
    rounds=[
        RoundInstruction(
            round_number=0,
            stitches=[
                StitchInstruction(
                    stitch_type="sc",
                    count=6,
                    target="magic ring"
                )
            ],
            total_stitches=6,
            description="Magic ring with 6 sc"
        )
    ],
    metadata=PatternMetadata(
        total_rounds=1,
        difficulty="beginner",
        tags=["sphere", "amigurumi"]
    )
)

# Serialize to JSON
json_str = pattern.to_json()
print(json_str)

# Load from JSON
loaded_pattern = PatternDSL.from_json(json_str)
```

### Gauge Utilities

```python
from knit_wit_engine.utils import (
    calculate_gauge_adjustments,
    convert_inches_to_cm,
    estimate_yarn_length
)

# Calculate gauge adjustments
adjustments = calculate_gauge_adjustments(
    target_stitches_per_cm=3.0,
    actual_stitches_per_cm=2.8,
    target_rows_per_cm=3.5,
    actual_rows_per_cm=3.3
)
print(adjustments["recommendation"])

# Convert units
cm = convert_inches_to_cm(4.0)  # 10.16 cm

# Estimate yarn needed
total_meters, formatted = estimate_yarn_length(
    total_stitches=500,
    stitches_per_cm=3.0
)
print(formatted)  # "15.0m (includes 20% buffer)"
```

## Project Structure

```
pattern-engine/
├── knit_wit_engine/           # Main package
│   ├── __init__.py            # Package exports
│   ├── algorithms/            # Pattern generation algorithms
│   │   ├── __init__.py
│   │   ├── sphere.py          # Sphere pattern generation
│   │   ├── cylinder.py        # Cylinder pattern generation
│   │   └── cone.py            # Cone pattern generation
│   ├── models/                # DSL data models
│   │   ├── __init__.py
│   │   └── dsl.py             # Pydantic models for pattern DSL
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── gauge.py           # Gauge calculations and conversions
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_imports.py        # Basic import tests
├── pyproject.toml             # Modern Python packaging config
├── requirements.txt           # Legacy requirements file
└── README.md                  # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=knit_wit_engine --cov-report=html

# Run specific test file
pytest tests/test_imports.py -v
```

### Code Quality

```bash
# Format code with black
black knit_wit_engine tests

# Sort imports with isort
isort knit_wit_engine tests

# Type checking with mypy
mypy knit_wit_engine

# Linting with ruff
ruff check knit_wit_engine tests
```

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd pattern-engine

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
uv pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

## Current Status

**Version**: 0.1.0 (Alpha)

This is the initial scaffold for the pattern engine library. The current implementation includes:

- Complete package structure with proper module organization
- Type-safe Pydantic v2 models for the Pattern DSL
- Stub implementations for all core algorithms (sphere, cylinder, cone)
- Basic gauge calculation utilities
- Comprehensive import tests

### Phase 1 Roadmap

The following features will be implemented in Phase 1:

1. **Complete Algorithm Implementations**
   - Full sphere generation with proper increase/decrease patterns
   - Cylinder generation with flat or rounded ends
   - Cone generation with smooth tapering

2. **Advanced DSL Features**
   - Stitch abbreviation expansion
   - Pattern validation and error checking
   - Multi-language pattern export

3. **Enhanced Utilities**
   - Advanced gauge adjustment recommendations
   - Yarn consumption estimation by stitch type
   - Pattern optimization algorithms

## Contributing

This package is part of the larger Knit-Wit project. For contribution guidelines and development workflow, please refer to the main project documentation.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit the GitHub repository.

## Acknowledgments

Built with:
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type annotations
- [NumPy](https://numpy.org/) - Numerical computing tools
- [pytest](https://pytest.org/) - Testing framework
