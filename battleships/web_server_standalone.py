#!/usr/bin/env python3
"""
Flask web server for Battleships game using the web adapter
"""

try:
    from flask import Flask, jsonify, render_template, request
    from flask_cors import CORS
except ImportError:
    print("Flask not installed. Install with: pip install Flask Flask-CORS")
    exit(1)

from adapters.web_adapter import WebGameAPI

app = Flask(__name__, 
           template_folder='web/templates', 
           static_folder='web/static')
CORS(app)

# Global game API instance
game_api = WebGameAPI()


@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')


@app.route('/api/game', methods=['POST'])
def create_game():
    """Create a new game session"""
    data = request.get_json() or {}
    debug_mode = data.get('debug_mode', False)
    
    result = game_api.create_game(debug_mode)
    return jsonify(result)


@app.route('/api/game/<session_id>/start', methods=['POST'])
def start_game(session_id):
    """Start a game session"""
    result = game_api.start_game(session_id)
    return jsonify(result)


@app.route('/api/game/<session_id>/guess', methods=['POST'])
def submit_guess(session_id):
    """Submit a guess"""
    data = request.get_json()
    if not data or 'position' not in data:
        return jsonify({'error': 'Position required'}), 400
        
    position = data['position']
    result = game_api.submit_guess(session_id, position)
    return jsonify(result)


@app.route('/api/game/<session_id>/state', methods=['GET'])
def get_game_state(session_id):
    """Get current game state"""
    result = game_api.get_game_state(session_id)
    return jsonify(result)


@app.route('/api/game/<session_id>', methods=['DELETE'])
def delete_game(session_id):
    """Delete a game session"""
    result = game_api.delete_game(session_id)
    return jsonify(result)


@app.route('/api/games', methods=['GET'])
def list_games():
    """List all active games"""
    result = game_api.list_games()
    return jsonify(result)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'battleships-game',
        'version': '1.0.0'
    })


def main():
    """Main entry point for the web server"""
    print("🚢 Starting Battleships Web Server...")
    print("📋 Game Engine: Standalone")
    print("🌐 Access the game at: http://localhost:5000")
    print("🔧 API endpoints at: http://localhost:5000/api/")
    print("❤️  Health check at: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the server.\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()