"""
Uploader service for sending downloaded videos back to Telegram.
"""

from __future__ import annotations

from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile

from bot.utils.cleaner import safe_unlink
from bot.utils.logger import get_logger


logger = get_logger()


async def upload_video_flow(
    bot: Bot,
    chat_id: int,
    video_path: Path,
    status_message_id: int,
    reply_to_message_id: int | None = None,
) -> None:
    """
    Complete upload flow:
    - Send the video
    - Update the status message
    - Remove the temporary file from disk
    """
    try:
        video = FSInputFile(str(video_path))

        await bot.send_video(
            chat_id=chat_id,
            video=video,
            caption="🎬 Download completed",
            supports_streaming=True,
            reply_to_message_id=reply_to_message_id,
        )

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_message_id,
            text="✅ Download complete",
        )
    finally:
        # Ensure we always try to delete the file, even if sending fails.
        safe_unlink(video_path)

