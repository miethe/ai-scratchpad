# Knit-Wit Pattern DSL Specification v0.1

## Overview

The Knit-Wit Pattern Domain-Specific Language (DSL) is a JSON-based format for representing crochet patterns in a structured, machine-readable way. This specification defines the complete data model for patterns that can be generated, visualized, and exported by the Knit-Wit application.

## Design Goals

- **Type Safety**: Strong typing on both backend (Pydantic) and frontend (TypeScript)
- **Human Readable**: JSON format that can be manually inspected and understood
- **Validation**: Built-in constraints and validation rules
- **Extensibility**: Designed to support future stitch types and shape variants
- **Interoperability**: Clean API boundary between pattern engine and visualization

## Schema Files

- **JSON Schema**: `docs/dsl-schema.json` - JSON Schema Draft 7 specification
- **Pydantic Models**: `packages/pattern-engine/knit_wit_engine/models/dsl.py` - Python data models
- **TypeScript Types**: `apps/mobile/src/types/dsl.ts` - Frontend type definitions
- **Examples**: `docs/examples/` - Sample valid patterns

## Data Model

### PatternDSL (Root Object)

The top-level container for a complete crochet pattern.

```typescript
interface PatternDSL {
  shape: ShapeParameters;
  gauge: GaugeInfo;
  rounds: RoundInstruction[];
  metadata: PatternMetadata;
  notes?: string | null;
}
```

**Required Fields**:
- `shape`: 3D shape parameters
- `gauge`: Gauge and yarn information
- `rounds`: Round-by-round instructions (minimum 1)
- `metadata`: Generation metadata

**Optional Fields**:
- `notes`: General pattern notes and instructions

**Validation Rules**:
- Must have at least one round
- Round numbers must be sequential starting from 0

---

### ShapeParameters

Defines the 3D shape type and dimensions.

```typescript
interface ShapeParameters {
  shape_type: 'sphere' | 'cylinder' | 'cone';
  diameter_cm?: number | null;       // For sphere, cylinder
  height_cm?: number | null;         // For cylinder, cone
  base_diameter_cm?: number | null;  // For cone
  top_diameter_cm?: number | null;   // For cone
}
```

**Required Fields**:
- `shape_type`: Must be one of: `sphere`, `cylinder`, `cone`

**Shape-Specific Requirements**:

| Shape Type | Required Parameters |
|------------|---------------------|
| `sphere` | `diameter_cm` |
| `cylinder` | `diameter_cm`, `height_cm` |
| `cone` | `base_diameter_cm`, `top_diameter_cm`, `height_cm` |

**Validation Rules**:
- All dimension values must be > 0
- Required parameters depend on `shape_type`

**Examples**:

```json
// Sphere
{
  "shape_type": "sphere",
  "diameter_cm": 10.0
}

// Cylinder
{
  "shape_type": "cylinder",
  "diameter_cm": 8.0,
  "height_cm": 12.0
}

// Cone
{
  "shape_type": "cone",
  "base_diameter_cm": 12.0,
  "top_diameter_cm": 4.0,
  "height_cm": 15.0
}
```

---

### GaugeInfo

Gauge information determining the relationship between physical dimensions and stitch counts.

```typescript
interface GaugeInfo {
  stitches_per_cm: number;
  rows_per_cm: number;
  hook_size_mm?: number | null;
  yarn_weight?: YarnWeight | null;
  swatch_notes?: string | null;
}

type YarnWeight = 'lace' | 'fingering' | 'sport' | 'DK' | 'worsted' | 'bulky' | 'super_bulky';
```

**Required Fields**:
- `stitches_per_cm`: Must be > 0
- `rows_per_cm`: Must be > 0

**Optional Fields**:
- `hook_size_mm`: Recommended hook size in millimeters (> 0)
- `yarn_weight`: Yarn weight category
- `swatch_notes`: Additional gauge notes

**Validation Rules**:
- `stitches_per_cm` and `rows_per_cm` must be positive numbers
- `hook_size_mm` must be positive if provided
- `yarn_weight` must be from predefined list

**Example**:

```json
{
  "stitches_per_cm": 1.4,
  "rows_per_cm": 1.6,
  "hook_size_mm": 4.0,
  "yarn_weight": "worsted",
  "swatch_notes": "Worked in single crochet with worsted weight yarn"
}
```

---

### RoundInstruction

Complete instruction for a single round (row) in the pattern.

