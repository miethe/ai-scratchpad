# Knit-Wit API Documentation Index

Complete API contract for the Knit-Wit pattern generation service. All endpoints, schemas, examples, and implementation guidance.

**Phase**: 0 (Foundation)
**Task**: ARCH-3 - API Contract Definition
**Status**: COMPLETED
**Date**: 2024-11-10

---

## Documentation Files

### 1. api-contract.md (33 KB)
**The authoritative API specification document**

Start here for comprehensive API documentation.

**Contains**:
- API overview and design principles
- Authentication and authorization strategy
- Complete endpoint specifications (5 endpoints)
- Request/response schemas with validation rules
- Error handling and status codes
- HTTP status code reference
- Testing examples (curl, Python, TypeScript)
- Performance targets and constraints
- API versioning and deprecation policy
- Future roadmap (v1.1, v2.0)

**Best for**: Understanding the API design, detailed endpoint specs, implementation guidance

**Sections**:
1. Overview (9 sections covering design & constraints)
2. API Versioning (strategy, deprecation policy)
3. Authentication (MVP: none, Future: JWT/OAuth placeholders)
4. Error Handling (9 error codes with details)
5. Endpoints (5 fully documented)
   - POST /patterns/generate
   - GET /patterns/{id}
   - POST /patterns/{id}/export/pdf
   - POST /patterns/{id}/export/svg
   - GET /health
6. Data Models (PatternDSL, shapes, gauge, etc.)
7. Testing & Examples (3 languages)
8. Maturity & Roadmap

---

### 2. openapi.yaml (27 KB)
**Machine-readable OpenAPI 3.0.3 specification**

Use this for tool integration and code generation.

**Contains**:
- Valid OpenAPI 3.0.3 YAML format
- All 5 endpoints with complete definitions
- Request/response schemas with examples
- Reusable component definitions
- Error responses with examples
- Parameter validation rules
- Tags for API organization
- Server definitions (dev, production)

**Best for**:
- Import into Postman/Insomnia for interactive testing
- Generate API client code (TypeScript, Python, etc.)
- Auto-generate documentation sites
- Contract-based testing
- API validation and linting

**Usage**:
```bash
# Import into Postman
File > Import > Paste contents

# Generate TypeScript client
openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o api

# View in Swagger UI
http://localhost:8000/docs
```

---

### 3. quick-reference.md (8.5 KB)
**One-page developer cheat sheet**

Use this while coding.

**Contains**:
- Endpoint summary table
- Copy-paste curl examples
- Response format templates
- Error codes quick lookup
- Validation rules checklist
- Performance targets
- Code examples (TypeScript, Python)
- Useful tools and commands

**Best for**:
- Quick lookup while developing
- Copy-paste examples
- Error code reference
- Performance targets at a glance
- Useful curl commands

---

### 4. README.md (7.9 KB)
**Documentation guide and getting started**

Read this first to navigate the docs.

**Contains**:
- File directory explanation
- Quick facts about the API
- How to use each documentation file
- Testing approaches (curl, Swagger, Python, TypeScript)
- Performance targets
- Error codes reference
- Future API versions
- Related documentation links

**Best for**:
- Understanding what documentation to read
- Finding the right resource for your task
- Testing strategies overview
- Support resources

---

## Quick Navigation

### I want to...

#### Understand the overall API design
**Read**: api-contract.md sections 1-4
- Overview
- API Versioning
- Authentication
- Error Handling

#### Test an endpoint locally
**Read**: api-contract.md "Testing & Examples" section
Or: quick-reference.md "Quick Examples"
**Tools**: curl, httpx, axios

#### Import into Postman/Insomnia
**Use**: openapi.yaml
**Steps**:
1. File → Import
2. Paste openapi.yaml contents
3. All endpoints auto-populate

#### Generate API client
**Use**: openapi.yaml
**Tools**: OpenAPI Generator, Swagger Codegen
**Example**: TypeScript client generation

#### Implement an endpoint in Phase 1
**Read**: api-contract.md for that endpoint
**Use**: openapi.yaml for schema validation
**Follow**: Integration checklist in README.md

