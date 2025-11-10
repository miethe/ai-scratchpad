# Knit-Wit API Contract v1.0

**Version**: 1.0
**Status**: Active (MVP Implementation)
**Last Updated**: 2024-11-10
**API Base URL**: `/api/v1`
**Full URL Example**: `http://localhost:8000/api/v1`

---

## Table of Contents

1. [Overview](#overview)
2. [API Versioning](#api-versioning)
3. [Authentication](#authentication)
4. [Base Response Format](#base-response-format)
5. [Error Handling](#error-handling)
6. [Endpoints](#endpoints)
   - [POST /patterns/generate](#post-patternsgenerate)
   - [GET /patterns/{id}](#get-patternsid)
   - [POST /patterns/{id}/export/pdf](#post-patternsidexportpdf)
   - [POST /patterns/{id}/export/svg](#post-patternsidexportsvg)
   - [GET /health](#get-health)
7. [Data Models](#data-models)
8. [HTTP Status Codes](#http-status-codes)
9. [Rate Limiting](#rate-limiting)
10. [Testing & Examples](#testing--examples)

---

## Overview

The Knit-Wit API provides endpoints for generating parametric crochet patterns, retrieving pattern details, and exporting patterns in multiple formats (PDF, SVG, JSON).

### Key Features

- **RESTful Design**: Follows REST principles with standard HTTP methods and status codes
- **JSON-First**: All request and response bodies use JSON format
- **Type Safe**: Request/response validated against defined schemas
- **Stateless**: Patterns are generated on-demand; no server-side state (MVP)
- **CORS Enabled**: Supports cross-origin requests from web and mobile clients
- **Versioned**: API versioning via URL path (`/api/v1/`)

### Use Cases

1. **Pattern Generation**: Frontend submits shape parameters → backend generates pattern DSL
2. **Pattern Export**: Frontend requests PDF/SVG export of a generated pattern
3. **Health Monitoring**: Monitoring systems check backend availability

---

## API Versioning

### Strategy

- **Version Location**: URL path prefix (e.g., `/api/v1/`)
- **Current Version**: `v1`
- **Breaking Changes**: Increment major version (v1 → v2)
- **Non-Breaking Changes**: Increment minor version (v1.0 → v1.1)
- **Bugfixes**: Increment patch version (v1.0 → v1.0.1)

### Deprecation Policy

When breaking changes are necessary:

1. **Announce**: Document deprecation in API release notes (2 weeks notice)
2. **Support**: Maintain old version for at least 1 version cycle
3. **Migrate**: Provide migration guide for clients
4. **Sunset**: Remove old version with clear communication

### Example

```
Current: /api/v1/patterns/generate
Future: /api/v2/patterns/generate
Old version still works: /api/v1/patterns/generate (deprecated)
```

---

## Authentication

### MVP Approach

**No Authentication Required** in MVP phase.

Rationale:
- Patterns are ephemeral (not persisted)
- No user accounts or sensitive data
- Simplifies initial development
- Can add authentication in v1.1+

### Future Implementation (v1.1+)

When user accounts are added:

```
Authorization: Bearer {jwt_token}
X-API-Key: optional_alternative
```

**Placeholder for future auth endpoint:**
```
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
```

---

## Base Response Format

### Success Response (2xx)

All successful responses follow this structure:

```json
{
  "success": true,
  "data": { /* endpoint-specific data */ },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:00:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

**Fields**:
- `success` (boolean): Always `true` for 2xx responses
- `data` (object): Endpoint-specific payload
- `meta` (object): Response metadata
  - `version`: Engine/API version that generated the response
  - `timestamp`: ISO 8601 server timestamp
  - `request_id`: Unique request identifier for debugging

---

## Error Handling

### Error Response Format (4xx, 5xx)

All error responses follow this standardized format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      /* additional context specific to error */
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:00:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

**Fields**:
- `success` (boolean): Always `false` for error responses
- `error` (object): Error details
  - `code` (string): Machine-readable error code (uppercase with underscores)
  - `message` (string): Human-readable error description
  - `details` (object): Optional additional context
- `meta` (object): Response metadata (same as success)

### Error Codes

#### 400 Bad Request Errors

| Code | Message | Details | Cause |
|------|---------|---------|-------|
| `VALIDATION_ERROR` | Invalid request data | `{field: "shape_type", constraint: "must be sphere, cylinder, or cone"}` | Input validation failed |
| `INVALID_GAUGE` | Invalid gauge parameters | `{field: "gauge.stitches_per_cm", constraint: "must be between 0.5 and 20"}` | Gauge out of acceptable range |
| `INVALID_DIMENSIONS` | Invalid shape dimensions | `{field: "diameter_cm", constraint: "must be > 0"}` | Negative or zero dimensions |
| `INVALID_SHAPE` | Unsupported shape type | `{shape: "hexagon"}` | Shape not in (sphere, cylinder, cone) |
| `MISSING_REQUIRED_FIELD` | Required field missing | `{field: "gauge"}` | Request missing required field |

#### 404 Not Found Errors

| Code | Message | Details | Cause |
|------|---------|---------|-------|
| `PATTERN_NOT_FOUND` | Pattern not found | `{pattern_id: "abc123"}` | Pattern ID doesn't exist or expired |
| `EXPORT_NOT_FOUND` | Export not available | `{format: "pdf"}` | Export wasn't generated or expired |

#### 500 Internal Server Errors

| Code | Message | Details | Cause |
|------|---------|---------|-------|
| `GENERATION_ERROR` | Failed to generate pattern | `{reason: "gauge distribution calculation failed"}` | Algorithm execution error |
| `EXPORT_ERROR` | Failed to export pattern | `{format: "pdf", reason: "PDF generation failed"}` | Export service error |
| `INTERNAL_ERROR` | Unexpected server error | `{message: "..."}` | Unhandled exception |

### Example Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "field": "gauge.stitches_per_cm",
      "constraint": "must be between 0.5 and 20",
      "provided": 0.2
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_xyz789abc"
  }
}
```

---

## Endpoints

### POST /patterns/generate

Generate a crochet pattern based on shape parameters.

**Summary**: Generates a complete crochet pattern (DSL) for the specified shape with the given parameters.

**HTTP Method**: `POST`

**Full Path**: `/api/v1/patterns/generate`

**Status Code**: `201 Created`

#### Request Schema

```typescript
{
  // Shape definition (required)
  shape: {
    shape_type: "sphere" | "cylinder" | "cone";  // required
    diameter_cm?: number;           // required for sphere/cylinder
    height_cm?: number;             // required for cylinder/cone
    base_diameter_cm?: number;      // required for cone
    top_diameter_cm?: number;       // required for cone
  };

  // Gauge information (required)
  gauge: {
    stitches_per_cm: number;        // required, > 0
    rows_per_cm: number;            // required, > 0
    hook_size_mm?: number | null;   // optional, > 0
    yarn_weight?: string | null;    // optional: lace, fingering, sport, DK, worsted, bulky, super_bulky
    swatch_notes?: string | null;   // optional
  };

  // Pattern preferences (optional)
  stitch_type?: "sc";               // optional, default: "sc" (single crochet)
  terminology?: "US" | "UK";        // optional, default: "US"
  units?: "cm" | "inches";          // optional, default: "cm"
  notes?: string | null;            // optional, max 500 chars
}
```

#### Validation Rules

- **shape_type**: Must be one of: `sphere`, `cylinder`, `cone`
- **diameter_cm** (sphere/cylinder): Must be > 0 and <= 100 cm
- **height_cm** (cylinder/cone): Must be > 0 and <= 100 cm
- **base_diameter_cm** (cone): Must be > top_diameter_cm and <= 100 cm
- **top_diameter_cm** (cone): Must be > 0 and < base_diameter_cm
- **stitches_per_cm**: Must be > 0.5 and < 20 (gauge must be reasonable)
- **rows_per_cm**: Must be > 0.5 and < 20
- **hook_size_mm**: If provided, must be > 0
- **yarn_weight**: If provided, must match enum
- **notes**: If provided, max 500 characters, no HTML

#### Request Example

```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "sphere",
      "diameter_cm": 10.0
    },
    "gauge": {
      "stitches_per_cm": 1.4,
      "rows_per_cm": 1.6,
      "hook_size_mm": 4.0,
      "yarn_weight": "worsted"
    },
    "stitch_type": "sc",
    "terminology": "US",
    "units": "cm"
  }'
```

#### Response Schema (201 Created)

```typescript
{
  success: true;
  data: {
    id: string;                     // Unique pattern identifier (UUID)
    pattern: {                      // Complete Pattern DSL
      shape: ShapeParameters;
      gauge: GaugeInfo;
      rounds: RoundInstruction[];
      metadata: PatternMetadata;
      notes?: string;
    };
    created_at: string;             // ISO 8601 timestamp
    expires_at?: string;            // ISO 8601 timestamp (session cache duration)
  };
  meta: {
    version: string;                // e.g., "0.1.0"
    timestamp: string;              // ISO 8601
    request_id: string;
  };
}
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "id": "pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v",
    "pattern": {
      "shape": {
        "shape_type": "sphere",
        "diameter_cm": 10.0
      },
      "gauge": {
        "stitches_per_cm": 1.4,
        "rows_per_cm": 1.6,
        "hook_size_mm": 4.0,
        "yarn_weight": "worsted",
        "swatch_notes": null
      },
      "rounds": [
        {
          "round_number": 0,
          "stitches": [
            {
              "stitch_type": "ch",
              "count": 2,
              "target": null,
              "note": "Magic ring alternative"
            },
            {
              "stitch_type": "sc",
              "count": 6,
              "target": "second ch from hook",
              "note": null
            }
          ],
          "total_stitches": 6,
          "description": "Start with magic ring, 6 sc"
        },
        {
          "round_number": 1,
          "stitches": [
            {
              "stitch_type": "inc",
              "count": 6,
              "target": "each st",
              "note": "2 sc in each stitch around"
            }
          ],
          "total_stitches": 12,
          "description": "Increase round: 2 sc in each st (12)"
        }
      ],
      "metadata": {
        "generated_at": "2024-11-10T12:34:56Z",
        "engine_version": "0.1.0",
        "total_rounds": 8,
        "estimated_time_minutes": 45,
        "difficulty": "beginner",
        "tags": ["sphere", "3d-shape", "amigurumi", "beginner-friendly"]
      },
      "notes": "Work in continuous spiral. Use stitch marker to track beginning of rounds."
    },
    "created_at": "2024-11-10T12:34:56Z",
    "expires_at": "2024-11-10T14:34:56Z"
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Error Responses

**400 Bad Request** - Validation failed

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "field": "shape.diameter_cm",
      "constraint": "must be > 0",
      "provided": -5
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

**400 Bad Request** - Invalid gauge

```json
{
  "success": false,
  "error": {
    "code": "INVALID_GAUGE",
    "message": "Invalid gauge parameters",
    "details": {
      "field": "gauge.stitches_per_cm",
      "constraint": "must be between 0.5 and 20",
      "provided": 0.1
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

**500 Internal Server Error** - Generation failed

```json
{
  "success": false,
  "error": {
    "code": "GENERATION_ERROR",
    "message": "Failed to generate pattern",
    "details": {
      "reason": "gauge distribution calculation exceeded limits"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Performance

- **Target Response Time**: < 200ms (p95)
- **Timeout**: 30 seconds
- **Max Pattern Size**: 500 rounds (enforced)

#### Notes

- Pattern ID is valid for the duration of the session (browser tab)
- After session expires, pattern must be regenerated
- Pattern is not persisted to database in MVP
- Duplicate requests with identical parameters may be cached

---

### GET /patterns/{id}

Retrieve a previously generated pattern.

**Summary**: Returns a pattern that was previously generated in the current session.

**HTTP Method**: `GET`

**Full Path**: `/api/v1/patterns/{id}`

**Status Code**: `200 OK`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Pattern identifier returned from /generate endpoint (UUID format) |

#### Request Example

```bash
curl http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v
```

#### Response Schema (200 OK)

```typescript
{
  success: true;
  data: {
    id: string;
    pattern: PatternDSL;              // Same structure as /generate response
    created_at: string;               // ISO 8601
    expires_at?: string;              // ISO 8601
    time_remaining_seconds?: number;  // Seconds until pattern expires
  };
  meta: {
    version: string;
    timestamp: string;
    request_id: string;
  };
}
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "id": "pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v",
    "pattern": {
      "shape": { "shape_type": "sphere", "diameter_cm": 10.0 },
      "gauge": { "stitches_per_cm": 1.4, "rows_per_cm": 1.6 },
      "rounds": [ /* ... */ ],
      "metadata": { "generated_at": "2024-11-10T12:34:56Z" }
    },
    "created_at": "2024-11-10T12:34:56Z",
    "expires_at": "2024-11-10T14:34:56Z",
    "time_remaining_seconds": 3600
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Error Responses

**404 Not Found** - Pattern expired or invalid ID

```json
{
  "success": false,
  "error": {
    "code": "PATTERN_NOT_FOUND",
    "message": "Pattern not found",
    "details": {
      "pattern_id": "pattern_invalid_id",
      "reason": "pattern expired or does not exist"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Performance

- **Target Response Time**: < 50ms (cached)
- **Timeout**: 10 seconds

#### Notes

- Pattern must be retrieved within session duration (default 2 hours)
- Useful for recovering pattern after navigation or refresh
- Optional for MVP (may defer to Phase 1)

---

### POST /patterns/{id}/export/pdf

Export a pattern to PDF format.

**Summary**: Generates a PDF document of the pattern with instructions, diagram, and materials list.

**HTTP Method**: `POST`

**Full Path**: `/api/v1/patterns/{id}/export/pdf`

**Status Code**: `200 OK`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Pattern identifier (UUID) |

#### Request Schema (Optional Body)

```typescript
{
  // Export options (all optional)
  options?: {
    include_diagram?: boolean;       // default: true
    include_materials?: boolean;     // default: true
    include_gauge_swatch?: boolean;  // default: true
    paper_size?: "A4" | "Letter";   // default: "A4"
    include_difficulty?: boolean;    // default: true
    include_time_estimate?: boolean; // default: true
  };
}
```

#### Request Example

```bash
curl -X POST http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "include_diagram": true,
      "include_materials": true,
      "paper_size": "A4"
    }
  }'
```

#### Response Schema (200 OK)

```typescript
{
  success: true;
  data: {
    id: string;                      // Export ID
    format: "pdf";
    url?: string;                    // Direct download URL (if stored externally)
    content?: string;                // Base64-encoded PDF (if embedded)
    content_type: "application/pdf";
    file_size_bytes: number;
    created_at: string;              // ISO 8601
    expires_at?: string;             // ISO 8601
  };
  meta: {
    version: string;
    timestamp: string;
    request_id: string;
  };
}
```

#### Response Example (Embedded Content)

```json
{
  "success": true,
  "data": {
    "id": "export_pdf_abc123xyz",
    "format": "pdf",
    "content": "JVBERi0xLjQKJeLjz9MNCi...[base64 encoded PDF]...Qg==",
    "content_type": "application/pdf",
    "file_size_bytes": 245678,
    "created_at": "2024-11-10T12:34:56Z",
    "expires_at": "2024-11-10T14:34:56Z"
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Response Example (External URL)

```json
{
  "success": true,
  "data": {
    "id": "export_pdf_abc123xyz",
    "format": "pdf",
    "url": "https://storage.example.com/exports/abc123xyz.pdf",
    "content_type": "application/pdf",
    "file_size_bytes": 245678,
    "created_at": "2024-11-10T12:34:56Z",
    "expires_at": "2024-11-10T14:34:56Z"
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Error Responses

**404 Not Found** - Pattern not found

```json
{
  "success": false,
  "error": {
    "code": "PATTERN_NOT_FOUND",
    "message": "Pattern not found",
    "details": {
      "pattern_id": "pattern_invalid_id"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

**500 Internal Server Error** - Export failed

```json
{
  "success": false,
  "error": {
    "code": "EXPORT_ERROR",
    "message": "Failed to export pattern",
    "details": {
      "format": "pdf",
      "reason": "PDF rendering service unavailable"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Performance

- **Target Response Time**: < 2 seconds (p95)
- **Timeout**: 30 seconds
- **Max File Size**: 10 MB

#### Notes

- PDF is generated on-demand and may be cached temporarily
- Contains formatted instructions, diagram (SVG), and materials list
- Respects user's terminology preference (US/UK)
- MVP: May use embedded content (base64) or cloud storage URL depending on deployment

---

### POST /patterns/{id}/export/svg

Export a pattern to SVG (Scalable Vector Graphics) format.

**Summary**: Generates an SVG visualization of the pattern structure.

**HTTP Method**: `POST`

**Full Path**: `/api/v1/patterns/{id}/export/svg`

**Status Code**: `200 OK`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Pattern identifier (UUID) |

#### Request Schema (Optional Body)

```typescript
{
  // Export options (all optional)
  options?: {
    include_labels?: boolean;        // default: true
    include_stitch_counts?: boolean; // default: true
    style?: "wireframe" | "filled";  // default: "filled"
    show_increases?: boolean;        // default: true (highlight increase stitches)
    show_decreases?: boolean;        // default: true (highlight decrease stitches)
  };
}
```

#### Request Example

```bash
curl -X POST http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v/export/svg \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "include_labels": true,
      "show_increases": true,
      "show_decreases": true,
      "style": "filled"
    }
  }'
```

#### Response Schema (200 OK)

```typescript
{
  success: true;
  data: {
    id: string;                       // Export ID
    format: "svg";
    content: string;                  // SVG XML as string
    content_type: "image/svg+xml";
    file_size_bytes: number;
    width_units: string;              // "cm", "inches", etc.
    height_units: string;
    created_at: string;               // ISO 8601
    expires_at?: string;              // ISO 8601
  };
  meta: {
    version: string;
    timestamp: string;
    request_id: string;
  };
}
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "id": "export_svg_def456uvw",
    "format": "svg",
    "content": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 200 200\"><!-- sphere diagram --><circle cx=\"100\" cy=\"100\" r=\"50\" fill=\"#e8d4f1\" stroke=\"#7b2cbf\" stroke-width=\"2\"/><text x=\"100\" y=\"105\" text-anchor=\"middle\">10cm sphere</text></svg>",
    "content_type": "image/svg+xml",
    "file_size_bytes": 1234,
    "width_units": "cm",
    "height_units": "cm",
    "created_at": "2024-11-10T12:34:56Z",
    "expires_at": "2024-11-10T14:34:56Z"
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Error Responses

**404 Not Found** - Pattern not found

```json
{
  "success": false,
  "error": {
    "code": "PATTERN_NOT_FOUND",
    "message": "Pattern not found",
    "details": {
      "pattern_id": "pattern_invalid_id"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

**500 Internal Server Error** - Export failed

```json
{
  "success": false,
  "error": {
    "code": "EXPORT_ERROR",
    "message": "Failed to export pattern",
    "details": {
      "format": "svg",
      "reason": "SVG rendering failed"
    }
  },
  "meta": {
    "version": "0.1.0",
    "timestamp": "2024-11-10T12:34:56Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Performance

- **Target Response Time**: < 500ms (p95)
- **Timeout**: 10 seconds
- **Max File Size**: 5 MB

#### Notes

- SVG is returned as inline XML string (not embedded)
- Can be directly embedded in HTML, used in Canvas rendering, or saved to file
- Includes visual aids for increase/decrease stitches
- Scalable without quality loss
- WCAG AA color contrast ensured for accessibility

---

### GET /health

Health check endpoint for monitoring and deployment.

**Summary**: Returns the health status of the API and component versions.

**HTTP Method**: `GET`

**Full Path**: `/health` (NOT versioned)

**Status Code**: `200 OK`

#### Request Example

```bash
curl http://localhost:8000/health
```

#### Response Schema (200 OK)

```typescript
{
  status: "healthy" | "degraded" | "unhealthy";
  version: string;                  // API version (e.g., "0.1.0")
  app_name: string;                 // "Knit-Wit API"
  timestamp: string;                // ISO 8601
  components?: {                    // Optional detailed status
    pattern_engine?: "healthy" | "degraded";
    export_service?: "healthy" | "degraded";
  };
}
```

#### Response Example

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "app_name": "Knit-Wit API",
  "timestamp": "2024-11-10T12:34:56Z",
  "components": {
    "pattern_engine": "healthy",
    "export_service": "healthy"
  }
}
```

#### Response Example (Degraded)

```json
{
  "status": "degraded",
  "version": "0.1.0",
  "app_name": "Knit-Wit API",
  "timestamp": "2024-11-10T12:34:56Z",
  "components": {
    "pattern_engine": "healthy",
    "export_service": "degraded"
  }
}
```

#### Performance

- **Target Response Time**: < 50ms
- **Timeout**: 5 seconds
- **SLA**: Should have 99.9% uptime

#### Notes

- Not version-gated (always at root level `/health`)
- No authentication required
- Used by load balancers and monitoring systems
- Should respond even under degraded conditions
- Returns 200 even if services are degraded (to allow further investigation)

---

## Data Models

### PatternDSL

Complete crochet pattern representation.

```typescript
interface PatternDSL {
  shape: ShapeParameters;
  gauge: GaugeInfo;
  rounds: RoundInstruction[];
  metadata: PatternMetadata;
  notes?: string | null;
}
```

**See**: `/docs/dsl-specification.md` for complete field definitions and examples.

### ShapeParameters

Defines the 3D shape type and dimensions.

```typescript
interface ShapeParameters {
  shape_type: "sphere" | "cylinder" | "cone";
  diameter_cm?: number | null;       // For sphere, cylinder
  height_cm?: number | null;         // For cylinder, cone
  base_diameter_cm?: number | null;  // For cone
  top_diameter_cm?: number | null;   // For cone
}
```

### GaugeInfo

Gauge and yarn information.

```typescript
interface GaugeInfo {
  stitches_per_cm: number;
  rows_per_cm: number;
  hook_size_mm?: number | null;
  yarn_weight?: "lace" | "fingering" | "sport" | "DK" | "worsted" | "bulky" | "super_bulky" | null;
  swatch_notes?: string | null;
}
```

### RoundInstruction

A single round (row) of instructions.

```typescript
interface RoundInstruction {
  round_number: number;
  stitches: StitchInstruction[];
  total_stitches: number;
  description?: string | null;
}
```

### StitchInstruction

A single stitch operation.

```typescript
interface StitchInstruction {
  stitch_type: string;  // "sc", "inc", "dec", "ch", "slst", etc.
  count: number;        // default: 1
  target?: string | null;       // "next st", "same st", "each st", etc.
  note?: string | null;
}
```

### PatternMetadata

Pattern generation metadata.

```typescript
interface PatternMetadata {
  generated_at: string;           // ISO 8601
  engine_version: string;         // Semantic version
  total_rounds: number;
  estimated_time_minutes?: number | null;
  difficulty?: "beginner" | "intermediate" | "advanced" | null;
  tags?: string[];                // default: []
}
```

---

## HTTP Status Codes

### Success (2xx)

| Code | Usage |
|------|-------|
| `200 OK` | GET successful, export retrieval successful |
| `201 Created` | Pattern successfully generated |
| `202 Accepted` | Background job accepted (future async exports) |

### Client Errors (4xx)

| Code | Usage |
|------|-------|
| `400 Bad Request` | Invalid input validation (VALIDATION_ERROR, INVALID_GAUGE, etc.) |
| `404 Not Found` | Pattern/export not found (PATTERN_NOT_FOUND, EXPORT_NOT_FOUND) |
| `409 Conflict` | Request conflicts with current state (future use) |
| `422 Unprocessable Entity` | Request format valid but semantically incorrect (future use) |

### Server Errors (5xx)

| Code | Usage |
|------|-------|
| `500 Internal Server Error` | Unhandled exception (INTERNAL_ERROR, GENERATION_ERROR, EXPORT_ERROR) |
| `503 Service Unavailable` | Temporary service outage (export service down) |

---

## Rate Limiting

### MVP Approach

**No rate limiting** in MVP (stateless, lightweight operations).

### Future Implementation (v1.1+)

When scaling or managing resources:

```
X-RateLimit-Limit: 100        # Requests per minute
X-RateLimit-Remaining: 95     # Requests left in window
X-RateLimit-Reset: 1699614900 # Unix timestamp when limit resets
```

**Limits** (proposed):
- Anonymous: 100 requests/minute
- Authenticated: 1000 requests/minute
- Pattern generation: 10 concurrent per IP

**Exceeded** (429 Too Many Requests):
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "window_seconds": 60,
      "retry_after_seconds": 45
    }
  }
}
```

---

## Testing & Examples

### Test the Health Endpoint

```bash
# Using curl
curl http://localhost:8000/health

# Using httpie
http GET http://localhost:8000/health

# Using curl with verbose output
curl -v http://localhost:8000/health
```

### Test Pattern Generation (Sphere)

```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -H "User-Agent: Knit-Wit-Tests/1.0" \
  -d '{
    "shape": {
      "shape_type": "sphere",
      "diameter_cm": 10.0
    },
    "gauge": {
      "stitches_per_cm": 1.4,
      "rows_per_cm": 1.6,
      "hook_size_mm": 4.0,
      "yarn_weight": "worsted"
    },
    "terminology": "US",
    "units": "cm"
  }'
```

### Test Pattern Generation (Cylinder)

```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "cylinder",
      "diameter_cm": 8.0,
      "height_cm": 12.0
    },
    "gauge": {
      "stitches_per_cm": 1.5,
      "rows_per_cm": 1.7,
      "hook_size_mm": 3.5,
      "yarn_weight": "DK"
    }
  }'
```

### Test Pattern Generation (Cone)

```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "cone",
      "base_diameter_cm": 12.0,
      "top_diameter_cm": 4.0,
      "height_cm": 15.0
    },
    "gauge": {
      "stitches_per_cm": 1.6,
      "rows_per_cm": 1.8
    }
  }'
```

### Test Invalid Request (Missing Required Field)

```bash
curl -X POST http://localhost:8000/api/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shape": {
      "shape_type": "sphere"
      # Missing diameter_cm
    }
  }'
```

Expected response (400):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "field": "shape.diameter_cm",
      "constraint": "required for sphere shape"
    }
  }
}
```

### Test Export (PDF)

```bash
# Get pattern ID from generate response, then:
curl -X POST http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "include_diagram": true,
      "include_materials": true,
      "paper_size": "A4"
    }
  }' | jq '.data.content' > pattern.pdf

# Or save URL directly if using external storage
curl -X POST http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v/export/pdf \
  -H "Content-Type: application/json" | jq -r '.data.url'
```

### Test Export (SVG)

```bash
curl -X POST http://localhost:8000/api/v1/patterns/pattern_8f7a3b9c-2e1d-4k6j-9x2p-5q8r1s3t2u9v/export/svg \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.data.content' > pattern.svg
```

### Using Postman / Insomnia

Import the generated OpenAPI specification:

```
GET http://localhost:8000/openapi.json
```

Or import from `/docs/openapi.yaml` when generated.

### Testing with Python/httpx

```python
import httpx
import json

async with httpx.AsyncClient() as client:
    # Test generation
    response = await client.post(
        "http://localhost:8000/api/v1/patterns/generate",
        json={
            "shape": {"shape_type": "sphere", "diameter_cm": 10.0},
            "gauge": {"stitches_per_cm": 1.4, "rows_per_cm": 1.6}
        }
    )
    assert response.status_code == 201
    pattern = response.json()
    pattern_id = pattern["data"]["id"]

    # Test retrieval
    response = await client.get(f"http://localhost:8000/api/v1/patterns/{pattern_id}")
    assert response.status_code == 200

    # Test PDF export
    response = await client.post(
        f"http://localhost:8000/api/v1/patterns/{pattern_id}/export/pdf"
    )
    assert response.status_code == 200
```

### Testing with TypeScript/axios

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Test generation
const generateResponse = await apiClient.post('/patterns/generate', {
  shape: {
    shape_type: 'sphere',
    diameter_cm: 10.0,
  },
  gauge: {
    stitches_per_cm: 1.4,
    rows_per_cm: 1.6,
  },
});

const patternId = generateResponse.data.data.id;

// Test retrieval
const getResponse = await apiClient.get(`/patterns/${patternId}`);
console.log(getResponse.data);

// Test PDF export
const pdfResponse = await apiClient.post(
  `/patterns/${patternId}/export/pdf`
);
const pdfContent = pdfResponse.data.data.content;
```

---

## API Maturity & Roadmap

### Current (v1.0)

- Pattern generation for sphere, cylinder, cone
- PDF and SVG export
- Single crochet (sc) stitch type
- No user accounts or persistence
- No rate limiting or authentication

### Planned (v1.1)

- [ ] User authentication (OAuth 2.0 / JWT)
- [ ] Pattern persistence (database)
- [ ] Pattern history and favorites
- [ ] Support for HDC/DC stitches
- [ ] Joined rounds (in addition to spiral)
- [ ] Rate limiting per user
- [ ] Async exports for large patterns
- [ ] Pattern search and filtering

### Future (v2.0+)

- [ ] Colorwork and stripes
- [ ] User-defined custom shapes
- [ ] Community pattern sharing
- [ ] Yarn recommendation engine
- [ ] AR preview in mobile app
- [ ] Yarn weight approximation from image
- [ ] Subscription/premium features

---

## Support & Questions

For questions about the API:

1. **Check Examples**: See "Testing & Examples" section
2. **Read Spec**: Refer to individual endpoint documentation
3. **Check GitHub Issues**: github.com/knit-wit/issues
4. **Contact Team**: dev@knit-wit.example.com (placeholder)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-10 | Initial API contract for MVP |

---

**End of API Contract**