```typescript
interface RoundInstruction {
  round_number: number;
  stitches: StitchInstruction[];
  total_stitches: number;
  description?: string | null;
}
```

**Required Fields**:
- `round_number`: 0-indexed round number (>= 0)
- `stitches`: Array of stitch instructions (minimum 1)
- `total_stitches`: Total stitch count after round (>= 1)

**Optional Fields**:
- `description`: Human-readable round description

**Validation Rules**:
- `round_number` must be >= 0
- `stitches` array must not be empty
- `total_stitches` must be >= 1
- Round numbers must be sequential across the pattern

**Example**:

```json
{
  "round_number": 2,
  "stitches": [
    {
      "stitch_type": "sc",
      "count": 1,
      "target": "next st"
    },
    {
      "stitch_type": "inc",
      "count": 1,
      "target": "next st"
    }
  ],
  "total_stitches": 18,
  "description": "[sc, inc] around (18)"
}
```

---

### StitchInstruction

A single stitch operation within a round.

```typescript
interface StitchInstruction {
  stitch_type: string;
  count: number;
  target?: string | null;
  note?: string | null;
}
```

**Required Fields**:
- `stitch_type`: Type of stitch (e.g., `sc`, `inc`, `dec`, `hdc`, `dc`)

**Optional Fields**:
- `count`: Number of repetitions (default: 1, must be >= 1)
- `target`: Where to place the stitch (e.g., "next st", "same st")
- `note`: Additional clarification

**Common Stitch Types** (MVP):
- `ch`: Chain
- `sc`: Single crochet
- `inc`: Increase (2 sc in same stitch)
- `dec`: Decrease (sc2tog)
- `slst`: Slip stitch

**Validation Rules**:
- `count` must be >= 1
- `stitch_type` is required

**Examples**:

```json
// Simple stitch
{
  "stitch_type": "sc",
  "count": 6,
  "target": "each st"
}

// Increase with note
{
  "stitch_type": "inc",
  "count": 6,
  "target": "each st",
  "note": "2 sc in each stitch around"
}

// Decrease
{
  "stitch_type": "dec",
  "count": 1,
  "target": "next 2 sts",
  "note": "sc2tog"
}
```

---

### PatternMetadata

Metadata about pattern generation and characteristics.

```typescript
interface PatternMetadata {
  generated_at: string;              // ISO 8601 timestamp
  engine_version: string;            // Semantic version
  total_rounds: number;
  estimated_time_minutes?: number | null;
  difficulty?: Difficulty | null;
  tags: string[];
}

type Difficulty = 'beginner' | 'intermediate' | 'advanced';
```

**Required Fields**:
- `generated_at`: ISO 8601 timestamp
- `engine_version`: Semantic version string (e.g., "0.1.0")
- `total_rounds`: Total number of rounds (>= 0)

**Optional Fields**:
- `estimated_time_minutes`: Completion time estimate (>= 0)
- `difficulty`: Skill level required
- `tags`: Searchable tags (default: `[]`)

**Validation Rules**:
- `total_rounds` must be >= 0
- `estimated_time_minutes` must be >= 0 if provided
- `difficulty` must be from predefined list
- `engine_version` should follow semver format

**Example**:

```json
{
  "generated_at": "2024-11-10T10:30:00Z",
  "engine_version": "0.1.0",
  "total_rounds": 8,
  "estimated_time_minutes": 45,
  "difficulty": "beginner",
  "tags": ["sphere", "3d-shape", "amigurumi", "beginner-friendly"]
}
```

---

## Complete Example

See `docs/examples/` for complete valid patterns:

- `sphere-example.json`: Simple 10cm diameter sphere
- `cylinder-example.json`: 8cm diameter × 12cm height cylinder
- `cone-example.json`: Tapered cone from 12cm to 4cm

### Minimal Sphere Example

```json
{
  "shape": {
    "shape_type": "sphere",
    "diameter_cm": 10.0
  },
  "gauge": {
    "stitches_per_cm": 1.4,
    "rows_per_cm": 1.6
  },
  "rounds": [
    {
      "round_number": 0,
      "stitches": [
        {
          "stitch_type": "sc",
          "count": 6
        }
      ],
      "total_stitches": 6,
      "description": "Magic ring, 6 sc"
    }
  ],
  "metadata": {
    "generated_at": "2024-11-10T10:30:00Z",
    "engine_version": "0.1.0",
    "total_rounds": 1,
    "tags": []
  }
}
```

