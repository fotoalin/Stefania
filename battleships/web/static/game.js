// Battleships Game JavaScript Client
class BattleshipGame {
    constructor() {
        this.gameId = null;
        this.gameRunning = false;
        this.isDebugMode = false;
        
        this.initializeElements();
        this.attachEventListeners();
        this.initializeBoard();
    }
    
    initializeElements() {
        this.startBtn = document.getElementById('startBtn');
        this.debugBtn = document.getElementById('debugBtn');
        this.exitBtn = document.getElementById('exitBtn');
        this.gameStatus = document.getElementById('gameStatus');
        this.gameStats = document.getElementById('gameStats');
        this.boardCells = document.getElementById('boardCells');
        this.messageLog = document.getElementById('messageLog');
        this.clickInstruction = document.getElementById('clickInstruction');
    }
    
    attachEventListeners() {
        this.startBtn.addEventListener('click', () => this.startGame(false));
        this.debugBtn.addEventListener('click', () => this.startGame(true));
        this.exitBtn.addEventListener('click', () => this.exitGame());
    }
    
    initializeBoard() {
        this.boardCells.innerHTML = '';
        for (let i = 1; i <= 10; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.position = i;
            cell.textContent = ' ';
            cell.addEventListener('click', () => this.handleCellClick(i));
            this.boardCells.appendChild(cell);
        }
    }
    
