#!/bin/bash

# Share Visual Explainer HTML via Cloudflare Pages
# Usage: ./Share.sh <html-file> [project-name]
# Returns: Live URL instantly
#
# Requires: npx wrangler (included with wrangler package)
# One-time setup: npx wrangler login

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
DIM='\033[0;90m'
NC='\033[0m'

HTML_FILE="${1}"
PROJECT_NAME="${2:-ve-shared}"

if [ -z "$HTML_FILE" ]; then
    echo -e "${RED}Error: Please provide an HTML file to share${NC}" >&2
    echo "Usage: $0 <html-file> [project-name]" >&2
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo -e "${RED}Error: File not found: $HTML_FILE${NC}" >&2
    exit 1
fi

# Check wrangler auth
if ! npx wrangler whoami >/dev/null 2>&1; then
    echo -e "${RED}Error: Not authenticated with Cloudflare${NC}" >&2
    echo "" >&2
    echo -e "${CYAN}One-time setup:${NC}" >&2
    echo "  1. Create a free account at https://cloudflare.com" >&2
    echo "  2. Run: npx wrangler login" >&2
    echo "  3. Try sharing again" >&2
    exit 1
fi

# Create temp directory with index.html
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

cp "$HTML_FILE" "$TEMP_DIR/index.html"

FILENAME=$(basename "$HTML_FILE" .html)
echo -e "${CYAN}Sharing ${FILENAME}...${NC}" >&2

# Deploy to Cloudflare Pages via wrangler
# --commit-dirty suppresses the "uncommitted changes" warning
# --branch main ensures it's a production deploy (not preview)
set +e
RESULT=$(npx wrangler pages deploy "$TEMP_DIR" \
    --project-name "$PROJECT_NAME" \
    --commit-dirty \
    --branch main \
    2>&1)
DEPLOY_EXIT=$?
set -e

if [ $DEPLOY_EXIT -ne 0 ]; then
    # If project doesn't exist, create it and retry
    if echo "$RESULT" | grep -qi "project not found\|could not find"; then
        echo -e "${DIM}Creating project '${PROJECT_NAME}'...${NC}" >&2
        npx wrangler pages project create "$PROJECT_NAME" --production-branch main >/dev/null 2>&1 || true
        set +e
        RESULT=$(npx wrangler pages deploy "$TEMP_DIR" \
            --project-name "$PROJECT_NAME" \
            --commit-dirty \
            --branch main \
            2>&1)
        DEPLOY_EXIT=$?
        set -e
    fi

    if [ $DEPLOY_EXIT -ne 0 ]; then
        echo -e "${RED}Error: Deployment failed${NC}" >&2
        echo "$RESULT" >&2
        exit 1
    fi
fi

# Extract the deployment URL from wrangler output
# wrangler pages deploy outputs the URL on a line like:
# ✨ Deployment complete! Take a peek over at https://abc123.ve-shared.pages.dev
DEPLOY_URL=$(echo "$RESULT" | grep -oE 'https://[^ ]+\.pages\.dev' | head -1)

if [ -z "$DEPLOY_URL" ]; then
    # Fallback: try to find any URL in output
    DEPLOY_URL=$(echo "$RESULT" | grep -oE 'https://[^ ]+' | head -1)
fi

if [ -z "$DEPLOY_URL" ]; then
    echo -e "${RED}Error: Could not extract deployment URL${NC}" >&2
    echo -e "${DIM}Wrangler output:${NC}" >&2
    echo "$RESULT" >&2
    exit 1
fi

echo "" >&2
echo -e "${GREEN}✓ Shared successfully!${NC}" >&2
echo "" >&2
echo -e "${GREEN}Live URL:  ${DEPLOY_URL}${NC}" >&2
echo -e "${DIM}Project:   ${PROJECT_NAME}${NC}" >&2
echo -e "${DIM}Dashboard: https://dash.cloudflare.com/?to=/:account/pages/view/${PROJECT_NAME}${NC}" >&2
echo "" >&2

# JSON output for programmatic use
echo "{\"url\":\"${DEPLOY_URL}\",\"project\":\"${PROJECT_NAME}\"}"
