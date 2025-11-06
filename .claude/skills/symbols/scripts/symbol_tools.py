#!/usr/bin/env python3
"""
Symbol Tools - Intelligent codebase symbol analysis

Provides token-efficient access to MeatyPrompts codebase symbols through
pre-generated symbol graphs that are chunked by domain and separated from tests.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal

# Base path to symbol files
SYMBOLS_DIR = Path("ai")

# Available symbol files
SYMBOL_FILES = {
    "ui": SYMBOLS_DIR / "symbols-ui.json",
    "web": SYMBOLS_DIR / "symbols-web.json",  # Frontend app (apps/web)
    "api": SYMBOLS_DIR / "symbols-api.json",
    "shared": SYMBOLS_DIR / "symbols-web.json",  # Map to web until separate file created
    "ui-tests": SYMBOLS_DIR / "symbols-ui-tests.json",
    "api-tests": SYMBOLS_DIR / "symbols-api-tests.json",
    "shared-tests": SYMBOLS_DIR / "symbols-shared-tests.json",
    "full": SYMBOLS_DIR / "symbols.graph.json",
}


def _normalize_symbol_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize symbol data to handle both schema formats.

    Converts flat schema {"symbols": [...]} to hierarchical schema
    {"modules": [{"path": "...", "symbols": [...]}]} format.

    Returns list of modules in hierarchical format.
    """
    # Check if already hierarchical format
    if "modules" in data:
        return data["modules"]

    # Convert flat format to hierarchical
    if "symbols" in data:
        # Group symbols by path
        modules_dict = {}
        for symbol in data["symbols"]:
            path = symbol.get("path", "unknown")
            if path not in modules_dict:
                modules_dict[path] = {
                    "path": path,
                    "symbols": []
                }
            # Create symbol without "path" key since it's in module
            symbol_copy = {k: v for k, v in symbol.items() if k != "path"}
            modules_dict[path]["symbols"].append(symbol_copy)

        return list(modules_dict.values())

    return []


def query_symbols(
    name: Optional[str] = None,
    kind: Optional[str] = None,
    domain: Optional[str] = None,
    path: Optional[str] = None,
    limit: int = 20,
    summary_only: bool = False,
) -> List[Dict[str, Any]]:
    """
    Query symbols by name, kind, domain, or path without loading entire graph.

    Args:
        name: Symbol name (supports partial/fuzzy matching)
        kind: Symbol kind (component, hook, function, class, interface, type, method)
        domain: Domain filter (ui, api, shared)
        path: File path pattern (e.g., "components", "hooks", "services")
        limit: Maximum results to return (default: 20)
        summary_only: Return only name and summary (default: False)

    Returns:
        List of matching symbols with file path, line number, and summary
    """
    results = []
    domains_to_search = [domain.lower()] if domain else ["ui", "web", "api", "shared"]

    for domain_name in domains_to_search:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            # Path filter
            if path and path.lower() not in module["path"].lower():
                continue

            for symbol in module.get("symbols", []):
                # Name filter (fuzzy match)
                if name and name.lower() not in symbol["name"].lower():
                    continue

                # Kind filter
                if kind and symbol["kind"] != kind.lower():
                    continue

                # Build result
                result = {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain_name.upper(),
                    "summary": symbol.get("summary", ""),
                }

                if summary_only:
                    result = {"name": result["name"], "summary": result["summary"]}

                results.append(result)

                if len(results) >= limit:
                    return results

    return results