    async startGame(debugMode = false) {
        try {
            this.isDebugMode = debugMode;
            this.updateStatus('Creating game...', 'info');
            this.setButtonsEnabled(false);
            
            // Create game
            const createResponse = await fetch('/api/game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ debug_mode: debugMode })
            });
            
            const createResult = await createResponse.json();
            if (createResult.error) {
                throw new Error(createResult.error);
            }
            
            this.gameId = createResult.game_id;
            
            // Start game
            const startResponse = await fetch(`/api/game/${this.gameId}/start`, {
                method: 'POST'
            });
            
            const startResult = await startResponse.json();
            if (startResult.error) {
                throw new Error(startResult.error);
            }
            
            this.gameRunning = true;
            this.updateGameState(startResult);
            this.setGameControlsEnabled(true);
            
            this.addLogMessage('Game started! Find all 3 battleships.', 'success');
            
        } catch (error) {
            this.updateStatus(`Error: ${error.message}`, 'error');
            this.setButtonsEnabled(true);
        }
    }
    
    async handleCellClick(position) {
        if (!this.gameRunning) {
            this.addLogMessage('Please start a game first!', 'error');
            return;
        }
        
        // Check if cell already has a result
        const cell = document.querySelector(`[data-position="${position}"]`);
        if (cell.classList.contains('hit') || cell.classList.contains('miss')) {
            this.addLogMessage(`Position ${position} has already been guessed!`, 'error');
            return;
        }
        
        try {
            this.setGameControlsEnabled(false);
            this.updateStatus(`Making guess at position ${position}...`, 'info');
            
            // Add visual feedback for the clicked cell
            cell.style.transform = 'scale(0.9)';
            setTimeout(() => {
                cell.style.transform = '';
            }, 150);
            
            const response = await fetch(`/api/game/${this.gameId}/guess`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position })
            });
            
            const result = await response.json();
            if (result.error) {
                throw new Error(result.error);
            }
            
            this.updateGameState(result);
            
            if (result.game_running && result.waiting_for_input) {
                this.setGameControlsEnabled(true);
            }
            
        } catch (error) {
            this.addLogMessage(`Error: ${error.message}`, 'error');
            this.setGameControlsEnabled(true);
        }
    }
    
    async exitGame() {
        if (!this.gameId) return;
        
        try {
            await fetch(`/api/game/${this.gameId}/exit`, {
                method: 'POST'
            });
            
            this.gameRunning = false;
            this.gameId = null;
            this.updateStatus('Game exited', 'info');
            this.setButtonsEnabled(true);
            this.setGameControlsEnabled(false);
            this.initializeBoard();
            
        } catch (error) {
            this.addLogMessage(`Error exiting game: ${error.message}`, 'error');
        }
    }
    
    updateGameState(state) {
        // Update board display
        this.updateBoard(state.board);
        
        // Update status
        if (state.message) {
            this.addLogMessage(state.message, this.getMessageType(state.message));
            
            if (state.message.includes('Congratulations')) {
                this.updateStatus('🎉 You won! All battleships found!', 'success');
                this.gameRunning = false;
                this.setButtonsEnabled(true);
                this.setGameControlsEnabled(false);
                this.clickInstruction.innerHTML = '<p>🎉 Congratulations! Click "Start New Game" to play again!</p>';
            } else if (state.message.includes('Game over')) {
                this.updateStatus('💥 Game over! Better luck next time!', 'error');
                this.gameRunning = false;
                this.setButtonsEnabled(true);
                this.setGameControlsEnabled(false);
                this.clickInstruction.innerHTML = '<p>💥 Game over! Click "Start New Game" to try again!</p>';
            } else if (state.waiting_for_input) {
                this.updateStatus('Your turn - make a guess!', 'info');
            }
        }
        
        // Update stats from board display
        this.updateStatsFromBoard(state.board);
    }
    
    updateBoard(boardDisplay) {
        if (!boardDisplay) return;
        
        const lines = boardDisplay.split('\n');
        const boardLine = lines.find(line => line.includes(' ') && !line.includes('-') && !line.match(/^\d/));
        
        if (boardLine) {
            const cells = boardLine.trim().split(/\s+/);
            const cellElements = document.querySelectorAll('.cell');
            
            cells.forEach((cellValue, index) => {
                if (index < cellElements.length) {
                    const cell = cellElements[index];
                    cell.textContent = cellValue === ' ' ? ' ' : cellValue;
                    
                    // Update cell appearance
                    cell.className = 'cell';
                    if (cellValue === 'F') {
                        cell.classList.add('hit');
                        cell.textContent = '💥';
                    } else if (cellValue === 'M') {
                        cell.classList.add('miss');
                        cell.textContent = '🌊';
                    } else if (cellValue === 'B' && this.isDebugMode) {
                        cell.classList.add('battleship');
                        cell.textContent = '🚢';
                    } else if (this.gameRunning) {
                        cell.classList.add('clickable');
                    }
                }
            });
        }
    }
    
    updateStatsFromBoard(boardDisplay) {
        if (!boardDisplay) return;
        
        const lines = boardDisplay.split('\n');
        const boardLine = lines.find(line => line.includes(' ') && !line.includes('-') && !line.match(/^\d/));
        
        if (boardLine) {
            const cells = boardLine.trim().split(/\s+/);
            const hits = cells.filter(cell => cell === 'F').length;
            const misses = cells.filter(cell => cell === 'M').length;
            const remaining = 3 - hits;
            const attempts = 5 - (hits + misses);
            
            this.gameStats.innerHTML = `
                Battleships found: ${hits}/3 | 
                Attempts remaining: ${Math.max(0, attempts)} | 
                Misses: ${misses}
            `;
        }
    }
    
    updateStatus(message, type = 'info') {
        this.gameStatus.textContent = message;
        this.gameStatus.className = `status ${type}`;
    }
    
    setButtonsEnabled(enabled) {
        this.startBtn.disabled = !enabled;
        this.debugBtn.disabled = !enabled;
    }
    
    setGameControlsEnabled(enabled) {
        this.exitBtn.disabled = !enabled;
        
        // Update cell clickability
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            if (enabled && !cell.classList.contains('hit') && !cell.classList.contains('miss')) {
                cell.classList.add('clickable');
            } else {
                cell.classList.remove('clickable');
            }
        });
        
        // Update click instruction
        if (enabled) {
            this.clickInstruction.innerHTML = '<p>🎯 Click on any empty cell to make your guess!</p>';
        } else {
            this.clickInstruction.innerHTML = '<p>Start a game to begin clicking on cells!</p>';
        }
    }
    
    addLogMessage(message, type = 'info') {
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
        
        this.messageLog.appendChild(logEntry);
        this.messageLog.scrollTop = this.messageLog.scrollHeight;
    }
    
    getMessageType(message) {
        if (message.includes('Sunk') || message.includes('Congratulations')) {
            return 'success';
        } else if (message.includes('Miss') || message.includes('Game over')) {
            return 'error';
        } else {
            return 'info';
        }
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    new BattleshipGame();
});