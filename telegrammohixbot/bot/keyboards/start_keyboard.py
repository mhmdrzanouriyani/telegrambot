"""
Inline keyboard for the /start welcome message.

This module only knows about button layout and callback data,
not about how those callbacks are handled.
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class StartCallbacks:
    """
    Centralized callback data values for the start menu.

    Keeping these as constants avoids typos between keyboard and handlers.
    """

    DOWNLOAD = "start_download"
    HOW_TO_USE = "start_how_to_use"
    SUPPORTED = "start_supported"


def build_start_keyboard() -> InlineKeyboardMarkup:
    """
    Build the inline keyboard shown under the /start message.

    Buttons:
    - 📥 Download video
    - ℹ️ How to use
    - ❓ Supported platforms
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="📥 Download video",
                callback_data=StartCallbacks.DOWNLOAD,
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ How to use",
                callback_data=StartCallbacks.HOW_TO_USE,
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Supported platforms",
                callback_data=StartCallbacks.SUPPORTED,
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

