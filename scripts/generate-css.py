#!/usr/bin/env python3
"""Generate CSS files from palette.json source of truth."""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
COLORS_DIR = REPO_ROOT / "assets" / "colors"
PALETTE_JSON = COLORS_DIR / "palette.json"


def load_palette() -> dict:
    """Load palette.json."""
    with open(PALETTE_JSON) as f:
        return json.load(f)


def generate_theme_css(theme_id: str, theme: dict) -> str:
    """Generate CSS for a single theme."""
    lines = [
        f"/* {theme['name']} - {theme['mode']} mode */",
        f"/* Generated from palette.json - do not edit directly */",
        "",
        ":root {",
    ]

    for name, value in theme["colors"].items():
        lines.append(f"  --color-{name}: {value};")

    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def generate_tokens_css(palette: dict) -> str:
    """Generate tokens.css with all themes as data attributes."""
    lines = [
        "/* Brand Color Tokens */",
        "/* Generated from palette.json - do not edit directly */",
        "/* Usage: <html data-theme=\"deep-water\"> or <html data-theme=\"twilight-light\"> */",
        "",
    ]

    # Default theme
    default_id = palette["current"]
    default_theme = palette["themes"][default_id]
    lines.append("/* Default theme (no data-theme attribute) */")
    lines.append(":root {")
    for name, value in default_theme["colors"].items():
        lines.append(f"  --color-{name}: {value};")
    lines.append("}")
    lines.append("")

    # Semantic colors (always available)
    lines.append("/* Semantic colors */")
    lines.append(":root {")
    for name, value in palette["semantic"].items():
        lines.append(f"  --color-{name}: {value};")
    lines.append("}")
    lines.append("")

    # All themes via data attribute
    for theme_id, theme in palette["themes"].items():
        lines.append(f"/* {theme['name']} */")
        lines.append(f'[data-theme="{theme_id}"] {{')
        for name, value in theme["colors"].items():
            lines.append(f"  --color-{name}: {value};")
        lines.append("}")
        lines.append("")

    # Auto dark/light mode
    lines.append("/* Auto mode - respects system preference */")
    lines.append("@media (prefers-color-scheme: light) {")
    lines.append('  [data-theme="auto"] {')
    light_theme = palette["themes"].get(f"{default_id}-light", palette["themes"][default_id])
    for name, value in light_theme["colors"].items():
        lines.append(f"    --color-{name}: {value};")
    lines.append("  }")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def generate_individual_css(palette: dict) -> dict[str, str]:
    """Generate individual CSS files for each theme."""
    files = {}
    for theme_id, theme in palette["themes"].items():
        files[f"{theme_id}.css"] = generate_theme_css(theme_id, theme)
    return files


def main():
    palette = load_palette()

    # Generate tokens.css (all-in-one)
    tokens_css = generate_tokens_css(palette)
    tokens_path = COLORS_DIR / "tokens.css"
    tokens_path.write_text(tokens_css)
    print(f"Generated: {tokens_path}")

    # Generate individual theme files
    individual = generate_individual_css(palette)
    for filename, content in individual.items():
        filepath = COLORS_DIR / filename
        filepath.write_text(content)
        print(f"Generated: {filepath}")

    print(f"\nGenerated {1 + len(individual)} CSS files from palette.json")


if __name__ == "__main__":
    main()
