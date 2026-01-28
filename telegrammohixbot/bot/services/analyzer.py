"""
URL analyzer service.

Responsibility:
- Basic validation that a string looks like a URL
- Detection of supported platforms based on the URL

The logic here is intentionally simple and easy to extend
for future platforms (TikTok, Twitter, etc.).
"""

from __future__ import annotations

import enum
import re
from typing import Optional


class Platform(str, enum.Enum):
    """Supported platforms."""

    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"


_URL_REGEX = re.compile(
    r"^(https?://)"
    r"([\w\-\.]+)"
    r"(:\d+)?"
    r"(/[\w\-\.~:/?#[\]@!$&'()*+,;=%]*)?$",
    re.IGNORECASE,
)


def is_valid_url(text: str) -> bool:
    """Return True if the input looks like a valid HTTP/HTTPS URL."""
    return bool(_URL_REGEX.match(text.strip()))


def detect_platform(url: str) -> Optional[Platform]:
    """
    Detect which platform the URL belongs to.

    Currently supports:
    - YouTube (www.youtube.com, m.youtube.com, youtu.be, youtube.com/shorts)
    - Instagram (instagram.com, www.instagram.com)
    """
    normalized = url.lower()

    if any(domain in normalized for domain in ("youtube.com", "youtu.be")):
        return Platform.YOUTUBE

    if "instagram.com" in normalized:
        return Platform.INSTAGRAM

    return None

