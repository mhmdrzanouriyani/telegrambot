"""
User session storage for video URLs.

Stores URLs per chat_id (user session) so the URL persists across
multiple button interactions without requiring the user to resend the link.
"""

from __future__ import annotations

from typing import Optional

# Session storage: chat_id -> stored_url
# This allows the URL to persist across multiple button clicks
# until the user cancels or sends a new link
user_sessions: dict[int, str] = {}


def store_url(chat_id: int, url: str) -> None:
    """Store a URL for a user session."""
    user_sessions[chat_id] = url


def get_url(chat_id: int) -> Optional[str]:
    """Get the stored URL for a user session."""
    return user_sessions.get(chat_id)


def clear_url(chat_id: int) -> None:
    """Clear the stored URL for a user session."""
    user_sessions.pop(chat_id, None)


def has_url(chat_id: int) -> bool:
    """Check if a user session has a stored URL."""
    return chat_id in user_sessions
