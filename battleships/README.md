# Battleships Game - Standalone Engine with Platform Adapters

A professional, platform-agnostic implementation of the classic Battleships game with a clean separation between game logic and platform-specific interfaces.

## Architecture Overview

This implementation follows a **standalone engine + adapter pattern** where:
- **Core Engine**: Contains pure game logic with no I/O dependencies
- **Platform Adapters**: Handle platform-specific concerns (console, web, etc.)
- **Complete Decoupling**: Engine can be used by any platform without modification

## Features

- 🎯 **Standalone Game Engine**: Pure logic, no platform dependencies
- 🖥️ **Console Adapter**: Rich terminal interface with debug mode
- 🌐 **Web Adapter**: RESTful API for browser-based games
- 🏗️ **SOLID Principles**: Clean, maintainable, extensible architecture
- 🔧 **Design Patterns**: Strategy, Factory, Adapter, Session Management
- 🧪 **Easy Testing**: Mock any component independently
- 📝 **Type Hints**: Full type safety and IDE support
- 🔄 **Session Management**: Multiple concurrent games with cleanup

## Project Structure

```
battleships/
├── battleships_oop/                    # Core game engine (platform-agnostic)
│   ├── __init__.py                    # Engine exports
│   ├── engine.py                      # Pure game logic engine  
│   ├── models.py                      # Data models and enums
│   ├── board.py                       # Board management
│   └── game_state.py                  # Game state management
├── adapters/                          # Platform-specific adapters
│   ├── __init__.py                    # Adapter exports
│   ├── console_adapter.py             # Console/terminal interface
│   └── web_adapter.py                 # Web/HTTP interface
├── web/                               # Web interface assets
│   ├── templates/
│   │   └── index.html                # Game UI
│   └── static/
│       ├── style.css                 # Game styling
│       └── game.js                   # Client-side JavaScript
├── battleships_functional_method.py   # Original functional implementation
├── console_game.py                    # Console game launcher
├── console_debug_game.py              # Console debug launcher
├── demo_standalone.py                 # Engine demonstration
├── web_server_standalone.py           # Web server launcher
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Core Design Patterns

### 1. **Adapter Pattern**
- **Console Adapter**: Translates engine calls to terminal I/O
- **Web Adapter**: Translates engine calls to HTTP/JSON APIs
- **Pluggable Architecture**: Any platform can implement an adapter

### 2. **Engine Pattern**
- **Pure Logic**: `BattleshipEngine` contains only game rules
- **No I/O Dependencies**: Engine never calls print(), input(), or network
- **Stateful**: Engine maintains game state internally

### 3. **Session Management**
- **Multi-tenancy**: Web adapter supports multiple concurrent games
- **Auto-cleanup**: Inactive sessions are automatically removed
- **Thread-safe**: Concurrent access protection with locks

## SOLID Principles in Action

### Single Responsibility Principle (SRP)
- **Engine**: Game logic only
- **Board**: Position and state management only
- **GameState**: Progress tracking only
- **Adapters**: Platform-specific I/O only

### Open/Closed Principle (OCP)
- **New Platforms**: Add adapters without changing engine
- **New Features**: Extend engine without breaking adapters
- **New Game Modes**: Modify rules without touching I/O

### Dependency Inversion Principle (DIP)
- **Adapters depend on Engine**: Not the other way around
- **Engine is Pure**: No dependencies on external systems
- **Clean Boundaries**: Clear contracts between layers

## Usage

### Console Game
```bash
# Normal mode
python3 console_game.py

# Debug mode (shows battleship positions)
python3 console_debug_game.py
```

### Web Game
```bash
# Install dependencies
pip install -r requirements.txt

# Start web server
python3 web_server_standalone.py

# Access at http://localhost:5000
```

### Engine Usage (for developers)
```python
from battleships_oop.engine import BattleshipEngine

# Create engine instance
engine = BattleshipEngine(max_attempts=5, battleship_count=3)

# Initialize game
state = engine.initialize_game()
print(f"Game started: {state['game_initialized']}")

# Make guesses
result = engine.make_guess(5)
print(f"Result: {result['message']}")

