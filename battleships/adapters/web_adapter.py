"""
Web adapter for the Battleships game engine
"""

import json
import os
import sys
import time
import uuid
from threading import Lock, Thread
from typing import Any, Dict, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from battleships.engine import BattleshipEngine
from battleships.models import GameResult


class WebGameSession:
    """Represents a single web game session"""
    
    def __init__(self, session_id: str, debug_mode: bool = False):
        self.session_id = session_id
        self.debug_mode = debug_mode
        self.engine = BattleshipEngine()
        self.created_at = time.time()
        self.last_activity = time.time()
        self._lock = Lock()
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize the game session"""
        with self._lock:
            self.last_activity = time.time()
            result = self.engine.initialize_game()
            result.update({
                'game_id': self.session_id,
                'session_id': self.session_id,
                'debug_mode': self.debug_mode,
                'board_display': self.engine.get_board_display(self.debug_mode),
                'timestamp': self.last_activity
            })
            return result
    
    def make_guess(self, position: int) -> Dict[str, Any]:
        """Make a guess in this session"""
        with self._lock:
            self.last_activity = time.time()
            result = self.engine.make_guess(position)
            result.update({
                'game_id': self.session_id,
                'session_id': self.session_id,
                'board_display': self.engine.get_board_display(self.debug_mode),
                'timestamp': self.last_activity
            })
            return result
    
    def get_state(self) -> Dict[str, Any]:
        """Get current session state"""
        with self._lock:
            state = self.engine.get_game_state()
            state.update({
                'game_id': self.session_id,
                'session_id': self.session_id,
                'debug_mode': self.debug_mode,
                'board_display': self.engine.get_board_display(self.debug_mode),
                'created_at': self.created_at,
                'last_activity': self.last_activity,
                'timestamp': time.time()
            })
            return state


class WebGameAdapter:
    """Web adapter for managing multiple game sessions"""
    
    def __init__(self):
        self._sessions: Dict[str, WebGameSession] = {}
        self._lock = Lock()
        
        # Start cleanup thread
        self._cleanup_thread = Thread(target=self._cleanup_old_sessions, 
                                     daemon=True)
        self._cleanup_thread.start()
    
    def create_session(self, debug_mode: bool = False) -> Dict[str, Any]:
        """Create a new game session"""
        session_id = str(uuid.uuid4())
        
        with self._lock:
            session = WebGameSession(session_id, debug_mode)
            self._sessions[session_id] = session
        
        return {
            'game_id': session_id,  # Use game_id for JavaScript compatibility
            'session_id': session_id,  # Keep session_id for internal consistency
            'debug_mode': debug_mode,
            'status': 'Session created'
        }
    
    def initialize_game(self, session_id: str) -> Dict[str, Any]:
        """Initialize a game in the given session"""
        session = self._get_session(session_id)
        if not session:
            return {'error': 'Session not found'}
        
        return session.initialize()
    
    def make_guess(self, session_id: str, position: int) -> Dict[str, Any]:
        """Make a guess in the given session"""
        session = self._get_session(session_id)
        if not session:
            return {'error': 'Session not found'}
        
        return session.make_guess(position)
    
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """Get the state of a specific session"""
        session = self._get_session(session_id)
        if not session:
            return {'error': 'Session not found'}
        
        return session.get_state()
    
    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a game session"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return {'status': 'Session deleted'}
            else:
                return {'error': 'Session not found'}
    
    def list_sessions(self) -> Dict[str, Any]:
        """List all active sessions"""
        with self._lock:
            sessions_info = {}
            for session_id, session in self._sessions.items():
                sessions_info[session_id] = {
                    'debug_mode': session.debug_mode,
                    'created_at': session.created_at,
                    'last_activity': session.last_activity,
                    'game_result': session.engine.get_game_result().value,
                    'is_game_over': session.engine.is_game_over()
                }
        
        return {'sessions': sessions_info, 'total': len(sessions_info)}
    
    def _get_session(self, session_id: str) -> Optional[WebGameSession]:
        """Get a session by ID"""
        with self._lock:
            return self._sessions.get(session_id)
    
    def _cleanup_old_sessions(self) -> None:
        """Cleanup thread to remove old inactive sessions"""
        while True:
            time.sleep(300)  # Check every 5 minutes
            current_time = time.time()
            
            with self._lock:
                expired_sessions = []
                for session_id, session in self._sessions.items():
                    # Remove sessions inactive for more than 1 hour
                    if current_time - session.last_activity > 3600:
                        expired_sessions.append(session_id)
                
                for session_id in expired_sessions:
                    del self._sessions[session_id]
                
                if expired_sessions:
                    print(f"Cleaned up {len(expired_sessions)} expired sessions")


class WebGameAPI:
    """RESTful API interface using the web adapter"""
    
    def __init__(self):
        self.adapter = WebGameAdapter()
    
    def create_game(self, debug_mode: bool = False) -> Dict[str, Any]:
        """API endpoint to create a new game"""
        return self.adapter.create_session(debug_mode)
    
    def start_game(self, session_id: str) -> Dict[str, Any]:
        """API endpoint to start/initialize a game"""
        return self.adapter.initialize_game(session_id)
    
    def submit_guess(self, session_id: str, position: int) -> Dict[str, Any]:
        """API endpoint to submit a guess"""
        return self.adapter.make_guess(session_id, position)
    
    def get_game_state(self, session_id: str) -> Dict[str, Any]:
        """API endpoint to get game state"""
        return self.adapter.get_session_state(session_id)
    
    def delete_game(self, session_id: str) -> Dict[str, Any]:
        """API endpoint to delete a game"""
        return self.adapter.delete_session(session_id)
    
    def list_games(self) -> Dict[str, Any]:
        """API endpoint to list all games"""
        return self.adapter.list_sessions()


def main():
    """Simple test of the web adapter"""
    print("Testing Web Game Adapter...")
    
    adapter = WebGameAdapter()
    
    # Create a session
    result = adapter.create_session(debug_mode=True)
    session_id = result['session_id']
    print(f"Created session: {session_id}")
    
    # Initialize game
    result = adapter.initialize_game(session_id)
    print(f"Board:\n{result['board_display']}")
    
    # Make some guesses
    for pos in [1, 5, 10]:
        result = adapter.make_guess(session_id, pos)
        print(f"Guess {pos}: {result.get('message', 'No message')}")
        if 'error' not in result:
            print(f"Board:\n{result['board_display']}")
    
    # List sessions
    sessions = adapter.list_sessions()
    print(f"Active sessions: {sessions['total']}")
    
    # Clean up
    adapter.delete_session(session_id)
    print("Session deleted.")


if __name__ == "__main__":
    main()