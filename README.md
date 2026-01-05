# YouTube Transcript MCP Server

MCP server for extracting transcripts from YouTube videos. **No API keys required.**

## Features

- **No API keys** - Uses youtube-transcript-api, no authentication needed
- **Plain text transcripts** - Get full transcript as readable text
- **Timed transcripts** - Get transcript with timestamps for each segment
- **Video metadata** - Extract title, duration, and other video info

## Quick Install (Claude Code)

```bash
# Clone the repository
git clone https://github.com/IAMSamuelRodda/youtube-transcript-mcp.git
cd youtube-transcript-mcp

# Run the install script (no config needed!)
./install.sh
```

The install script will:
1. Create a Python virtual environment
2. Install dependencies
3. Register the MCP server with Claude Code

**That's it!** No API keys or configuration required.

## Manual Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Claude Code

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "/path/to/youtube-transcript-mcp/.venv/bin/python",
      "args": ["/path/to/youtube-transcript-mcp/youtube_transcript_mcp.py"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_transcript` | Get plain text transcript from a YouTube video |
| `get_timed_transcript` | Get transcript with timestamps |
| `get_video_info` | Get video metadata (title, duration, etc.) |

## Usage Examples

Once configured, you can ask Claude:

- "Get the transcript from this YouTube video: https://youtube.com/watch?v=..."
- "Summarize this YouTube video for me"
- "What are the main points discussed in this video?"
- "Get the timestamps for when they talk about X in this video"

## How It Works

Uses the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) library to extract auto-generated and manual captions directly from YouTube without requiring any API credentials.

## Limitations

- Only works with videos that have captions (auto-generated or manual)
- Some videos may have captions disabled by the uploader
- Age-restricted or private videos may not be accessible

## License

MIT
