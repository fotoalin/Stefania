"""
Platform adapters for the Battleships game engine
"""

from .console_adapter import ConsoleGameAdapter
from .web_adapter import WebGameAdapter

__all__ = [
    "ConsoleGameAdapter",
    "WebGameAdapter"
]