def load_domain(
    domain: Literal["ui", "web", "api", "shared"],
    include_tests: bool = False,
    max_symbols: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Load complete symbol set for a specific domain.

    Args:
        domain: Domain to load (ui, web, api, shared)
        include_tests: Include test file symbols (default: False)
        max_symbols: Limit number of symbols returned (default: all)

    Returns:
        Dict with domain, type, totalSymbols, and symbols array
    """
    domain = domain.lower()
    main_file = SYMBOL_FILES.get(domain)
    test_file = SYMBOL_FILES.get(f"{domain}-tests")

    if not main_file or not main_file.exists():
        raise FileNotFoundError(f"Symbol file for domain '{domain}' not found")

    with open(main_file) as f:
        main_data = json.load(f)

    # Normalize data to handle both flat and hierarchical schemas
    main_modules = _normalize_symbol_data(main_data)

    # Collect all symbols
    all_symbols = []
    for module in main_modules:
        for symbol in module.get("symbols", []):
            all_symbols.append(
                {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain.upper(),
                    "summary": symbol.get("summary", ""),
                }
            )

    # Add test symbols if requested
    if include_tests and test_file and test_file.exists():
        with open(test_file) as f:
            test_data = json.load(f)

        # Normalize test data
        test_modules = _normalize_symbol_data(test_data)

        for module in test_modules:
            for symbol in module.get("symbols", []):
                all_symbols.append(
                    {
                        "kind": symbol["kind"],
                        "name": symbol["name"],
                        "line": symbol["line"],
                        "file": module["path"],
                        "domain": domain.upper(),
                        "summary": symbol.get("summary", ""),
                        "test": True,
                    }
                )

    # Apply limit if specified
    if max_symbols:
        all_symbols = all_symbols[:max_symbols]

    return {
        "domain": domain.upper(),
        "type": "MAIN" if not include_tests else "MAIN+TESTS",
        "totalSymbols": len(all_symbols),
        "symbols": all_symbols,
    }


def search_patterns(
    pattern: str,
    layer: Optional[str] = None,
    priority: Optional[str] = None,
    domain: Optional[str] = None,
    limit: int = 30,
) -> List[Dict[str, Any]]:
    """
    Advanced pattern-based search with architectural layer awareness.

    Args:
        pattern: Search pattern (supports regex)
        layer: Architectural layer (router, service, repository, component, hook, util)
        priority: Priority filter (high, medium, low)
        domain: Domain filter (ui, api, shared)
        limit: Maximum results (default: 30)

    Returns:
        List of matching symbols with layer and priority information
    """
    # Compile regex pattern
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        # If pattern is not valid regex, treat as literal string
        regex = re.compile(re.escape(pattern), re.IGNORECASE)

    # Layer to kind/path mapping
    layer_mapping = {
        "router": {"kinds": ["function", "class"], "paths": ["router", "routes"]},
        "service": {"kinds": ["class", "function"], "paths": ["service"]},
        "repository": {"kinds": ["class"], "paths": ["repository", "repo"]},
        "component": {"kinds": ["component"], "paths": ["component"]},
        "hook": {"kinds": ["hook"], "paths": ["hook"]},
        "util": {"kinds": ["function", "class"], "paths": ["util", "helper"]},
    }

    results = []
    domains_to_search = [domain.lower()] if domain else ["ui", "web", "api", "shared"]

    for domain_name in domains_to_search:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            for symbol in module.get("symbols", []):
                # Pattern match on name
                if not regex.search(symbol["name"]):
                    continue

                # Layer filter
                if layer:
                    layer_config = layer_mapping.get(layer.lower(), {})
                    kinds = layer_config.get("kinds", [])
                    paths = layer_config.get("paths", [])

                    # Check kind match
                    if symbol["kind"] not in kinds:
                        continue

                    # Check path match
                    if paths and not any(p in module["path"].lower() for p in paths):
                        continue

                # Determine priority based on naming conventions
                detected_priority = "medium"
                if any(
                    x in symbol["name"].lower()
                    for x in ["service", "router", "repository"]
                ):
                    detected_priority = "high"
                elif any(x in symbol["name"].lower() for x in ["util", "helper"]):
                    detected_priority = "low"

                # Priority filter
                if priority and detected_priority != priority.lower():
                    continue

                # Detect layer from path/kind
                detected_layer = None
                for layer_name, config in layer_mapping.items():
                    if symbol["kind"] in config["kinds"]:
                        if any(p in module["path"].lower() for p in config["paths"]):
                            detected_layer = layer_name
                            break

                result = {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain_name.upper(),
                    "summary": symbol.get("summary", ""),
                    "layer": detected_layer,
                    "priority": detected_priority,
                }

                results.append(result)

                if len(results) >= limit:
                    return results

    return results


def get_symbol_context(
    name: str,
    file: Optional[str] = None,
    include_related: bool = False,
) -> Dict[str, Any]:
    """
    Get full context for a specific symbol including definition location and related symbols.

    Args:
        name: Exact symbol name
        file: File path if name is ambiguous
        include_related: Include related symbols (imports, usages) (default: False)

    Returns:
        Dict with symbol info and optionally related symbols
    """
    # Search all domains for the symbol
    found_symbol = None
    found_module = None
    found_domain = None

    for domain_name in ["ui", "web", "api", "shared"]:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            # File filter if provided
            if file and file not in module["path"]:
                continue

            for symbol in module.get("symbols", []):
                if symbol["name"] == name:
                    found_symbol = symbol
                    found_module = module
                    found_domain = domain_name
                    break

            if found_symbol:
                break

        if found_symbol:
            break

    if not found_symbol:
        return {"error": f"Symbol '{name}' not found"}

    result = {
        "symbol": {
            "kind": found_symbol["kind"],
            "name": found_symbol["name"],
            "line": found_symbol["line"],
            "file": found_module["path"],
            "domain": found_domain.upper(),
            "summary": found_symbol.get("summary", ""),
        }
    }

    # Find related symbols if requested
    if include_related:
        related = []

        # Look for related symbols in the same file
        for symbol in found_module.get("symbols", []):
            if symbol["name"] != name:
                related.append(
                    {
                        "kind": symbol["kind"],
                        "name": symbol["name"],
                        "line": symbol["line"],
                        "summary": symbol.get("summary", ""),
                        "relation": "same-file",
                    }
                )

        # Look for Props interface for components
        if found_symbol["kind"] == "component":
            props_name = f"{name}Props"
            props_results = query_symbols(name=props_name, kind="interface", limit=5)
            for props in props_results:
                related.append(
                    {
                        "kind": props["kind"],
                        "name": props["name"],
                        "line": props["line"],
                        "file": props["file"],
                        "summary": props["summary"],
                        "relation": "props-interface",
                    }
                )

        result["related"] = related

    return result


def update_symbols(
    mode: Literal["full", "incremental", "domain"] = "incremental",
    domain: Optional[str] = None,
    files: Optional[List[str]] = None,
    chunk: bool = True,
) -> Dict[str, Any]:
    """
    Trigger symbol graph regeneration or incremental update.

    Note: This function provides the interface but delegates to existing
    slash commands for actual implementation.

    Args:
        mode: Update mode (full, incremental, domain)
        domain: Specific domain to update (for domain mode)
        files: Specific files to update (for incremental mode)
        chunk: Re-chunk symbols after update (default: True)

    Returns:
        Dict with update results
    """
    # This would integrate with existing slash commands:
    # /symbols-update, /symbols-chunk
    return {
        "note": "Use /symbols-update and /symbols-chunk slash commands",
        "mode": mode,
        "domain": domain,
        "files": files,
        "chunk": chunk,
    }


if __name__ == "__main__":
    # Example usage
    print("Symbol Tools - Example Usage\n")

    # Query components with 'Card' in name
    print("1. Query UI components with 'Card' in name:")
    results = query_symbols(name="Card", kind="component", domain="ui", limit=5)
    for r in results:
        print(f"  - {r['name']} ({r['file']}:{r['line']})")

    # Load API domain
    print("\n2. Load API domain (first 10 symbols):")
    api_data = load_domain(domain="api", max_symbols=10)
    print(f"  Total: {api_data['totalSymbols']} symbols")
    for s in api_data["symbols"][:3]:
        print(f"  - {s['name']} ({s['kind']})")

    # Search for services
    print("\n3. Search for service layer classes:")
    services = search_patterns(pattern="Service", layer="service", limit=5)
    for s in services:
        print(f"  - {s['name']} ({s['file']}:{s['line']})")
