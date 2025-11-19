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
