/**
 * Pattern types based on Knit-Wit Pattern DSL v0.1
 * These will be expanded as the pattern engine is integrated
 */

export type ShapeType = 'sphere' | 'cylinder' | 'cone';
export type StitchType = 'sc' | 'inc' | 'dec' | 'slst' | 'ch';
export type Units = 'cm' | 'in';
export type Terminology = 'US' | 'UK';

export interface GaugeParams {
  sts_per_10cm: number;
  rows_per_10cm: number;
}

export interface PatternRequest {
  shape: ShapeType;
  diameter?: number;
  height?: number;
  units: Units;
  gauge: GaugeParams;
  stitch: StitchType;
  terms: Terminology;
}

export interface PatternDSL {
  meta: {
    version: string;
    units: Units;
    terms: Terminology;
    stitch: StitchType;
    round_mode: 'spiral' | 'joined';
    gauge: GaugeParams;
  };
  object: {
    type: ShapeType;
    params: Record<string, number>;
  };
  rounds: PatternRound[];
  materials: {
    yarn_weight: string;
    hook_size_mm: number;
    yardage_estimate: number;
  };
  notes: string[];
}

export interface PatternRound {
  r: number;
  ops: PatternOperation[];
  stitches: number;
}

export interface PatternOperation {
  op: string;
  count: number;
  repeat?: number;
}
