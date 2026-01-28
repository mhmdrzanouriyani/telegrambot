"""
Video description extractor service using yt-dlp.

This module extracts video descriptions/metadata without downloading the video file.
Uses yt-dlp with --skip-download and --print description flags.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from yt_dlp import YoutubeDL

from bot.utils.logger import get_logger


logger = get_logger()


def _extract_description_sync(url: str) -> Optional[str]:
    """
    Blocking part executed in a thread via asyncio.to_thread.

    Uses yt-dlp to extract video description without downloading the video.

    Args:
        url: The video URL to extract description from

    Returns:
        The video description text, or None if extraction fails
    """
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    try:
        logger.info("Extracting description for url=%s", url)
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            description = info.get("description", "")

            # Ensure description is a string
            if description is None:
                description = ""

            logger.info("Successfully extracted description (length=%d)", len(description))
            return description.strip() if description else None

    except Exception as exc:
        logger.exception("Error extracting description for url=%s: %s", url, exc)
        return None


async def get_video_description(url: str) -> Optional[str]:
    """
    Extract the full video description from a video URL asynchronously.

    This function:
    - Uses yt-dlp to fetch metadata only (no video download)
    - Does NOT download the media file
    - Executes in a thread pool to avoid blocking the event loop

    Args:
        url: The video URL (YouTube, Instagram, etc.)

    Returns:
        The full video description text, or None if extraction fails
    """
    return await asyncio.to_thread(_extract_description_sync, url)
