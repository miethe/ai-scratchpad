/**
 * Knit-Wit Pattern DSL TypeScript Types
 *
 * Type definitions for the Knit-Wit Domain-Specific Language (DSL) v0.1.
 * These types mirror the Pydantic models in packages/pattern-engine/knit_wit_engine/models/dsl.py
 * to ensure type safety across the frontend-backend boundary.
 *
 * @module types/dsl
 * @version 0.1.0
 */

/**
 * Type of 3D shape to generate
 */
export type ShapeType = 'sphere' | 'cylinder' | 'cone';

/**
 * Recommended yarn weight categories
 */
export type YarnWeight = 'lace' | 'fingering' | 'sport' | 'DK' | 'worsted' | 'bulky' | 'super_bulky';

/**
 * Pattern difficulty levels
 */
export type Difficulty = 'beginner' | 'intermediate' | 'advanced';

/**
 * A single stitch operation within a round.
 *
 * Examples:
 * - "sc in next st" (single crochet in next stitch)
 * - "inc" (increase - 2 sc in same stitch)
 * - "dec" (decrease - sc2tog)
 */
export interface StitchInstruction {
  /**
   * Type of stitch (sc, hdc, dc, inc, dec, etc.)
   * @example "sc", "inc", "dec", "hdc", "dc"
   */
  stitch_type: string;

  /**
   * Number of times to repeat this stitch
   * @default 1
   * @minimum 1
   */
  count: number;

  /**
   * Where to place the stitch (next st, same st, etc.)
   * @example "next st", "same st", "next 2 sts"
   */
  target?: string | null;

  /**
   * Additional instruction or clarification
   */
  note?: string | null;
}

/**
 * Complete instruction for a single round (row) in the pattern.
 *
 * Each round contains one or more stitch instructions and metadata
 * about the round number and total stitch count.
 */
export interface RoundInstruction {
  /**
   * Round number (0-indexed)
   * @minimum 0
   */
  round_number: number;

  /**
   * List of stitch instructions for this round
   * @minItems 1
   */
  stitches: StitchInstruction[];

  /**
   * Total stitch count after completing this round
   * @minimum 1
   */
  total_stitches: number;

  /**
   * Human-readable description of the round
   */
  description?: string | null;
}

/**
 * Gauge information for the pattern.
 *
 * Gauge determines the relationship between physical dimensions
 * and stitch/row counts.
 */
export interface GaugeInfo {
  /**
   * Number of stitches per centimeter
   * @minimum 0 (exclusive)
   */
  stitches_per_cm: number;

  /**
   * Number of rows per centimeter
   * @minimum 0 (exclusive)
   */
  rows_per_cm: number;

  /**
   * Recommended crochet hook size in millimeters
   * @minimum 0 (exclusive)
   */
  hook_size_mm?: number | null;

  /**
   * Recommended yarn weight category
   */
  yarn_weight?: YarnWeight | null;

  /**
   * Additional gauge swatch notes
   */
  swatch_notes?: string | null;
}

/**
 * Parameters defining the shape dimensions.
 *
 * Different shapes require different parameters:
 * - Sphere: diameter_cm
 * - Cylinder: diameter_cm, height_cm
 * - Cone: base_diameter_cm, top_diameter_cm, height_cm
 */
export interface ShapeParameters {
  /**
   * Type of 3D shape
   */
  shape_type: ShapeType;

  /**
   * Diameter in centimeters (sphere, cylinder)
   * @minimum 0 (exclusive)
   */
  diameter_cm?: number | null;

  /**
   * Height in centimeters (cylinder, cone)
   * @minimum 0 (exclusive)
   */
  height_cm?: number | null;

  /**
   * Base diameter in centimeters (cone)
   * @minimum 0 (exclusive)
   */
  base_diameter_cm?: number | null;

  /**
   * Top diameter in centimeters (cone)
   * @minimum 0 (exclusive)
   */
  top_diameter_cm?: number | null;
}

/**
 * Metadata about the pattern generation.
 *
 * Includes information about generation time, version, and other
 * non-instruction data.
 */
export interface PatternMetadata {
  /**
   * Pattern generation timestamp (ISO 8601 format)
   */
  generated_at: string;

  /**
   * Pattern engine version used
   * @default "0.1.0"
   * @pattern ^\d+\.\d+\.\d+$
   */
  engine_version: string;

