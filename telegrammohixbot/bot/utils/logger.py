"""
Centralized logging configuration.

Using a shared logger makes it easy to debug and to plug in
file-based logging later if required.
"""

from __future__ import annotations

import logging
from typing import Optional


_LOGGER_NAME = "telegram_downloader_bot"
_configured = False


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Configure the root logger for the application.

    This should be called once from the main entrypoint.
    """
    global _configured

    logger = logging.getLogger(_LOGGER_NAME)

    if not _configured:
        logger.setLevel(level)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        _configured = True

    return logger


def get_logger() -> logging.Logger:
    """
    Get the shared application logger.

    If it hasn't been configured yet, this will configure it with defaults.
    """
    if not _configured:
        return setup_logger()
    return logging.getLogger(_LOGGER_NAME)

