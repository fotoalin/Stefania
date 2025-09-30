"""
Game state management
"""

from .models import GameResult


class GameState:
    """Manages game state - Single Responsibility Principle"""
    
    def __init__(self, max_attempts: int = 5, battleship_count: int = 3):
        self._max_attempts = max_attempts
        self._battleship_count = battleship_count
        self._attempts_used = 0
        self._battleships_sunk = 0
    
    def use_attempt(self) -> None:
        """Use one attempt"""
        self._attempts_used += 1
    
    def sink_battleship(self) -> None:
        """Record a battleship as sunk"""
        self._battleships_sunk += 1
    
    @property
    def attempts_remaining(self) -> int:
        return self._max_attempts - self._attempts_used
    
    @property
    def battleships_sunk(self) -> int:
        return self._battleships_sunk
    
    @property
    def total_battleships(self) -> int:
        return self._battleship_count
    
    @property
    def attempts_used(self) -> int:
        return self._attempts_used
    
    @property
    def max_attempts(self) -> int:
        return self._max_attempts
    
    def get_game_result(self) -> GameResult:
        """Determine the current game result"""
        if self._battleships_sunk >= self._battleship_count:
            return GameResult.WIN
        elif self._attempts_used >= self._max_attempts:
            return GameResult.LOSE
        else:
            return GameResult.IN_PROGRESS
    
    def reset(self) -> None:
        """Reset the game state for a new game"""
        self._attempts_used = 0
        self._battleships_sunk = 0
