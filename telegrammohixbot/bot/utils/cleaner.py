"""
Helpers for managing the downloads directory and cleaning up files.
"""

from __future__ import annotations

import os
from pathlib import Path

from bot.utils.logger import get_logger


logger = get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOWNLOAD_DIR = BASE_DIR / "downloads"


def ensure_download_dir() -> Path:
    """
    Ensure that the downloads directory exists and return its path.

    The directory is created under the project root as `downloads/`.
    """
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return DOWNLOAD_DIR


def safe_unlink(path: Path) -> None:
    """
    Delete a file from disk if it exists, ignoring common errors.

    This is used after a file has been sent to Telegram to avoid
    filling up disk space with temporary files.
    """
    try:
        if path.exists() and path.is_file():
            os.remove(path)
            logger.info("Deleted temporary file: %s", path)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to delete file: %s", path)

