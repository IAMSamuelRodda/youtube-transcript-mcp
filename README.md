# YouTube Transcript MCP Server

MCP server for extracting transcripts from YouTube videos using the youtube-transcript-api library.

## Features

- **No API keys required** - Uses youtube-transcript-api
- **3 tools** - Plain text, timed transcripts, video metadata
- **Fast** - Direct transcript extraction without authentication

## Tools

| Tool | Description |
|------|-------------|
| `get_transcript` | Get plain text transcript from a YouTube video |
| `get_timed_transcript` | Get transcript with timestamps |
| `get_video_info` | Get video metadata (title, duration, etc.) |

## Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Standalone (stdio)

```bash
python youtube_transcript_mcp.py
```

### With Claude Code

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/youtube_transcript_mcp.py"],
      "transportType": "stdio"
    }
  }
}
```

## Dependencies

- `mcp` - Model Context Protocol SDK
- `youtube-transcript-api` - YouTube transcript extraction

## License

MIT
