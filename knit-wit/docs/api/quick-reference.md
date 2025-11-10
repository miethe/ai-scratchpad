# Knit-Wit API - Quick Reference

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.knit-wit.app/api/v1
```

## Endpoints Summary

| Method | Path | Status | Purpose |
|--------|------|--------|---------|
| POST | `/patterns/generate` | 201 | Generate pattern |
| GET | `/patterns/{id}` | 200 | Retrieve pattern |
| POST | `/patterns/{id}/export/pdf` | 200 | Export as PDF |
| POST | `/patterns/{id}/export/svg` | 200 | Export as SVG |
| GET | `/health` | 200 | Health check |

---

## Quick Examples

### Generate Sphere Pattern
```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "sphere",
      "diameter_cm": 10
    },
    "gauge": {
      "stitches_per_cm": 1.4,
      "rows_per_cm": 1.6,
      "hook_size_mm": 4.0,
      "yarn_weight": "worsted"
    }
  }' | jq .
```

### Generate Cylinder Pattern
```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "cylinder",
      "diameter_cm": 8,
      "height_cm": 12
    },
    "gauge": {
      "stitches_per_cm": 1.5,
      "rows_per_cm": 1.7
    }
  }' | jq .
```

### Retrieve Pattern
```bash
curl http://localhost:8000/api/v1/patterns/pattern_abc123 | jq .
```

### Export to PDF
```bash
curl -X POST http://localhost:8000/api/v1/patterns/pattern_abc123/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "include_diagram": true,
      "paper_size": "A4"
    }
  }' | jq '.data.content' | base64 -d > pattern.pdf
```

### Export to SVG
```bash
curl -X POST http://localhost:8000/api/v1/patterns/pattern_abc123/export/svg | jq -r '.data.content' > pattern.svg
```

### Health Check
```bash
curl http://localhost:8000/health | jq .
```

---

## Response Format

### Success (201, 200)
```json
{
  "success": true,
  "data": { /* endpoint-specific */ },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123"
  }
}
```

### Error (400, 404, 500)
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { /* additional context */ }
  },
  "meta": { /* standard meta */ }
}
```

---

## Error Codes

### Validation Errors (400)
| Code | Meaning |
|------|---------|
| `VALIDATION_ERROR` | Input validation failed |
| `INVALID_GAUGE` | Gauge outside acceptable range (0.5-20) |
| `INVALID_DIMENSIONS` | Negative or zero dimensions |
| `INVALID_SHAPE` | Shape not in (sphere, cylinder, cone) |
| `MISSING_REQUIRED_FIELD` | Required field missing |

### Not Found (404)
| Code | Meaning |
|------|---------|
| `PATTERN_NOT_FOUND` | Pattern expired or invalid ID |
| `EXPORT_NOT_FOUND` | Export not available |

### Server Errors (500)
| Code | Meaning |
|------|---------|
| `GENERATION_ERROR` | Pattern generation failed |
| `EXPORT_ERROR` | Export generation failed |
| `INTERNAL_ERROR` | Unexpected server error |

---

## Request Validation Rules

### Shape Parameters
```
sphere:
  - diameter_cm: required, > 0, <= 100

cylinder:
  - diameter_cm: required, > 0, <= 100
  - height_cm: required, > 0, <= 100

cone:
  - base_diameter_cm: required, > 0, <= 100
  - top_diameter_cm: required, > 0, < base_diameter_cm
  - height_cm: required, > 0, <= 100
```

### Gauge Parameters
```
stitches_per_cm: required, > 0.5, < 20
rows_per_cm: required, > 0.5, < 20
hook_size_mm: optional, if provided > 0
yarn_weight: optional, must be from enum
  - lace, fingering, sport, DK, worsted, bulky, super_bulky
```

### Other Validation
```
stitch_type: optional, default "sc"
terminology: optional, default "US", choices: US | UK
units: optional, default "cm", choices: cm | inches
notes: optional, max 500 characters
```

---

## Response Latency Targets (P95)

| Endpoint | Target |
|----------|--------|
| POST /patterns/generate | < 200ms |
| GET /patterns/{id} | < 50ms |
| POST /patterns/{id}/export/pdf | < 2 sec |
| POST /patterns/{id}/export/svg | < 500ms |
| GET /health | < 50ms |