#### Debug an error
**Read**: api-contract.md "Error Handling" section
Or: quick-reference.md "Error Codes"
**Find**: Error code, cause, solution

#### Understand validation rules
**Read**: api-contract.md endpoint "Validation Rules"
Or: quick-reference.md "Request Validation Rules"

#### See code examples
**Read**: quick-reference.md for TypeScript/Python examples
Or: api-contract.md "Testing & Examples"

#### Check performance targets
**Read**: quick-reference.md "Response Latency Targets"
Or: api-contract.md "Performance" sections per endpoint

---

## API Quick Facts

### Base URLs
```
Development: http://localhost:8000/api/v1
Production: https://api.knit-wit.app/api/v1
```

### Authentication
- MVP (v0.1.0): Not required
- Future (v1.1+): JWT tokens or OAuth 2.0

### Response Format
All responses follow standardized format with `success`, `data`, and `meta` fields.

### Error Format
Standardized error responses with error code, message, and details.

### Endpoints (5 total)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| POST | /patterns/generate | Generate pattern | 201 |
| GET | /patterns/{id} | Retrieve pattern | 200 |
| POST | /patterns/{id}/export/pdf | Export PDF | 200 |
| POST | /patterns/{id}/export/svg | Export SVG | 200 |
| GET | /health | Health check | 200 |

---

## Implementation Phase 1

### Recommended Order
1. POST /patterns/generate (highest priority)
2. GET /health (verify compliance)
3. POST /patterns/{id}/export/pdf
4. POST /patterns/{id}/export/svg
5. GET /patterns/{id} (optional, can defer)

### For Each Endpoint
- Create Pydantic request/response models
- Implement validation logic
- Create FastAPI route handler
- Return correct status codes
- Use standardized error format
- Write tests (80%+ coverage)
- Verify against contract

---

## Key Sections Quick Links

### In api-contract.md:
- **API Overview**: Understanding design and constraints
- **Error Handling**: Error codes (400, 404, 500)
- **Endpoints**: Complete specifications for all 5
- **Data Models**: PatternDSL, shapes, gauge, rounds, stitches
- **Testing & Examples**: curl, Python, TypeScript, Postman
- **API Maturity & Roadmap**: Future versions v1.1, v2.0

### In openapi.yaml:
- **Paths**: All 5 endpoint definitions
- **Components/Schemas**: All data models
- **Responses**: Success and error examples
- **Examples**: Sphere, cylinder, cone requests

### In quick-reference.md:
- **Endpoints Summary**: One-page table
- **Quick Examples**: Copy-paste curl commands
- **Error Codes**: Fast lookup table
- **Code Examples**: TypeScript, Python samples

### In README.md:
- **Files Overview**: What each doc contains
- **Using This Documentation**: How to find what you need
- **Testing the API**: Multiple approaches
- **Development Workflow**: Implementation order
- **Integration Checklist**: What to do for each endpoint

---

## Document Statistics

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| api-contract.md | 33 KB | 1411 | Complete specification |
| openapi.yaml | 27 KB | 950 | Machine-readable spec |
| quick-reference.md | 8.5 KB | 393 | Developer cheat sheet |
| README.md | 7.9 KB | 304 | Navigation guide |
| **TOTAL** | **76 KB** | **3058** | **Comprehensive docs** |

---

## Validation & Quality

### Completeness
- ✓ 5/5 endpoints fully documented
- ✓ Request/response schemas: 100%
- ✓ Error cases documented: 100%
- ✓ Examples provided: 100%
- ✓ Validation rules: 100%

### OpenAPI Compliance
- ✓ Valid OpenAPI 3.0.3
- ✓ All required fields present
- ✓ Schemas self-contained
- ✓ Examples validate against schemas

### Developer Experience
- ✓ 3 documentation levels
- ✓ Examples in 3 languages
- ✓ Clear error messages
- ✓ Integration checklist
- ✓ Migration path documented

---

## Related Documentation

