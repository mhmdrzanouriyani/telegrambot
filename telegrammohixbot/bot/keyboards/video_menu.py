"""
Inline keyboard for video action menu.

Shown when user sends a video link, asking what they want to extract.
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class VideoMenuCallbacks:
    """
    Centralized callback data values for the video action menu.

    Keeping these as constants avoids typos between keyboard and handlers.
    """

    DOWNLOAD_VIDEO = "video_download"
    GET_DESCRIPTION = "video_description"
    BACK = "video_back"
    CANCEL = "video_cancel"


def build_video_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Build the inline keyboard shown when a video link is detected.

    Buttons:
        - 🎥 Download video
        - 📝 Get full video description
        - 🔙 Back
        - ❌ Cancel

    Note: URLs are stored per chat_id in user session storage,
    so callback handlers can retrieve the URL without needing it in callback data.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="🎥 Download video",
                callback_data=VideoMenuCallbacks.DOWNLOAD_VIDEO,
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Get full video description",
                callback_data=VideoMenuCallbacks.GET_DESCRIPTION,
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=VideoMenuCallbacks.BACK,
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Cancel",
                callback_data=VideoMenuCallbacks.CANCEL,
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
