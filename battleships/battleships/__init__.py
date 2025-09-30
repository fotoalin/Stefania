"""
Battleships Game Engine - Standalone Core
Pure game logic engine with no I/O dependencies
"""

from .board import BattleshipPlacer, Board
from .engine import BattleshipEngine
from .game_state import GameState
from .models import CellState, GameResult, Position

__version__ = "2.0.0"
__all__ = [
    "BattleshipEngine",
    "CellState",
    "GameResult", 
    "Position",
    "Board",
    "BattleshipPlacer",
    "GameState"
]
