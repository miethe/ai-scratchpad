---
name: symbols
description: Token-efficient codebase navigation through intelligent symbol loading and querying. Use this skill when implementing new features (find existing patterns), exploring codebase structure, searching for components/functions/types, or understanding architectural layers. Reduces token usage by 60-80% compared to loading full files.
---

# Symbols - Intelligent Codebase Symbol Analysis

## Overview

Enable token-efficient navigation of the MeatyPrompts codebase through pre-generated symbol graphs chunked by domain (UI, Web, API, Shared) and separated from test files. Query symbols by name, kind, path, or architectural layer without loading entire files. Load only the context needed for the current task.

**Key Benefits:**
- 60-80% reduction in token usage vs loading full codebase
- Progressive loading strategy (load only what's needed)
- Domain-specific chunking for targeted context (UI primitives, Web frontend, API backend, Shared utilities)
- Architectural layer awareness (Router → Service → Repository → DB)
- Test file separation (loaded only when debugging)
- Precise code references with file paths and line numbers
- Complete codebase coverage including frontend and backend

## When to Use

Use this skill when:
- **Before implementing new features** - Find existing patterns to follow
- **Exploring codebase structure** - Understand how code is organized
- **Searching for code** - Locate components, functions, hooks, services, or types
- **Token-efficient context loading** - Avoid loading entire files or directories
- **Understanding architectural layers** - Verify Router → Service → Repository patterns
- **Cross-domain development** - Work across UI, API, and Shared code
- **Debugging** - Load relevant symbols including tests

Do NOT use this skill for:
- Reading actual file contents (use Read tool instead)
- Making code changes (symbols are read-only references)
- Runtime analysis (symbols are static analysis only)

## Recent Fixes (October 2025)

The following critical P0 bugs were fixed to restore full codebase coverage:

1. **Added Web Domain Support** - Added `symbols-web.json` (629KB) to SYMBOL_FILES dictionary. Previously, the entire frontend app (apps/web) was invisible to symbol queries.

2. **Updated Domain Queries** - All query functions now search ui, web, api, and shared domains by default when no specific domain is provided. Previously only searched ui and api.

3. **Implemented Schema Normalization** - Added `_normalize_symbol_data()` function to handle both flat (`{symbols: [...]}`) and hierarchical (`{modules: [...]}`) JSON formats. Enables consistent parsing across all symbol files.

4. **Regenerated symbols-web.json** - Complete recursive directory scanning now captures all frontend code including:
   - React Query hooks (useContexts, useAgents, useMutations)
   - API client modules
   - Type definitions and interfaces
   - Frontend pages and components

5. **Fixed Domain Mapping** - Clarified domain definitions:
   - `ui`: UI primitives from packages/ui
   - `web`: Frontend application from apps/web
   - `api`: Backend services, routers, repositories
   - `shared`: Utilities and types (currently mapped to web)

**Impact**: Symbols skill coverage increased from 17% to 100% of codebase. Fixed 83% miss rate on frontend-related code.

See `docs/testing/symbols_skill_investigation_findings.md` for complete technical details.

## Core Capabilities

### 1. Query Symbols

Query symbols by name, kind, domain, or path without loading the entire symbol graph.

**When to use**: Find specific symbols, search by partial name, filter by type or location.

**How to use**:

Execute the Python function from `scripts/symbol_tools.py`:

```python
from symbol_tools import query_symbols

# Find all React components with "Card" in the name
results = query_symbols(name="Card", kind="component", domain="ui", limit=10)

# Find authentication-related functions
results = query_symbols(name="auth", kind="function", path="services")

# Get all custom hooks (summary only for quick scan)
results = query_symbols(kind="hook", domain="ui", summary_only=True)
```

**Parameters**:
- `name` (optional) - Symbol name (supports partial/fuzzy matching)
- `kind` (optional) - Symbol kind: component, hook, function, class, interface, type, method
- `domain` (optional) - Domain filter: ui (UI primitives), web (frontend app), api (backend), shared (utilities)
- `path` (optional) - File path pattern (e.g., "components", "hooks", "services")
- `limit` (optional) - Maximum results to return (default: 20)
- `summary_only` (optional) - Return only name and summary (default: false)

**Returns**: List of matching symbols with file path, line number, domain, and summary.

### 2. Load Domain

Load complete symbol set for a specific domain (UI, Web, API, or Shared).

**When to use**: Need broader context for a domain, implementing features that touch multiple files within a domain.

**How to use**:

```python
from symbol_tools import load_domain

# Load UI symbols for UI component work (excludes tests)
ui_context = load_domain(domain="ui", include_tests=False, max_symbols=100)

# Load Web symbols for frontend app development
web_context = load_domain(domain="web", include_tests=False, max_symbols=100)

# Load API symbols with tests for debugging
api_context = load_domain(domain="api", include_tests=True)

# Load first 50 shared symbols for quick reference
shared_context = load_domain(domain="shared", max_symbols=50)
```

**Parameters**:
- `domain` (required) - Domain to load: ui (UI primitives), web (frontend app), api (backend), shared (utilities)
- `include_tests` (optional) - Include test file symbols (default: false)
- `max_symbols` (optional) - Limit number of symbols returned (default: all)

**Returns**: Dict with domain, type, totalSymbols count, and symbols array.

**Token efficiency**: Load 50-100 symbols (~10-15KB) instead of full domain (~250KB)

### 3. Search Patterns

Advanced pattern-based search with architectural layer awareness.

**When to use**: Find symbols matching regex patterns, filter by architectural layer, understand MeatyPrompts layered architecture.

**How to use**:

```python
from symbol_tools import search_patterns

# Find all service layer classes
services = search_patterns(pattern="Service", layer="service", domain="api")

# Find router endpoints
routers = search_patterns(pattern="router|Router", layer="router")

# Find React components following naming pattern
components = search_patterns(pattern="^[A-Z].*Card", layer="component", domain="ui")
```

**Parameters**:
- `pattern` (required) - Search pattern (supports regex)
- `layer` (optional) - Architectural layer: router, service, repository, component, hook, util
- `priority` (optional) - Priority filter: high, medium, low
- `domain` (optional) - Domain filter: ui, api, shared
- `limit` (optional) - Maximum results (default: 30)

**Returns**: List of matching symbols with layer and priority information.

**Architectural layers**: Validates MeatyPrompts pattern (Router → Service → Repository → DB)

### 4. Get Symbol Context

Get full context for a specific symbol including definition location and related symbols.

**When to use**: Need detailed information about a specific symbol, want to find related symbols (props interfaces, same-file symbols).

**How to use**:

```python
from symbol_tools import get_symbol_context

# Get full context for a component (includes props interface)
context = get_symbol_context(name="PromptCard", include_related=True)

# Get service definition with related symbols
service = get_symbol_context(
    name="PromptService",
    file="services/api/app/services/prompt_service.py",
    include_related=True
)
```

**Parameters**:
- `name` (required) - Exact symbol name
- `file` (optional) - File path if name is ambiguous
- `include_related` (optional) - Include related symbols (imports, usages, props) (default: false)

**Returns**: Dict with symbol info and optionally related symbols array.

**Relationship detection**: Automatically finds props interfaces for components, same-file symbols.

### 5. Update Symbols

Trigger symbol graph regeneration or incremental update (delegated to symbols-engineer agent).

**When to use**: After significant code changes, when symbol files are out of sync with codebase.

**Primary approach - Use symbols-engineer agent**:

```markdown
Task("symbols-engineer", "Update symbols for the API domain after schema changes")
Task("symbols-engineer", "Perform incremental symbol update for recent file changes")
Task("symbols-engineer", "Regenerate full symbol graph and re-chunk by domain")
```

The `symbols-engineer` agent handles:
- Analyzing code changes and determining scope of updates
- Running programmatic symbol extraction using domain-specific scripts
- Merging extracted symbols into existing graphs
- Re-chunking symbols by domain for optimal loading
- Validation of symbol accuracy and completeness

**Alternative - Manual slash commands**:

If using slash commands directly (less recommended):
- `/symbols-update` - Trigger incremental or full update
- `/symbols-chunk` - Re-chunk updated symbols by domain

**Programmatic approach** (for advanced use):

Symbol extraction can also be done programmatically using scripts:

```python
from symbol_tools import update_symbols

# Incremental update for recent changes
result = update_symbols(mode="incremental")

# Full regeneration (use sparingly)
result = update_symbols(mode="full", chunk=True)

# Update specific domain only
result = update_symbols(mode="domain", domain="ui")
```

**Parameters**:
- `mode` (optional) - Update mode: full, incremental, domain (default: incremental)
- `domain` (optional) - Specific domain to update (for domain mode)
- `files` (optional) - Specific files to update (for incremental mode)
- `chunk` (optional) - Re-chunk symbols after update (default: true)

**Note**: This function provides the interface but delegates to symbols-engineer agent for orchestration.

## Quick Start Workflow

### Frontend Development Workflow

```python
from symbol_tools import query_symbols, load_domain, get_symbol_context

# 1. Find existing React hooks in frontend app
hooks = query_symbols(kind="hook", domain="web", limit=20)

# 2. Find similar components in UI library
similar = query_symbols(name="Card", kind="component", domain="ui", limit=10)

# 3. Load web domain context for frontend patterns
web_symbols = load_domain(domain="web", max_symbols=100)

# 4. Find existing API hooks (useContexts, useAgents, etc)
api_hooks = query_symbols(path="hooks/queries", domain="web")

# 5. Check shared types and interfaces
types = query_symbols(path="types", kind="interface", domain="web")
```

**Result**: ~100 symbols loaded (~15KB) instead of full 447KB graph = 97% reduction

### Backend Development Workflow

```python
from symbol_tools import load_domain, search_patterns, query_symbols

# 1. Load API layer symbols
api_symbols = load_domain(domain="api", max_symbols=50)

# 2. Find similar routers
routers = search_patterns(pattern="router", layer="router", domain="api")

# 3. Find service layer patterns
services = search_patterns(pattern="Service", layer="service", domain="api")

# 4. Load shared DTOs and types
dtos = query_symbols(path="schemas", kind="class", domain="api")
```

**Result**: ~50 symbols loaded (~8KB) for complete API context

### Debugging Workflow

```python
from symbol_tools import get_symbol_context, load_domain, query_symbols

# 1. Load component and related symbols
component = get_symbol_context(name="PromptCard", include_related=True)

# 2. Load test context to understand test cases
tests = load_domain(domain="ui", include_tests=True, max_symbols=30)

# 3. Search for related hooks in frontend app
hooks = query_symbols(path="hooks", name="prompt", kind="hook", domain="web")

# 4. Find state management patterns
state = query_symbols(path="contexts", kind="function", domain="web")

# 5. Find API client integration points
api_clients = query_symbols(path="lib/api", kind="function", domain="web")
```

**Result**: Full context including tests and frontend patterns loaded (~20KB instead of reading all files)

## Progressive Loading Strategy

Follow this three-tier approach for optimal token efficiency:

**Tier 1: Essential Context (25-30% of budget)**
- Load 10-20 symbols directly related to current task
- Focus on interfaces, types, and primary components/services
- Use: `query_symbols(name="PromptCard", limit=10)`

**Tier 2: Supporting Context (15-20% of budget)**
- Load related patterns and utilities
- Include cross-domain interfaces
- Use: `load_domain(domain="shared", max_symbols=50)`

**Tier 3: On-Demand Context (remaining budget)**
- Specific lookups when needed
- Deep dependency analysis
- Use: `get_symbol_context(name="Service", include_related=True)`

## Programmatic Symbol Extraction

Symbol graph updates can be performed programmatically using domain-specific extraction scripts. These scripts reduce manual work by automatically pulling structural information and summaries from code, allowing the symbols-engineer agent to focus on refinement.

### Available Extraction Scripts

**Python Symbol Extractor** (`scripts/extract_symbols_python.py`):
- Extracts Python modules, classes, functions, methods
- Pulls function signatures and docstrings
- Filters out test files and internal imports
- Supports batch processing for entire directories
- Output: JSON-compatible symbol metadata

Usage:
```bash
python .claude/skills/symbols/scripts/extract_symbols_python.py services/api/app
```

**TypeScript/JavaScript Symbol Extractor** (`scripts/extract_symbols_typescript.py`):
- Extracts TypeScript interfaces, types, functions, classes
- Extracts React components and hooks
- Parses JSDoc comments for summaries
- Handles monorepo structure (apps/web, packages/ui)
- Output: JSON-compatible symbol metadata

Usage:
```bash
python .claude/skills/symbols/scripts/extract_symbols_typescript.py apps/web/src
```

**Symbol Merger** (`scripts/merge_symbols.py`):
- Merges programmatically extracted symbols into existing graphs
- Handles incremental updates
- Maintains symbol relationships and cross-references
- Validates for consistency and duplicates

Usage:
```bash
python .claude/skills/symbols/scripts/merge_symbols.py --domain=api --input=extracted_symbols.json
```

### Workflow: Programmatic Updates

1. **Analyze changes**: Determine which domains/files changed
2. **Extract symbols**: Run domain-specific extractor on changed files
3. **Merge results**: Use symbol merger to integrate with existing graph
4. **Validate**: Verify accuracy and completeness
5. **Chunk**: Re-chunk symbols by domain for optimal loading

**Recommended**: Use `symbols-engineer` agent to orchestrate this workflow.

## Symbol Structure Reference

Symbols are stored in domain-specific JSON files in the `ai/` directory:

**Main symbol files**:
- `ai/symbols-ui.json` (191KB) - UI primitives from packages/ui
- `ai/symbols-web.json` (629KB) - Frontend app (apps/web: hooks, pages, components, types)
- `ai/symbols-api.json` (1.6MB) - Backend services, routers, repositories
- `ai/symbols-shared.json` - Currently mapped to symbols-web.json (pending separate file creation)

**Test symbol files** (load separately):
- `ai/symbols-ui-tests.json` (77KB)
- `ai/symbols-api-tests.json` (1.7MB)
- `ai/symbols-shared-tests.json` (pending creation)

**Complete reference**:
- `ai/symbols.graph.json` (447KB) - Complete codebase (rarely needed)

**Symbol kinds**:
- `component` - React components
- `hook` - React hooks (useState, useEffect, custom hooks)
- `function` - Regular functions and arrow functions
- `class` - Class declarations
- `method` - Class methods
- `interface` - TypeScript interfaces
- `type` - TypeScript type aliases

## Resources

### scripts/symbol_tools.py

Python implementation of all symbol query functions. Contains:
- `query_symbols()` - Query by name, kind, domain, path
- `load_domain()` - Load complete domain context
- `search_patterns()` - Pattern-based search with layer awareness
- `get_symbol_context()` - Get specific symbol with related symbols
- `update_symbols()` - Trigger regeneration

Execute directly or import functions as needed:

```bash
# Run examples
python .claude/skills/symbols/scripts/symbol_tools.py
```

```python
# Import in code
from symbol_tools import query_symbols, load_domain
```

### references/usage_patterns.md

Detailed examples and patterns for common development scenarios:
- Frontend development examples
- Backend API development examples
- Cross-domain development patterns
- Debugging workflows
- Token efficiency guidelines
- Integration patterns with agents

Read this reference for comprehensive examples of each workflow type.

### references/architecture_integration.md

Deep dive into MeatyPrompts architecture integration:
- Symbol structure specification
- Layered architecture mapping (Router → Service → Repository → DB)
- Symbol relationship analysis
- Development workflow integration
- Regeneration and update strategies
- Slash command integration
- Agent integration patterns
- Configuration reference

Read this reference to understand how symbols map to MeatyPrompts architectural patterns.

## Integration with MeatyPrompts

### Slash Commands

The symbols skill wraps these MeatyPrompts slash commands:
- `/symbols-query` - Query implementation
- `/symbols-search` - Search implementation
- `/load-symbols` - Domain loading implementation
- `/symbols-update` - Update implementation
- `/symbols-chunk` - Chunking implementation

### Related Agents

- `symbols-engineer` - Expert in symbol optimization and graph management
- `ui-engineer-enhanced` - Uses symbols for frontend work
- `codebase-explorer` - Uses symbols for efficient code discovery

### MeatyPrompts Architecture

Symbols understand and validate MeatyPrompts layered architecture:
- **Router layer** - HTTP endpoints, validation
- **Service layer** - Business logic, DTO mapping
- **Repository layer** - Database operations, RLS
- **Component layer** - UI components from `@meaty/ui`
- **Hook layer** - React hooks and state management
- **Util layer** - Shared utilities and helpers

Use `search_patterns()` with `layer` parameter to filter by architectural layer.

## Performance

**Token Efficiency Gains**:
- Full graph: 447KB (avoid loading)
- UI domain only: 191KB (57% reduction)
- Web domain only: 629KB (29% reduction) - Complete frontend app coverage
- API domain only: 1.6MB (larger due to comprehensive backend coverage)
- Shared domain: Maps to web (pending separate file)
- Typical query: 10-20 symbols (~2-5KB, 99% reduction)

**Progressive Loading Example**:
1. Essential context: 20 symbols = ~5KB (99% reduction vs full graph)
2. Supporting context: +30 symbols = ~12KB total (97% reduction)
3. On-demand lookup: +10 symbols = ~15KB total (97% reduction)

**Comparison to loading full files**:
- Loading full files for context: ~200KB+
- Using symbol skill: ~15KB
- **Efficiency gain: 93%**
