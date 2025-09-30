"""
Board management and related game logic
"""

from random import randint
from typing import List, Set

from .models import CellState, Position


class Board:
    """Manages the game board state - Single Responsibility Principle"""
    
    def __init__(self, size: int = 10):
        self._size = size
        self._cells = [CellState.EMPTY for _ in range(size)]
        self._battleship_positions: Set[Position] = set()
    
    def place_battleship(self, position: Position) -> bool:
        """Place a battleship at the given position"""
        if self._cells[position.index] != CellState.EMPTY:
            return False
        
        self._cells[position.index] = CellState.BATTLESHIP
        self._battleship_positions.add(position)
        return True
    
    def make_guess(self, position: Position) -> CellState:
        """Make a guess at the given position and return the result"""
        current_state = self._cells[position.index]
        
        if current_state == CellState.BATTLESHIP:
            self._cells[position.index] = CellState.HIT
            return CellState.HIT
        elif current_state == CellState.EMPTY:
            self._cells[position.index] = CellState.MISS
            return CellState.MISS
        else:
            return current_state  # Already guessed
    
    def get_cells(self) -> List[CellState]:
        """Get a copy of the board cells"""
        return self._cells.copy()
    
    def count_remaining_battleships(self) -> int:
        """Count how many battleships are still hidden"""
        return sum(1 for cell in self._cells if cell == CellState.BATTLESHIP)
    
    @property
    def size(self) -> int:
        """Get the board size"""
        return self._size


class BattleshipPlacer:
    """Handles battleship placement logic - Single Responsibility Principle"""
    
    def __init__(self, board: Board):
        self._board = board
    
    def place_random_battleships(self, count: int) -> None:
        """Place a specified number of battleships randomly"""
        placed = 0
        used_positions = set()
        
        while placed < count:
            index = randint(0, self._board.size - 1)
            position = Position(index)
            
            if position not in used_positions:
                if self._board.place_battleship(position):
                    used_positions.add(position)
                    placed += 1
