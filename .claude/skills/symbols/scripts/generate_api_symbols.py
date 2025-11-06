#!/usr/bin/env python3
"""
Generate API Symbol Artifacts

Extracts Python symbols from services/api and separates them into:
- symbols-api.json: Business logic (routers, services, repositories, schemas)
- symbols-api-tests.json: Test files
- symbols-api-scripts.json: Utility scripts and migrations

Usage:
    python generate_api_symbols.py [--output-dir=ai/]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

# Add parent directory to path to import extract_symbols_python
sys.path.insert(0, str(Path(__file__).parent))

from extract_symbols_python import (
    extract_symbols_from_directory,
    Symbol,
    categorize_file
)


def separate_symbols_by_category(symbols: List[Symbol]) -> Dict[str, List[Symbol]]:
    """
    Separate symbols into categories for different output files.

    Returns:
        Dict with keys: 'business_logic', 'test', 'script'
    """
    categorized = {
        'business_logic': [],
        'test': [],
        'script': []
    }

    for symbol in symbols:
        category = symbol.file_category

        if category == 'test':
            categorized['test'].append(symbol)
        elif category in ['script', 'migration', 'config']:
            categorized['script'].append(symbol)
        else:
            # router, service, repository, schema, business_logic
            categorized['business_logic'].append(symbol)

    return categorized


def symbols_to_output_format(
    symbols: List[Symbol],
    domain: str,
    category: str
) -> Dict[str, Any]:
    """Convert symbols to output format grouped by file path."""
    # Group symbols by file path
    modules = defaultdict(list)

    for symbol in symbols:
        symbol_dict = {
            "name": symbol.name,
            "kind": symbol.kind,
            "line": symbol.line,
            "signature": symbol.signature,
            "summary": symbol.summary,
        }

        # Add optional fields if present
        if symbol.parent:
            symbol_dict["parent"] = symbol.parent
        if symbol.expected_response:
            symbol_dict["expected_response"] = symbol.expected_response
        if symbol.decorators:
            symbol_dict["decorators"] = symbol.decorators
        if symbol.docstring:
            symbol_dict["docstring"] = symbol.docstring
        if symbol.file_category:
            symbol_dict["file_category"] = symbol.file_category

        modules[symbol.path].append(symbol_dict)

    # Build output structure
    module_list = []
    for path, syms in sorted(modules.items()):
        module_list.append({
            "path": path,
            "symbols": syms
        })

    return {
        "version": "1.0",
        "domain": domain,
        "category": category,
        "language": "python",
        "totalModules": len(module_list),
        "totalSymbols": len(symbols),
        "modules": module_list
    }


def main():
    """Main entry point."""
    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent.parent  # Up to meatyprompts/

    # API directory
    api_dir = project_root / "services" / "api"

    if not api_dir.exists():
        print(f"Error: API directory not found: {api_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting symbols from {api_dir}", file=sys.stderr)

    # Extract all symbols (including tests)
    all_symbols = extract_symbols_from_directory(
        api_dir,
        exclude_tests=False,
        exclude_private=False
    )

    print(f"Extracted {len(all_symbols)} total symbols", file=sys.stderr)

    # Separate symbols by category
    categorized = separate_symbols_by_category(all_symbols)

    print(f"  Business logic: {len(categorized['business_logic'])} symbols", file=sys.stderr)
    print(f"  Tests: {len(categorized['test'])} symbols", file=sys.stderr)
    print(f"  Scripts/Migrations: {len(categorized['script'])} symbols", file=sys.stderr)

    # Output directory
    output_dir = project_root / "ai"
    output_dir.mkdir(exist_ok=True)

    # Generate artifact files
    artifacts = {
        'symbols-api.json': ('api', 'business_logic', categorized['business_logic']),
        'symbols-api-tests.json': ('api', 'test', categorized['test']),
        'symbols-api-scripts.json': ('api', 'script', categorized['script']),
    }

    for filename, (domain, category, symbols) in artifacts.items():
        if not symbols:
            print(f"Skipping {filename} (no symbols)", file=sys.stderr)
            continue

        output_file = output_dir / filename
        output_data = symbols_to_output_format(symbols, domain, category)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)

        file_size = output_file.stat().st_size / 1024
        print(f"✓ Generated {filename} ({file_size:.1f}KB, {len(symbols)} symbols)", file=sys.stderr)

    print("\nSymbol extraction complete!", file=sys.stderr)


if __name__ == '__main__':
    main()
