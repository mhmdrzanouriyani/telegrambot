"""
Callback handlers for inline keyboard buttons.

Handles user interactions with the video action menu buttons.
"""

from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.video_menu import VideoMenuCallbacks, build_video_menu_keyboard
from bot.services.analyzer import detect_platform, Platform, is_valid_url
from bot.services.queue import download_queue, DownloadTask
from bot.services.description_extractor import get_video_description
from bot.utils.message_splitter import split_message
from bot.utils.logger import get_logger
from bot.services.url_storage import get_url, clear_url, has_url


logger = get_logger()
router = Router()


@router.callback_query(F.data == VideoMenuCallbacks.BACK)
async def handle_back(callback: CallbackQuery) -> None:
    """Handle back button click - return to main menu with stored URL."""
    chat_id = callback.message.chat.id
    
    # Check if user has a stored URL
    if not has_url(chat_id):
        await callback.answer("No stored link found. Please send a video link first.", show_alert=True)
        return
    
    # Return to main menu
    keyboard = build_video_menu_keyboard()
    await callback.message.edit_text(
        "What would you like to do with this link?",
        reply_markup=keyboard,
    )
    await callback.answer("Returned to menu")


@router.callback_query(F.data == VideoMenuCallbacks.CANCEL)
async def handle_cancel(callback: CallbackQuery) -> None:
    """Handle cancel button click - clear stored URL and remove keyboard."""
    chat_id = callback.message.chat.id
    
    # Clear stored URL from session
    clear_url(chat_id)
    
    await callback.message.edit_text(
        "❌ Cancelled.\n\n"
        "Please send a new video link to continue."
    )
    await callback.answer("Cancelled")


@router.callback_query(F.data == VideoMenuCallbacks.DOWNLOAD_VIDEO)
async def handle_download_video(callback: CallbackQuery) -> None:
    """Handle download video button click."""
    chat_id = callback.message.chat.id
    
    # Get URL from user session storage
    url = get_url(chat_id)
    
    if not url or not is_valid_url(url):
        await callback.answer("No stored link found. Please send a video link first.", show_alert=True)
        return

    platform = detect_platform(url)
    if platform is None:
        await callback.answer(
            "Unsupported platform. Only YouTube and Instagram are supported.",
            show_alert=True,
        )
        return

    # Update message to show processing
    await callback.message.edit_text(
        "Mohixtube Bot: Added to download queue ✅\n"
        "You will see status updates here."
    )

    # Create download task
    task = DownloadTask(
        url=url,
        platform=platform,
        chat_id=chat_id,
        status_message_id=callback.message.message_id,
        original_message_id=callback.message.message_id,
    )

    await download_queue.enqueue(task)
    await callback.answer("Video added to download queue")


@router.callback_query(F.data == VideoMenuCallbacks.GET_DESCRIPTION)
async def handle_get_description(callback: CallbackQuery) -> None:
    """Handle get description button click."""
    chat_id = callback.message.chat.id
    
    # Get URL from user session storage
    url = get_url(chat_id)
    
    if not url or not is_valid_url(url):
        await callback.answer("No stored link found. Please send a video link first.", show_alert=True)
        return

    # Show loading message
    await callback.message.edit_text("⏳ Extracting video description...")

    try:
        # Extract description asynchronously
        description = await get_video_description(url)

        if description is None or not description.strip():
            # Show menu again with error message
            keyboard = build_video_menu_keyboard()
            await callback.message.edit_text(
                "❌ Could not extract video description.\n"
                "The video might not have a description, or the URL is not supported.\n\n"
                "What would you like to do with this link?",
                reply_markup=keyboard,
            )
            await callback.answer("Description extraction failed")
            return

        # Split message if too long (accounting for prefix text)
        prefix = "📝 <b>Video Description:</b>\n\n"
        message_chunks = split_message(description, prefix=prefix)

        # Send first chunk (edit the existing message)
        # Use HTML parse mode for better handling of special characters
        try:
            await callback.message.edit_text(
                f"{prefix}{message_chunks[0]}",
                parse_mode="HTML",
            )
        except Exception:
            # Fallback to plain text if HTML parsing fails
            await callback.message.edit_text(
                f"📝 Video Description:\n\n{message_chunks[0]}",
            )

        # Send remaining chunks as new messages
        if len(message_chunks) > 1:
            continue_prefix = "📝 <b>Video Description (continued):</b>\n\n"
            for chunk in message_chunks[1:]:
                try:
                    await callback.message.answer(
                        f"{continue_prefix}{chunk}",
                        parse_mode="HTML",
                    )
                except Exception:
                    # Fallback to plain text if HTML parsing fails
                    await callback.message.answer(
                        f"📝 Video Description (continued):\n\n{chunk}",
                    )

        # Show menu again after showing description
        keyboard = build_video_menu_keyboard()
        await callback.message.answer(
            "What would you like to do with this link?",
            reply_markup=keyboard,
        )

        await callback.answer("Description extracted successfully")

    except Exception as exc:
        logger.exception("Error extracting description for callback: %s", callback.data)
        # Show menu again with error
        keyboard = build_video_menu_keyboard()
        await callback.message.edit_text(
            f"❌ An error occurred while extracting the description:\n{exc}\n\n"
            "What would you like to do with this link?",
            reply_markup=keyboard,
        )
        await callback.answer("Error occurred", show_alert=True)