---

## TypeScript Types (from OpenAPI Schema)

```typescript
// Request
interface GeneratePatternRequest {
  shape: ShapeParameters;
  gauge: GaugeInfo;
  stitch_type?: string;      // default: "sc"
  terminology?: "US" | "UK"; // default: "US"
  units?: "cm" | "inches";   // default: "cm"
  notes?: string;            // max 500 chars
}

// Response
interface GeneratePatternResponse {
  success: boolean;
  data: {
    id: string;              // UUID
    pattern: PatternDSL;
    created_at: string;      // ISO 8601
    expires_at?: string;     // ISO 8601
  };
  meta: {
    version: string;         // e.g., "0.1.0"
    timestamp: string;       // ISO 8601
    request_id: string;
  };
}

// Error
interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details: Record<string, any>;
  };
  meta: {
    version: string;
    timestamp: string;
    request_id: string;
  };
}
```

---

## Python httpx Usage

```python
import httpx
import asyncio
from typing import Any

async def generate_pattern(shape: dict, gauge: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/patterns/generate",
            json={
                "shape": shape,
                "gauge": gauge,
                "terminology": "US"
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

async def export_pdf(pattern_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8000/api/v1/patterns/{pattern_id}/export/pdf"
        )
        response.raise_for_status()
        return response.json()

# Usage
pattern = asyncio.run(
    generate_pattern(
        shape={"shape_type": "sphere", "diameter_cm": 10},
        gauge={"stitches_per_cm": 1.4, "rows_per_cm": 1.6}
    )
)
pattern_id = pattern["data"]["id"]
```

---

## TypeScript axios Usage

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000
});

async function generatePattern(shape: any, gauge: any) {
  const response = await api.post('/patterns/generate', {
    shape,
    gauge,
    terminology: 'US'
  });
  return response.data;
}

async function exportPdf(patternId: string) {
  const response = await api.post(`/patterns/${patternId}/export/pdf`);
  return response.data;
}

// Error handling
try {
  const pattern = await generatePattern(
    { shape_type: 'sphere', diameter_cm: 10 },
    { stitches_per_cm: 1.4, rows_per_cm: 1.6 }
  );
} catch (error) {
  if (error.response?.status === 400) {
    console.error('Validation error:', error.response.data.error);
  } else if (error.response?.status === 500) {
    console.error('Server error:', error.response.data.error);
  }
}
```

---

## OpenAPI/Swagger

- **File**: `docs/api/openapi.yaml`
- **View**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Raw JSON**: http://localhost:8000/openapi.json

Import openapi.yaml into:
- Postman
- Insomnia
- Swagger UI
- OpenAPI Generator

---

## Important Notes

### Pattern Lifecycle
1. Generated via POST /patterns/generate
2. ID returned in response
3. Stored in session cache (2 hour default)
4. Retrieved via GET /patterns/{id}
5. Exported via POST /patterns/{id}/export/*
6. Expires when session ends or timeout reached

### MVP Constraints
- Patterns not persisted (no database)
- No authentication required
- No rate limiting
- Stateless backend
- Session-based storage only

### Best Practices
- Always check `success` field before accessing `data`
- Implement proper error handling with error codes
- Store pattern ID for later retrieval
- Validate input before sending (client-side)
- Use request_id for debugging/logging
- Set appropriate timeouts (30s generation, 10s retrieval)
- Cache pattern ID during user session

---

## Useful Tools

```bash
# Format/pretty-print JSON
curl ... | jq .

# Save to file
curl ... | jq '.' > response.json

# Extract specific field
curl ... | jq '.data.id'

# Pretty headers
curl -v ... 2>&1 | grep '<'

# Test with specific User-Agent
curl -H "User-Agent: MyApp/1.0" ...

# Measure response time
curl -w "@curl-format.txt" -o /dev/null -s http://...

# HTTP timing breakdown
curl -w '%{time_total}s\n' http://...
```

---

**Last Updated**: 2024-11-10
**Version**: 0.1.0
**Status**: MVP Phase