### Phase 0 Completion
- **ARCH-1**: Algorithm Spike - `/docs/architecture/algorithm-spike.md`
- **ARCH-2**: DSL Schema - `/docs/dsl-specification.md`, `/docs/dsl-schema.json`
- **ARCH-3**: API Contract - You are here
- **ARCH-2 Completion**: `/docs/ARCH-2-COMPLETION.md`
- **ARCH-3 Completion**: `/docs/ARCH-3-COMPLETION.md`

### Examples
- Sphere pattern: `/docs/examples/sphere-example.json`
- Cylinder pattern: `/docs/examples/cylinder-example.json`
- Cone pattern: `/docs/examples/cone-example.json`

### Project Plans
- Phase 0 Overview: `/project_plans/mvp/phases/phase-0.md`
- Implementation Plan: `/project_plans/mvp/implementation-plan-overview.md`
- PRD: `/project_plans/mvp/prd.md`

---

## Tools & Integration

### API Testing
- **curl**: Command-line testing (examples provided)
- **Postman**: Import openapi.yaml
- **Insomnia**: Import openapi.yaml
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Code Generation
- **OpenAPI Generator**: Generate clients in 40+ languages
- **Swagger Codegen**: Alternative generator
- **Example**: TypeScript axios client from openapi.yaml

### Development Tools
- **httpx**: Python async HTTP client
- **axios**: TypeScript/JavaScript HTTP client
- **Postman**: API development and testing
- **Insomnia**: REST/GraphQL client

---

## Getting Started Checklist

- [ ] Read this file (INDEX.md) - you are here
- [ ] Skim api-contract.md overview
- [ ] Look at your target endpoint in api-contract.md
- [ ] Review quick-reference.md for examples
- [ ] Import openapi.yaml into Postman/Insomnia
- [ ] Test with curl examples from quick-reference.md
- [ ] For Phase 1 implementation: Read api-contract.md fully
- [ ] Create Pydantic models from schemas
- [ ] Implement endpoint per specification
- [ ] Write tests covering all examples
- [ ] Verify response matches spec
- [ ] Test error cases
- [ ] Check performance vs targets

---

## Support

### Common Questions

**Q: Where do I find the exact schema for request X?**
A: See the "Request Schema" section in api-contract.md for endpoint X

**Q: What error codes can endpoint Y return?**
A: See "Error Responses" section in api-contract.md for endpoint Y

**Q: How do I import the API into Postman?**
A: Copy openapi.yaml content, then File > Import > Paste text in Postman

**Q: What are the validation rules for gauge?**
A: See quick-reference.md "Request Validation Rules" section

**Q: Can I generate TypeScript types from the spec?**
A: Yes, use OpenAPI Generator with openapi.yaml

**Q: What's the response format for errors?**
A: See api-contract.md "Error Response Format" section

**Q: How long are patterns cached?**
A: Default 2 hours in session, documented in endpoint details

**Q: Is authentication required in MVP?**
A: No, documented in "Authentication" section of api-contract.md

---

## Next Steps

### For Developers (Phase 1)
1. Pick an endpoint from implementation order
2. Read its full specification in api-contract.md
3. Review openapi.yaml schema definition
4. Copy examples from quick-reference.md
5. Start implementation following integration checklist
6. Write tests covering all success and error cases
7. Test with provided examples
8. Submit for code review

### For Architects
1. Review ARCH-3-COMPLETION.md for deliverables
2. Verify all success criteria met
3. Review design decisions in api-contract.md
4. Confirm Phase 1 implementation order
5. Plan integration testing approach

### For PMs/Stakeholders
1. Review "API Maturity & Roadmap" in api-contract.md
2. See what's in MVP (v0.1.0) vs future versions
3. Understand constraints and when they'll be addressed
4. Plan user communication for auth (coming in v1.1)

---

## Version History

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2024-11-10 | COMPLETED | Initial API contract for MVP |

---

**Phase**: 0 - Foundation & Setup
**Task**: ARCH-3 - API Contract Definition
**Status**: COMPLETED ✓
**Ready For**: Phase 1 Implementation

---

**INDEX.md** - Last updated 2024-11-10
This file provides navigation guidance. For specific API details, see the dedicated documentation files above.
