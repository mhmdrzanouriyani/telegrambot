"""
Handlers for the /start command and its inline buttons.

This module is responsible only for user interaction and messages,
not for any downloading logic.
"""

from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards.start_keyboard import StartCallbacks, build_start_keyboard


router = Router()


START_MESSAGE = (
    "👋 Welcome to Mohixtube Bot!\n\n"
    "This bot can download videos from:\n\n"
    "• Instagram Reels\n"
    "• YouTube Videos\n"
    "• YouTube Shorts\n\n"
    "Just send the video link and I will download it for you.\n\n"
    "⬇️ Send a link to get started."
)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """
    Handle the /start command.

    Sends a friendly welcome message and shows an inline keyboard
    with common actions.
    """
    await message.answer(
        START_MESSAGE,
        reply_markup=build_start_keyboard(),
    )


@router.callback_query(F.data == StartCallbacks.DOWNLOAD)
async def handle_start_download_button(callback: CallbackQuery) -> None:
    """
    📥 Download video button.

    Simply tells the user to send a video link.
    """
    await callback.message.edit_text(
        "📥 Please send the video link you want to download.\n\n"
        "Supported:\n"
        "• Instagram Reels\n"
        "• YouTube Videos\n"
        "• YouTube Shorts",
        reply_markup=build_start_keyboard(),
    )
    await callback.answer()  # Close loading state


@router.callback_query(F.data == StartCallbacks.HOW_TO_USE)
async def handle_start_how_to_use_button(callback: CallbackQuery) -> None:
    """
    ℹ️ How to use button.

    Shows a short step-by-step guide.
    """
    text = (
        "ℹ️ How to use Mohixtube Bot:\n\n"
        "1️⃣ Copy the video link from Instagram or YouTube.\n"
        "2️⃣ Paste the link here in this chat.\n"
        "3️⃣ Wait while I download and send the video to you.\n\n"
        "⬇️ You can send a link now."
    )
    await callback.message.edit_text(text, reply_markup=build_start_keyboard())
    await callback.answer()


@router.callback_query(F.data == StartCallbacks.SUPPORTED)
async def handle_start_supported_button(callback: CallbackQuery) -> None:
    """
    ❓ Supported platforms button.

    Shows the currently supported platforms.
    """
    text = (
        "❓ Supported platforms:\n\n"
        "• Instagram Reels (public)\n"
        "• YouTube Videos\n"
        "• YouTube Shorts\n\n"
        "Send any of these links and Mohixtube Bot will download it for you."
    )
    await callback.message.edit_text(text, reply_markup=build_start_keyboard())
    await callback.answer()

