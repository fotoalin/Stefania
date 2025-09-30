"""
Model classes and enums for the Battleships game
"""

from enum import Enum


class CellState(Enum):
    """Enum for cell states - Single Responsibility Principle"""
    EMPTY = ' '
    BATTLESHIP = 'B'
    HIT = 'F'
    MISS = 'M'


class GameResult(Enum):
    """Enum for game results"""
    WIN = "win"
    LOSE = "lose"
    IN_PROGRESS = "in_progress"


class Position:
    """Value object for board positions"""
    
    def __init__(self, index: int):
        if not 0 <= index <= 9:
            raise ValueError("Position must be between 0 and 9")
        self._index = index
    
    @property
    def index(self) -> int:
        return self._index
    
    @property
    def display_number(self) -> int:
        return self._index + 1
    
    def __eq__(self, other):
        return isinstance(other, Position) and self._index == other._index
    
    def __hash__(self):
        return hash(self._index)
    
    def __repr__(self):
        return f"Position({self._index})"
    
    def __str__(self):
        return str(self.display_number)
