#!/usr/bin/env python3
"""
Console Battleships Game - Standalone version using the game engine
"""

from adapters.console_adapter import ConsoleGameAdapter


def main():
    """Main entry point for console battleships game"""
    try:
        adapter = ConsoleGameAdapter(debug_mode=False)
        adapter.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 🚢")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()