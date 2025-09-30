"""
Console adapter for the Battleships game engine
"""

import argparse
import os
import sys

from battleships.engine import BattleshipEngine
from battleships.models import GameResult

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class ConsoleGameAdapter:
    """Adapter to run the game engine in console mode"""
    
    def __init__(self, debug_mode: bool = False):
        self._engine = BattleshipEngine()
        self._debug_mode = debug_mode
    
    def run(self) -> None:
        """Run the complete game loop"""
        self._print_welcome()
        
        while True:
            if self._ask_play_again():
                self._play_game()
            else:
                break
        
        print("Thanks for playing Battleships! 🚢")
    
    def _print_welcome(self) -> None:
        """Print welcome message"""
        print("🚢 Welcome to Battleships!")
        print("Find all 3 battleships in 5 attempts.")
        print("Enter positions 1-10, or 'exit' to quit.\n")
        
        if self._debug_mode:
            print("🐛 DEBUG MODE: Battleship positions will be visible\n")
    
    def _ask_play_again(self) -> bool:
        """Ask if user wants to play (again)"""
        while True:
            try:
                response = input("Do you want to play? (y/n): ").strip().lower()
                if response in ['y', 'yes', 'sure']:
                    return True
                elif response in ['n', 'no', 'e', 'exit', 'q', 'quit']:
                    return False
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return False
    
    def _play_game(self) -> None:
        """Play a single game"""
        # Initialize the game
        self._engine.initialize_game()
        
        print("\nNew game started!")
        self._display_game_state()
        
        # Main game loop
        while not self._engine.is_game_over():
            try:
                position = self._get_user_input()
                if position is None:  # User wants to exit
                    print("Game exited.")
                    break
                
                # Make the guess
                result = self._engine.make_guess(position)
                
                if 'error' in result:
                    print(f"❌ {result['error']}")
                    continue
                
                # Display result message
                print(f"💥 {result['message']}")
                
                # Display updated game state
                self._display_game_state()
                
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted. Goodbye!")
                break
        
        # Display final result
        self._display_final_result()

    def _get_user_input(self) -> int | None:
        """Get and validate user input"""
        while True:
            try:
                user_input = input("Enter your guess (1-10): ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q', 'e']:
                    return None
                
                position = int(user_input)
                if 1 <= position <= 10:
                    return position
                else:
                    print("❌ Please enter a number between 1 and 10.")
                    
            except ValueError:
                print("❌ Please enter a valid number or 'exit' to quit.")
            except (EOFError, KeyboardInterrupt):
                return None
    
    def _display_game_state(self) -> None:
        """Display the current game state"""
        # Display board
        board_display = self._engine.get_board_display(self._debug_mode)
        print(board_display)
        
        # Display stats
        state = self._engine.get_game_state()
        print(f"Attempts left: {state['attempts_remaining']}, "
              f"Battleships sunk: {state['battleships_sunk']}/"
              f"{state['total_battleships']}\n")
    
    def _display_final_result(self) -> None:
        """Display the final game result"""
        result = self._engine.get_game_result()
        
        if result == GameResult.WIN:
            print("🎉 Congratulations! You've sunk all the battleships!")
        elif result == GameResult.LOSE:
            print("💥 Game over! You've run out of attempts.")
            print("Better luck next time!")
        
        # Show final board with all battleships revealed
        print("\nFinal board (with all battleships revealed):")
        final_board = self._engine.get_board_display(show_battleships=True)
        print(final_board)


def main():
    """Main entry point for console game"""
    parser = argparse.ArgumentParser(description='Battleships Console Game')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode (show battleship positions)')
    
    args = parser.parse_args()
    
    adapter = ConsoleGameAdapter(debug_mode=args.debug)
    adapter.run()


if __name__ == "__main__":
    main()
