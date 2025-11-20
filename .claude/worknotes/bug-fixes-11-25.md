# Bug Fixes - November 25, 2025

## 422 Error on /api/v1/visualization/frames

**Issue**: POST to `/api/v1/visualization/frames` returned 422 with ~100 "Field required" errors

**Root Cause**: Schema mismatch - endpoint expected pattern engine's internal `PatternDSL` format but frontend sends the frontend DSL format from `/patterns/generate`

**Fix**:
- Created `app/models/frontend_dsl.py` with Pydantic models matching frontend TypeScript types
- Created `app/utils/dsl_converter.py` to convert frontend DSL → pattern engine DSL
- Updated `visualization.py` endpoint to accept `FrontendPatternDSL` and convert before processing

**Files Changed**:
- `knit-wit/apps/api/app/models/frontend_dsl.py` (new)
- `knit-wit/apps/api/app/utils/dsl_converter.py` (new)
- `knit-wit/apps/api/app/api/v1/endpoints/visualization.py` (modified)

## Static SVG Visualization Instead of Actual Pattern

**Issue**: Visualization screen showed static "SVG Visualization" text in a circle instead of rendering the actual pattern with nodes, edges, and highlights

**Root Cause**: Frontend had placeholder SVG rendering code instead of implementing the actual visualization using API data

**Fix**:
- Implemented proper SVG rendering in VisualizationScreen with nodes, edges, color-coded stitches
- Added interactive node selection showing stitch type
- Color coding: blue (normal), green (increase), red (decrease)
- Proper data flow using `currentFrame.nodes` and `currentFrame.edges` from API

**Files Changed**:
- `knit-wit/apps/web/src/screens/VisualizationScreen.tsx` (modified)
