# YouTube Transcript MCP Server

MCP server for extracting transcripts from YouTube videos. **No API keys required.**

## Features

- **No API keys** - Uses youtube-transcript-api, no authentication needed
- **Plain text transcripts** - Get full transcript as readable text
- **Timed transcripts** - Get transcript with timestamps for each segment
- **Video metadata** - Extract title, duration, and other video info

## Installation

### Option 1: uvx (Recommended)

Zero-install method using [uv](https://docs.astral.sh/uv/). Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/IAMSamuelRodda/youtube-transcript-mcp", "youtube-transcript-mcp"]
    }
  }
}
```

**That's it!** No API keys or configuration required.

### Option 2: Local Clone

```bash
mkdir -p ~/.claude/mcp-servers
git clone https://github.com/IAMSamuelRodda/youtube-transcript-mcp.git ~/.claude/mcp-servers/youtube-transcript-mcp
cd ~/.claude/mcp-servers/youtube-transcript-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "~/.claude/mcp-servers/youtube-transcript-mcp/.venv/bin/python",
      "args": ["~/.claude/mcp-servers/youtube-transcript-mcp/youtube_transcript_mcp.py"]
    }
  }
}
```

## Updating

### uvx users

```bash
uv cache clean youtube-transcript-mcp
```

### Local clone users

```bash
cd ~/.claude/mcp-servers/youtube-transcript-mcp
git pull
source .venv/bin/activate
pip install -r requirements.txt
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