# Get board display
board = engine.get_board_display(show_battleships=False)
print(board)

# Check if game is over
if engine.is_game_over():
    print(f"Game result: {engine.get_game_result().value}")
```

### Adapter Usage (for platform developers)
```python
from adapters.web_adapter import WebGameAdapter

# Create web adapter
adapter = WebGameAdapter()

# Create and manage sessions
session = adapter.create_session(debug_mode=True)
session_id = session['session_id']

# Initialize game
game_state = adapter.initialize_game(session_id)

# Make moves
result = adapter.make_guess(session_id, 5)

# Clean up
adapter.delete_session(session_id)
```

## Game Rules

- **Board**: 10 positions (1-10)
- **Battleships**: 3 randomly placed
- **Attempts**: 5 chances to find all battleships
- **Symbols**: Hit='F', Miss='M', Empty=' ', Battleship='B' (debug only)
- **Win Condition**: Find all battleships before running out of attempts

## API Endpoints (Web)

### Create Game
```http
POST /api/game
Content-Type: application/json

{
  "debug_mode": false
}
```

### Start Game
```http
POST /api/game/<session_id>/start
```

### Submit Guess
```http
POST /api/game/<session_id>/guess
Content-Type: application/json

{
  "position": 5
}
```

### Get Game State
```http
GET /api/game/<session_id>/state
```

### Delete Game
```http
DELETE /api/game/<session_id>
```

### List All Games
```http
GET /api/games
```

## Creating New Platform Adapters

To add support for a new platform (mobile, desktop, etc.), create an adapter:

```python
from battleships_oop.engine import BattleshipEngine

class MyPlatformAdapter:
    def __init__(self):
        self.engine = BattleshipEngine()
    
    def start_game(self):
        # Initialize engine
        state = self.engine.initialize_game()
        
        # Display using your platform's UI
        self.display_board(state)
    
    def handle_user_input(self, position):
        # Get input from your platform
        result = self.engine.make_guess(position)
        
        # Show result using your platform's UI
        self.show_message(result['message'])
        self.display_board(result)
    
    # Implement platform-specific display methods
    def display_board(self, state): pass
    def show_message(self, message): pass
```

## Testing

### Unit Testing the Engine
```python
from battleships_oop.engine import BattleshipEngine
from battleships_oop.models import GameResult

def test_engine():
    engine = BattleshipEngine()
    
    # Test initialization
    state = engine.initialize_game()
    assert state['game_initialized'] == True
    assert state['battleships_sunk'] == 0
    
    # Test invalid guess
    result = engine.make_guess(0)  # Invalid position
    assert 'error' in result
    
    # Test valid guess
    result = engine.make_guess(5)
    assert 'message' in result
    assert result['position'] == 5
```

### Integration Testing
```bash
# Test console adapter
python3 console_debug_game.py

# Test web adapter
python3 adapters/web_adapter.py
```

## Dependencies

### Core Engine
- **No external dependencies** - pure Python 3.7+

### Console Adapter
- **No external dependencies** - uses built-in modules only

### Web Adapter
- `Flask>=3.0.0` - Web framework
- `Flask-CORS>=4.0.0` - Cross-origin resource sharing

Install web dependencies:
```bash
pip install -r requirements.txt
```

## Architecture Benefits

### For Game Developers
- **Pure Engine**: Embed in any application
- **No Side Effects**: Engine never touches I/O
- **Predictable**: Same inputs always produce same outputs
- **Testable**: Mock-free unit testing

### For Platform Developers  
- **Clean Interface**: Simple method calls, JSON responses
- **Session Management**: Built-in multi-user support
- **Thread Safety**: Concurrent access protection
- **Auto-cleanup**: No memory leaks from abandoned sessions

### For DevOps
- **Containerizable**: Engine has no OS dependencies
- **Scalable**: Web adapter supports load balancing
- **Monitorable**: Clear separation of concerns
- **Debuggable**: Debug mode for troubleshooting

This architecture demonstrates how to build truly reusable game engines that can power multiple platforms without coupling to any specific technology stack.
