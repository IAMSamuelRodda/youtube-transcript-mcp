#!/usr/bin/env python3
"""
MCP Server for YouTube Transcripts.

Provides tools to extract transcripts from YouTube videos using
the youtube-transcript-api library.

Requirements:
    - No credentials required (public API)
    - No OpenBao integration needed (no secrets)

Tools:
    - get_transcript: Get plain text transcript
    - get_timed_transcript: Get transcript with timestamps
    - get_video_info: Get video metadata (title, etc.)
"""

import re
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

# Initialize the MCP server
mcp = FastMCP("youtube_transcript")

# Constants
MAX_TRANSCRIPT_LENGTH = 50000  # Character limit for responses


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return as-is if already an ID."""
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',  # Just the ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


class TranscriptInput(BaseModel):
    """Input for transcript retrieval."""
    video_url: str = Field(description="YouTube video URL or video ID")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'en', 'es'). Auto-detects if not specified.")


class TimedTranscriptInput(BaseModel):
    """Input for timed transcript retrieval."""
    video_url: str = Field(description="YouTube video URL or video ID")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'en', 'es'). Auto-detects if not specified.")


@mcp.tool()
def get_transcript(params: TranscriptInput) -> str:
    """
    Get the plain text transcript of a YouTube video.

    Returns the full transcript as continuous text without timestamps.
    Useful for summarization, analysis, or when timing isn't needed.
    """
    try:
        video_id = extract_video_id(params.video_url)

        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to get transcript in requested language or auto-detect
        if params.language:
            try:
                transcript = transcript_list.find_transcript([params.language])
            except NoTranscriptFound:
                # Fall back to any available transcript
                transcript = transcript_list.find_transcript(['en'])
        else:
            # Try English first, then any available
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                # Get first available transcript
                transcript = next(iter(transcript_list))

        # Fetch the actual transcript data
        transcript_data = transcript.fetch()

        # Combine all text segments
        full_text = ' '.join(segment['text'] for segment in transcript_data)

        # Clean up whitespace
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        # Truncate if too long
        if len(full_text) > MAX_TRANSCRIPT_LENGTH:
            full_text = full_text[:MAX_TRANSCRIPT_LENGTH] + "\n\n[Transcript truncated due to length]"

        return f"Video ID: {video_id}\nLanguage: {transcript.language_code}\n\n{full_text}"

    except VideoUnavailable:
        return f"Error: Video '{params.video_url}' is unavailable or does not exist."
    except TranscriptsDisabled:
        return f"Error: Transcripts are disabled for video '{params.video_url}'."
    except NoTranscriptFound:
        return f"Error: No transcript found for video '{params.video_url}'."
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


@mcp.tool()
def get_timed_transcript(params: TimedTranscriptInput) -> str:
    """
    Get the transcript of a YouTube video with timestamps.

    Returns each segment with its start time in [MM:SS] format.
    Useful when you need to reference specific parts of the video.
    """
    try:
        video_id = extract_video_id(params.video_url)

        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to get transcript in requested language or auto-detect
        if params.language:
            try:
                transcript = transcript_list.find_transcript([params.language])
            except NoTranscriptFound:
                transcript = transcript_list.find_transcript(['en'])
        else:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                transcript = next(iter(transcript_list))

        # Fetch the actual transcript data
        transcript_data = transcript.fetch()

        # Format with timestamps
        lines = []
        for segment in transcript_data:
            start_seconds = int(segment['start'])
            minutes = start_seconds // 60
            seconds = start_seconds % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            text = segment['text'].strip()
            lines.append(f"{timestamp} {text}")

        result = '\n'.join(lines)

        # Truncate if too long
        if len(result) > MAX_TRANSCRIPT_LENGTH:
            result = result[:MAX_TRANSCRIPT_LENGTH] + "\n\n[Transcript truncated due to length]"

        return f"Video ID: {video_id}\nLanguage: {transcript.language_code}\n\n{result}"

    except VideoUnavailable:
        return f"Error: Video '{params.video_url}' is unavailable or does not exist."
    except TranscriptsDisabled:
        return f"Error: Transcripts are disabled for video '{params.video_url}'."
    except NoTranscriptFound:
        return f"Error: No transcript found for video '{params.video_url}'."
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


class VideoInfoInput(BaseModel):
    """Input for video info retrieval."""
    video_url: str = Field(description="YouTube video URL or video ID")


@mcp.tool()
def get_video_info(params: VideoInfoInput) -> str:
    """
    Get available transcript languages and metadata for a YouTube video.

    Returns list of available transcript languages (manual and auto-generated).
    """
    try:
        video_id = extract_video_id(params.video_url)

        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Collect language info
        manual = []
        auto_generated = []

        for transcript in transcript_list:
            lang_info = f"{transcript.language} ({transcript.language_code})"
            if transcript.is_generated:
                auto_generated.append(lang_info)
            else:
                manual.append(lang_info)

        result = f"Video ID: {video_id}\n\n"

        if manual:
            result += "Manual transcripts:\n"
            result += '\n'.join(f"  - {lang}" for lang in manual)
            result += "\n\n"

        if auto_generated:
            result += "Auto-generated transcripts:\n"
            result += '\n'.join(f"  - {lang}" for lang in auto_generated)

        if not manual and not auto_generated:
            result += "No transcripts available for this video."

        return result

    except VideoUnavailable:
        return f"Error: Video '{params.video_url}' is unavailable or does not exist."
    except TranscriptsDisabled:
        return f"Error: Transcripts are disabled for video '{params.video_url}'."
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error retrieving video info: {str(e)}"


if __name__ == "__main__":
    mcp.run()
