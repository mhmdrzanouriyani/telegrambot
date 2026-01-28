from aiogram import Router, F
from aiogram.types import Message

from bot.services.analyzer import detect_platform, Platform, is_valid_url
from bot.keyboards.video_menu import build_video_menu_keyboard
from bot.services.url_storage import store_url


router = Router()


@router.message(F.text)
async def handle_text_message(message: Message) -> None:
    """
    Entry point for all text messages.

    - Validates that the message contains a URL
    - Detects the target platform (YouTube / Instagram)
    - Stores URL in user session
    - Shows interactive menu with options: Download video, Get description, Back, Cancel
    """
    text = (message.text or "").strip()

    if not is_valid_url(text):
        await message.reply(
            "Welcome to Mohixtube Bot 🎬\n\n"
            "Please send a valid Instagram or YouTube URL.\n"
            "Example:\n"
            "- https://www.youtube.com/watch?v=...\n"
            "- https://www.instagram.com/reel/..."
        )
        return

    platform = detect_platform(text)
    if platform is None:
        await message.reply(
            "Mohixtube Bot currently supports only Instagram and YouTube URLs.\n"
            "Please send a link from these platforms."
        )
        return

    # Store URL in user session (per chat_id) so it persists across button clicks
    store_url(message.chat.id, text)

    # Show interactive menu with buttons
    keyboard = build_video_menu_keyboard()
    await message.reply(
        "What would you like to do with this link?",
        reply_markup=keyboard,
    )

