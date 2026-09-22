"""Central logging configuration for the application."""

import logging
from rich.logging import RichHandler
from config.settings import get_settings

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=getattr(logging, get_settings().log_level.upper(), logging.INFO),
            format="%(message)s",
            handlers=[RichHandler(rich_tracebacks=True)],
        )
    return logger