---

## Validation

### Python (Backend)

```python
from knit_wit_engine.models.dsl import PatternDSL

# From dictionary
pattern = PatternDSL.from_dict(data)

# From JSON string
pattern = PatternDSL.from_json(json_string)

# To JSON
json_output = pattern.to_json()

# Pydantic automatically validates:
# - Required fields
# - Type constraints
# - Value ranges
# - Sequential round numbers
```

### TypeScript (Frontend)

```typescript
import { PatternDSL, isPatternDSL, validateRoundsSequential } from '@/types/dsl';

// Runtime type guard
if (isPatternDSL(data)) {
  // TypeScript knows data is PatternDSL
  console.log(data.shape.shape_type);
}

// Validate round sequence
const isValid = validateRoundsSequential(pattern.rounds);
```

---

## Versioning

Current version: **v0.1** (MVP)

### Version History

- **v0.1** (2024-11-10): Initial MVP specification
  - Support for sphere, cylinder, cone shapes
  - Basic stitch types: sc, inc, dec, ch, slst
  - Spiral-only (no joined rounds)
  - Single crochet focus

### Planned for v0.2

- HDC (half double crochet) and DC (double crochet) support
- Joined rounds (slip stitch to first stitch)
- Color changes and stripes
- Pattern variations and modifiers

---

## Best Practices

### For Pattern Generators

1. **Always validate output**: Use Pydantic models to ensure valid patterns
2. **Sequential rounds**: Start at 0, increment by 1
3. **Accurate stitch counts**: Ensure `total_stitches` matches actual count
4. **Descriptive notes**: Add helpful descriptions for complex rounds
5. **Realistic gauges**: Validate gauge values are within reasonable ranges

### For Pattern Consumers

1. **Validate input**: Always validate JSON before parsing
2. **Handle missing optionals**: Check for null/undefined optional fields
3. **Preserve metadata**: Maintain `generated_at` and `engine_version`
4. **Respect gauge**: Use gauge information for visualization scaling

### For Frontend Developers

1. **Use TypeScript types**: Import from `@/types/dsl`
2. **Runtime validation**: Use type guards for API responses
3. **Error handling**: Gracefully handle validation failures
4. **Progressive enhancement**: Handle missing optional fields

---

## Error Handling

### Common Validation Errors

**Missing required field**:
```
ValidationError: Field 'shape' is required
```

**Invalid value**:
```
ValidationError: Field 'diameter_cm' must be greater than 0
```

**Non-sequential rounds**:
```
ValidationError: Round numbers must be sequential. Expected 2, got 3
```

**Invalid enum value**:
```
ValidationError: Field 'shape_type' must be one of: sphere, cylinder, cone
```

### Handling in Code

**Python**:
```python
from pydantic import ValidationError

try:
    pattern = PatternDSL.from_dict(data)
except ValidationError as e:
    # e.errors() contains detailed error information
    for error in e.errors():
        print(f"Field: {error['loc']}, Error: {error['msg']}")
```

**TypeScript**:
```typescript
import { isPatternDSL } from '@/types/dsl';

if (!isPatternDSL(data)) {
  throw new Error('Invalid pattern format');
}

// Type-safe from here on
const pattern: PatternDSL = data;
```

---

## Testing

### Unit Tests

Run validation tests:

```bash
# Python tests
pytest packages/pattern-engine/tests/unit/test_dsl_validation.py

# Tests cover:
# - All model validations
# - Required field enforcement
# - Value constraints
# - Example pattern validation
# - Schema alignment
```

### Schema Validation

Validate example patterns against JSON Schema:

```bash
# Using ajv-cli (install: npm install -g ajv-cli)
ajv validate -s docs/dsl-schema.json -d docs/examples/sphere-example.json
ajv validate -s docs/dsl-schema.json -d docs/examples/cylinder-example.json
ajv validate -s docs/dsl-schema.json -d docs/examples/cone-example.json
```

---

## References

- **JSON Schema Draft 7**: https://json-schema.org/specification-links.html#draft-7
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/

---

## Change Log

### v0.1 (2024-11-10)

Initial release for Knit-Wit MVP:
- Complete JSON Schema specification
- Pydantic v2 models with validation
- TypeScript type definitions
- Example patterns for all shapes
- Comprehensive validation tests
- Full documentation
