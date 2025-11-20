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

## 3D Visualization Feature Implementation

**Feature**: Added 3D isometric visualization with 2D/3D toggle for progressive pattern construction

**Implementation**:
- Comprehensive architecture design with isometric projection (30° angle)
- Backend 3D coordinate generation for sphere, cylinder, cone shapes
- Shape-aware geometric algorithms (spherical coords, cylindrical stacking, linear taper)
- Painter's algorithm depth sorting for correct occlusion
- Frontend SVG rendering with depth cues (size 60-100%, opacity 70-100%)
- Segmented control toggle UI between 2D and 3D views
- Query parameter ?mode=3d on /visualization/frames endpoint

**Testing**:
- 27/28 tests passed including all 12 new 3D tests
- Verified sphere, cylinder, cone coordinate generation
- Confirmed backward compatibility with 2D mode
- Performance <150ms (meets design target)

**Files Changed**:
- `knit-wit/docs/architecture/3d-visualization-design.md` (new)
- `knit-wit/docs/architecture/3d-visualization-recommendations.md` (new)
- `knit-wit/apps/api/app/models/visualization.py` (extended with 3D fields)
- `knit-wit/apps/api/app/services/visualization_service.py` (added 3D generators)
- `knit-wit/apps/api/app/api/v1/endpoints/visualization.py` (added mode param)
- `knit-wit/apps/api/tests/unit/test_visualization_service.py` (added 3D tests)
- `knit-wit/apps/api/tests/integration/test_visualization_api.py` (added 3D integration tests)
- `knit-wit/apps/web/src/types/visualization.ts` (extended with 3D types)
- `knit-wit/apps/web/src/services/api.ts` (added mode parameter)
- `knit-wit/apps/web/src/stores/useVisualizationStore.ts` (added mode state)
- `knit-wit/apps/web/src/screens/VisualizationScreen.tsx` (implemented 3D rendering)
