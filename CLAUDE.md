# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an **AI Scratchpad** - a general sandbox workspace for prototyping and developing smaller projects before they mature into standalone repositories. Nested CLAUDE.md files in project subdirectories provide project-specific guidance.

## Repository Structure

```
ai-scratchpad/
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # Specialized agent definitions
│   ├── commands/               # Custom slash commands
│   ├── skills/                 # Project skills
│   └── specs/                  # CLAUDE.md specification files
├── knit-wit/                   # Crochet pattern generator project
│   └── CLAUDE.md              # Project-specific guidance
└── [future projects]/          # Additional prototypes and experiments
```

## Working with Multiple Projects

Since this is a sandbox for multiple projects:

1. **Check for nested CLAUDE.md files** - Each project directory may have its own CLAUDE.md with specific guidance
2. **Scope commands appropriately** - When working in a subdirectory, respect project-specific conventions
3. **Isolate dependencies** - Projects should be self-contained where possible
4. **Project maturity varies** - Some projects are early prototypes, others are production-ready

## Active Projects

### knit-wit (Crochet Pattern Generator)
- **Location**: `knit-wit/`
- **Status**: Active Development (MVP Phase)
- **Description**: Mobile-first web app for generating parametric crochet patterns with interactive visualization
- **Stack**: React Native/Expo (frontend), FastAPI (backend), Python (pattern engine)
- **Guidance**: See `knit-wit/CLAUDE.md` for detailed project-specific information

## General Development Practices

### Task Management
- Use `TodoWrite` tool for multi-step work to track progress
- Update todos as work progresses
- Clean up completed todos at session end

### Exploration Strategy
- Use `codebase-explorer` agent for quick pattern discovery (symbols-based, fast)
- Use `explore` agent for deep analysis when needed
- Prefer symbol-based queries before reading full files

### Documentation vs AI Artifacts
| Type | Audience | Location | Agent |
|------|----------|----------|-------|
| Documentation | Humans | `docs/`, READMEs | `documentation-writer` |
| AI Artifacts | AI agents | `.claude/`, `ai/` | `ai-artifacts-engineer` |

### Git Workflow
- Use conventional commit messages: `type(scope): message`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
- Include Claude Code attribution in commits
- Never commit secrets or sensitive data

### Code Review Expectations
- Prefer refactoring over new code when possible
- Justify new patterns with clear rationale
- Test coverage: Unit (60%+), Integration (30%+), E2E (10%+)
- Follow project-specific patterns (see nested CLAUDE.md files)

## Professional Objectivity

Prioritize technical accuracy over validation:
- Use objective language ("The implementation shows..." not "I think...")
- State facts with rationale
- Disagree when necessary with technical justification
- Avoid excessive praise or emotional validation

## Tool Usage Best Practices

### Specialized Tools Priority
```
File search    → Glob (NOT find)
Content search → Grep (NOT grep/rg)
Read files     → Read (NOT cat/head/tail)
Edit files     → Edit (NOT sed/awk)
Write files    → Write (NOT echo >)
Terminal ops   → Bash (git, npm, docker, etc.)
```

### Agent Delegation
| Task | Agent | Why |
|------|-------|-----|
| Find patterns | `codebase-explorer` | Fast symbol queries |
| Deep analysis | `explore` | Full context needed |
| Most docs | `documentation-writer` | Cost-efficient (Haiku) |
| Complex docs | `documentation-complex` | Multi-system integration (Sonnet) |
| AI artifacts | `ai-artifacts-engineer` | Skills, agents, context |

## Skills Available

The `.claude/skills/` directory contains project skills:
- **symbols**: Token-efficient codebase navigation via symbol graphs
- **skill-creator**: Guide for creating new Claude Code skills

Use `/` slash commands to access custom skills and commands.

## Environment

This repository uses:
- **Package Manager**: Context-dependent (varies by project)
- **Version Control**: Git + GitHub
- **CI/CD**: Varies by project (see nested CLAUDE.md files)

## Getting Started with a New Project

When Claude Code encounters a subdirectory you haven't worked in:

1. **Check for CLAUDE.md** in that directory first
2. **Read project documentation** (README.md, docs/)
3. **Explore with symbols** if available (use `codebase-explorer` agent)
4. **Ask questions** if requirements unclear (use `AskUserQuestion` tool)
5. **Plan work** using `TodoWrite` for multi-step tasks

## Notes on This Repository

- **No emojis** unless explicitly requested
- **Concise communication** - CLI-appropriate, markdown formatted
- **Direct, objective** - technical accuracy over pleasantries
- **Tool-appropriate** - use specialized tools instead of bash when possible
- **Context-aware** - respect project-specific conventions in subdirectories
