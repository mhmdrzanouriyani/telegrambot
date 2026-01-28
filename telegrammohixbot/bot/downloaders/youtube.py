"""
YouTube and YouTube Shorts downloader using yt-dlp.

This module exposes a single async function that:
- Uses yt-dlp Python API (not shell)
- Downloads the best available video+audio
- Ensures MP4 output
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict
import time

from yt_dlp import YoutubeDL

from bot.utils.logger import get_logger


logger = get_logger()


def _build_ydl_opts(download_dir: Path) -> Dict[str, Any]:
    """
    Build yt-dlp options for YouTube.

    - Best MP4 video + M4A audio merged
    - MP4 output (Telegram-friendly)
    - Safe, filesystem-friendly filenames
    """
    return {
        # Prefer MP4+M4A for Telegram streaming compatibility
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "merge_output_format": "mp4",
        "outtmpl": str(download_dir / "%(title).80s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }


def _download_sync(url: str, download_dir: Path) -> Path:
    """
    Blocking part executed in a thread via asyncio.to_thread.

    Strategy:
    - Snapshot files in download_dir before download
    - Run yt-dlp
    - Snapshot files after download
    - The new file(s) are assumed to be the download output
    """
    before_files = set(download_dir.glob("*"))

    ydl_opts = _build_ydl_opts(download_dir)
    logger.info("Starting YouTube download for url=%s", url)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Give ffmpeg a brief moment to finalize the file on disk
    time.sleep(1)

    after_files = set(download_dir.glob("*"))
    new_files = list(after_files - before_files)

    if not new_files:
        raise RuntimeError("yt-dlp finished but no output file found")

    # Prefer mp4 output if multiple files were created
    mp4_files = [f for f in new_files if f.suffix.lower() == ".mp4"]
    downloaded_file = mp4_files[0] if mp4_files else new_files[0]

    logger.info("YouTube download finished: %s", downloaded_file)
    return downloaded_file


async def download_youtube_video(url: str, download_dir: Path) -> Path:
    """
    Download a YouTube video or Shorts URL to the given directory.

    Executed via asyncio.to_thread so the event loop is not blocked.
    """
    download_dir.mkdir(parents=True, exist_ok=True)
    return await asyncio.to_thread(_download_sync, url, download_dir)

