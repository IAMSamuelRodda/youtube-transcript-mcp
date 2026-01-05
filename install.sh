#!/usr/bin/env bash
# YouTube Transcript MCP Server - Claude Code Installation Script
# No API keys required - just installs and registers

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }

# Check for Python venv
if [[ ! -d "${SCRIPT_DIR}/.venv" ]]; then
    info "Creating Python virtual environment..."
    python3 -m venv "${SCRIPT_DIR}/.venv"
    info "Installing dependencies..."
    "${SCRIPT_DIR}/.venv/bin/pip" install -q -r "${SCRIPT_DIR}/requirements.txt"
else
    info "Virtual environment already exists."
fi

# Register with Claude Code
MCP_NAME="youtube-transcript"
PYTHON_PATH="${SCRIPT_DIR}/.venv/bin/python"

info "Registering MCP server with Claude Code..."
claude mcp add "$MCP_NAME" -s user -- "$PYTHON_PATH" "${SCRIPT_DIR}/youtube_transcript_mcp.py"

info "YouTube Transcript MCP server registered successfully!"
info "Restart Claude Code to use the new server."
info ""
info "No API keys required - ready to use immediately!"