  /**
   * Total number of rounds
   * @minimum 0
   */
  total_rounds: number;

  /**
   * Estimated completion time in minutes
   * @minimum 0
   */
  estimated_time_minutes?: number | null;

  /**
   * Pattern difficulty level
   */
  difficulty?: Difficulty | null;

  /**
   * Searchable tags for the pattern
   * @default []
   */
  tags: string[];
}

/**
 * Complete pattern representation in the Knit-Wit DSL.
 *
 * This is the top-level model that contains all information needed
 * to render and execute a crochet pattern.
 */
export interface PatternDSL {
  /**
   * Shape parameters
   */
  shape: ShapeParameters;

  /**
   * Gauge information
   */
  gauge: GaugeInfo;

  /**
   * Round-by-round instructions
   * @minItems 1
   */
  rounds: RoundInstruction[];

  /**
   * Pattern metadata
   */
  metadata: PatternMetadata;

  /**
   * General notes and instructions
   */
  notes?: string | null;
}

/**
 * Type guards for runtime validation
 */
export const isShapeType = (value: unknown): value is ShapeType => {
  return typeof value === 'string' && ['sphere', 'cylinder', 'cone'].includes(value);
};

export const isYarnWeight = (value: unknown): value is YarnWeight => {
  return (
    typeof value === 'string' &&
    ['lace', 'fingering', 'sport', 'DK', 'worsted', 'bulky', 'super_bulky'].includes(value)
  );
};

export const isDifficulty = (value: unknown): value is Difficulty => {
  return typeof value === 'string' && ['beginner', 'intermediate', 'advanced'].includes(value);
};

export const isStitchInstruction = (value: unknown): value is StitchInstruction => {
  if (typeof value !== 'object' || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.stitch_type === 'string' &&
    typeof obj.count === 'number' &&
    obj.count >= 1
  );
};

export const isRoundInstruction = (value: unknown): value is RoundInstruction => {
  if (typeof value !== 'object' || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.round_number === 'number' &&
    obj.round_number >= 0 &&
    Array.isArray(obj.stitches) &&
    obj.stitches.length > 0 &&
    typeof obj.total_stitches === 'number' &&
    obj.total_stitches >= 1
  );
};

export const isPatternDSL = (value: unknown): value is PatternDSL => {
  if (typeof value !== 'object' || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.shape === 'object' &&
    obj.shape !== null &&
    typeof obj.gauge === 'object' &&
    obj.gauge !== null &&
    Array.isArray(obj.rounds) &&
    obj.rounds.length > 0 &&
    typeof obj.metadata === 'object' &&
    obj.metadata !== null
  );
};

/**
 * Validation helpers
 */

/**
 * Validates that round numbers are sequential starting from 0
 */
export const validateRoundsSequential = (rounds: RoundInstruction[]): boolean => {
  return rounds.every((round, index) => round.round_number === index);
};

/**
 * Validates that a shape has the required parameters
 */
export const validateShapeParameters = (shape: ShapeParameters): boolean => {
  switch (shape.shape_type) {
    case 'sphere':
      return typeof shape.diameter_cm === 'number' && shape.diameter_cm > 0;
    case 'cylinder':
      return (
        typeof shape.diameter_cm === 'number' &&
        shape.diameter_cm > 0 &&
        typeof shape.height_cm === 'number' &&
        shape.height_cm > 0
      );
    case 'cone':
      return (
        typeof shape.base_diameter_cm === 'number' &&
        shape.base_diameter_cm > 0 &&
        typeof shape.top_diameter_cm === 'number' &&
        shape.top_diameter_cm > 0 &&
        typeof shape.height_cm === 'number' &&
        shape.height_cm > 0
      );
    default:
      return false;
  }
};

/**
 * Default values for creating new patterns
 */
export const defaultGaugeInfo: GaugeInfo = {
  stitches_per_cm: 1.4, // 14 stitches per 10cm
  rows_per_cm: 1.6, // 16 rows per 10cm
  hook_size_mm: 4.0,
  yarn_weight: 'worsted',
  swatch_notes: null,
};

export const defaultPatternMetadata: Omit<PatternMetadata, 'generated_at' | 'total_rounds'> = {
  engine_version: '0.1.0',
  estimated_time_minutes: null,
  difficulty: null,
  tags: [],
};
