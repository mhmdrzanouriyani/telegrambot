"""
Utility functions for splitting long messages to fit Telegram limits.

Telegram has a maximum message length of 4096 characters.
This module provides functions to split text into multiple messages if needed.
"""

from __future__ import annotations

from typing import List

# Telegram maximum message length
TELEGRAM_MAX_MESSAGE_LENGTH = 4096


def split_message(text: str, max_length: int = TELEGRAM_MAX_MESSAGE_LENGTH, prefix: str = "") -> List[str]:
    """
    Split a long text message into multiple messages that fit within Telegram limits.

    Args:
        text: The text to split
        max_length: Maximum length per message (default: 4096 for Telegram)
        prefix: Optional prefix to add to each chunk (accounted for in length calculation)

    Returns:
        List of text chunks, each within the length limit
    """
    # Account for prefix length
    available_length = max_length - len(prefix)
    
    if len(text) <= available_length:
        return [text]

    chunks: List[str] = []
    current_chunk = ""

    # Split by lines first to preserve readability
    lines = text.split("\n")

    for line in lines:
        # If adding this line would exceed the limit, save current chunk and start new one
        if len(current_chunk) + len(line) + 1 > available_length:
            if current_chunk:
                chunks.append(current_chunk.rstrip())
                current_chunk = ""

            # If a single line is longer than available_length, split it by words
            if len(line) > available_length:
                words = line.split(" ")
                for word in words:
                    if len(current_chunk) + len(word) + 1 > available_length:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip())
                            current_chunk = ""
                    current_chunk += word + " "
            else:
                current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.rstrip())

    return chunks if chunks else [text[:available_length]]
