# =============================================================================
# Brand Assets Build & Development
# =============================================================================

set dotenv-load := true

# Default recipe - show help
default:
    @just --list

# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------

# Generate CSS from palette.json
generate-css:
    @python3 scripts/generate-css.py

# Build public/ directory for deployment
build: clean generate-css
    @echo "Building public/..."
    @mkdir -p public
    @cp -r assets public/
    @cp -r docs public/ 2>/dev/null || true
    @cp index.html public/ 2>/dev/null || true
    @echo "Build complete: public/"

# Remove build artifacts
clean:
    @rm -rf public

# -----------------------------------------------------------------------------
# Development
# -----------------------------------------------------------------------------

# Serve locally for development
serve: build
    @echo "Serving at http://localhost:8787"
    @npx wrangler pages dev public

# Open palette preview in browser
palette:
    @open docs/palette-preview.html 2>/dev/null || xdg-open docs/palette-preview.html

# -----------------------------------------------------------------------------
# Deployment
# -----------------------------------------------------------------------------

# Deploy to Cloudflare Pages
deploy: build
    @npx wrangler pages deploy public --project-name=brand
