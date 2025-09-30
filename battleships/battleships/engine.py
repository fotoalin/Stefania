"""
Core game engine - completely platform-agnostic
"""

from typing import Any, Dict, List, Optional

from .board import BattleshipPlacer, Board
from .game_state import GameState
from .models import CellState, GameResult, Position


class BattleshipEngine:
    """
    Pure game engine with no I/O dependencies.
    This is the core game logic that can be used by any platform.
    """
    
    def __init__(self, max_attempts: int = 5, battleship_count: int = 3):
        self._board = Board()
        self._game_state = GameState(max_attempts, battleship_count)
        self._placer = BattleshipPlacer(self._board)
        self._game_initialized = False
    
    def initialize_game(self) -> Dict[str, Any]:
        """Initialize a new game and return the initial state"""
        self._board = Board()
        self._game_state = GameState(
            self._game_state.max_attempts, 
            self._game_state.total_battleships
        )
        self._placer = BattleshipPlacer(self._board)
        self._placer.place_random_battleships(self._game_state.total_battleships)
        self._game_initialized = True
        
        return self.get_game_state()
    
    def make_guess(self, position: int) -> Dict[str, Any]:
        """
        Make a guess at the given position (1-10).
        Returns the result and updated game state.
        """
        if not self._game_initialized:
            return {'error': 'Game not initialized'}
            
        if not (1 <= position <= 10):
            return {'error': 'Position must be between 1 and 10'}
            
        if self._game_state.get_game_result() != GameResult.IN_PROGRESS:
            return {'error': 'Game is not in progress'}
        
        try:
            pos = Position(position - 1)  # Convert to 0-based
            result = self._board.make_guess(pos)
            self._game_state.use_attempt()
            
            # Determine the message based on result
            if result == CellState.HIT:
                message = "Sunk!"
                self._game_state.sink_battleship()
            elif result == CellState.MISS:
                message = "Miss!"
            else:
                message = "You already guessed that position."
            
            return {
                'result': result.value,
                'message': message,
                'position': position,
                **self.get_game_state()
            }
            
        except ValueError as e:
            return {'error': str(e)}
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get the current complete game state"""
        return {
            'board_cells': [cell.value for cell in self._board.get_cells()],
            'attempts_remaining': self._game_state.attempts_remaining,
            'attempts_used': self._game_state.attempts_used,
            'battleships_sunk': self._game_state.battleships_sunk,
            'total_battleships': self._game_state.total_battleships,
            'game_result': self._game_state.get_game_result().value,
            'game_initialized': self._game_initialized,
            'remaining_battleships': self._board.count_remaining_battleships()
        }
    
    def get_board_display(self, show_battleships: bool = False) -> str:
        """
        Get a formatted board display.
        show_battleships: If True, reveals battleship positions (for debug mode)
        """
        header = " ".join([str(i) for i in range(1, 11)])
        separator = "-" * (len(self._board.get_cells()) * 2)
        
        cells = self._board.get_cells()
        display_cells = []
        
        for cell in cells:
            if cell == CellState.BATTLESHIP and not show_battleships:
                display_cells.append(CellState.EMPTY.value)
            else:
                display_cells.append(cell.value)
        
        content = " ".join(display_cells)
        return f"{header}\n{separator}\n{content}\n{separator}"
    
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self._game_state.get_game_result() != GameResult.IN_PROGRESS
    
    def get_game_result(self) -> GameResult:
        """Get the current game result"""
        return self._game_state.get_game_result()
    
    def reset(self) -> None:
        """Reset the game for a new round"""
        self._game_initialized = False
        self._board = Board()
        self._game_state = GameState(
            self._game_state.max_attempts,
            self._game_state.total_battleships
        )
        self._placer = BattleshipPlacer(self._board)
