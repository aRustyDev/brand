#!/usr/bin/env python3
"""Generate consumer-ready CSS theme files from palette.json.

Each theme gets a single CSS file with standard light/dark selectors
that consumers can import directly.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
COLORS_DIR = REPO_ROOT / "assets" / "colors"
THEMES_DIR = COLORS_DIR / "themes"
PALETTE_JSON = COLORS_DIR / "palette.json"


def load_palette() -> dict:
    """Load palette.json."""
    with open(PALETTE_JSON) as f:
        return json.load(f)


def generate_consumer_css(base_theme_id: str, palette: dict) -> str:
    """Generate consumer-ready CSS with light/dark selectors.

    Args:
        base_theme_id: The base theme name (e.g., 'forest-night')
        palette: The full palette dict

    Returns:
        CSS string with :root/light and dark selectors
    """
    dark_theme = palette["themes"].get(base_theme_id)
    light_theme = palette["themes"].get(f"{base_theme_id}-light")

    if not dark_theme or not light_theme:
        raise ValueError(f"Missing dark or light variant for {base_theme_id}")

    semantic = palette.get("semantic", {})

    lines = [
        f"/* {dark_theme['name']} Theme */",
        f"/* Generated from palette.json - do not edit directly */",
        f"/* Import: @import url('https://brand.arusty.dev/assets/colors/themes/{base_theme_id}.css'); */",
        "",
        "/* Light mode (default) */",
        ":root,",
        '[data-theme="light"] {',
    ]

    for name, value in light_theme["colors"].items():
        lines.append(f"  --color-{name}: {value};")

    # Add semantic colors
    if semantic:
        lines.append("")
        lines.append("  /* Semantic */")
        for name, value in semantic.items():
            lines.append(f"  --color-{name}: {value};")

    lines.append("}")
    lines.append("")
    lines.append("/* Dark mode */")
    lines.append('[data-theme="dark"] {')

    for name, value in dark_theme["colors"].items():
        lines.append(f"  --color-{name}: {value};")

    lines.append("}")
    lines.append("")

    # Add prefers-color-scheme for auto behavior
    lines.append("/* Auto dark mode (respects system preference when no data-theme set) */")
    lines.append("@media (prefers-color-scheme: dark) {")
    lines.append("  :root:not([data-theme]) {")

    for name, value in dark_theme["colors"].items():
        lines.append(f"    --color-{name}: {value};")

    lines.append("  }")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def get_base_themes(palette: dict) -> list[str]:
    """Get list of base theme IDs (excluding -light variants)."""
    return [
        theme_id for theme_id in palette["themes"].keys()
        if not theme_id.endswith("-light")
    ]


def main():
    palette = load_palette()

    # Ensure themes directory exists
    THEMES_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old files in themes dir
    for old_file in THEMES_DIR.glob("*.css"):
        old_file.unlink()
        print(f"Removed: {old_file}")

    # Generate consumer-ready theme files
    base_themes = get_base_themes(palette)

    for theme_id in base_themes:
        css_content = generate_consumer_css(theme_id, palette)
        filepath = THEMES_DIR / f"{theme_id}.css"
        filepath.write_text(css_content)
        print(f"Generated: {filepath}")

    print(f"\nGenerated {len(base_themes)} theme files in {THEMES_DIR}")
    print("\nUsage:")
    print(f'  @import url("https://brand.arusty.dev/assets/colors/themes/{palette["current"]}.css");')


if __name__ == "__main__":
    main()
