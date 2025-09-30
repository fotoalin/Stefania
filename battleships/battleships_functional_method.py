

"""
the program should generate 3 random numbers between 0 and 9 and
place a 'B' on the board, at the random index positions.

The user has 5 attempts to guess the location of the battleship.

There should be 3 battleships on the board. 
Once the battleships are sunk or the user runs out of attempts, the game ends.

Once a battleship is found, the computer outputs "sunk" and changes the space to an F (found). If the computer misses, the blank space is turned to an M.

"""

from random import randint

board = [' ' for _ in range(10)]


def show_debug_board(debug=False):
    # display the board for debugging purposes
    if debug is True:
        print(" ".join([str(i) for i in range(10)]))
        print("-" * (len(board) * 2))
        print(" ".join(board))
        print("-" * (len(board) * 2))
        return

    # display the board for the user
    print(" ".join([str(i+1) for i in range(10)]))
    print("-" * (len(board) * 2))
    display_board = [' ' if space == 'B' else space for space in board]
    print(" ".join(display_board))
    print("-" * (len(board) * 2))


def place_battleships(num_battleships=3):
    """
        Randomly place battleships on the board.
        Each battleship is marked with 'B' at a random position.
    """

    battleships = 0
    used_indices = set()  # unique indices to avoid placing multiple battleships in the same position

    while battleships < num_battleships:
        index = randint(0, 9)
        
        if index in used_indices:
            continue
        
        used_indices.add(index)
        
        # print(index)

        if board[index] == ' ':
            board[index] = 'B'
            battleships += 1


def get_user_guess():
    """
        Get a valid user guess between 1 and 10.
    """
    while True:
        try:
            guess = input("Enter your guess (1-10): ")
            if guess.lower() in ['exit', 'quit', 'q', 'e']:
                print("Exiting the game.")
                exit()
            guess = int(guess)
            if 1 <= guess <= 10:
                return guess - 1  # Convert to 0-based index for internal use
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")


def play_game():
    """
        Main game loop.
    """
    attempts = 5
    battleships_sunk = 0
    total_battleships = 3

    while attempts > 0 and battleships_sunk < total_battleships:
        guess = get_user_guess()

        if board[guess] == 'B':
            print("Sunk!")
            board[guess] = 'F'  # Mark as found
            battleships_sunk += 1
        elif board[guess] == ' ':
            print("Miss!")
            board[guess] = 'M'  # Mark as missed
        elif board[guess] in ['F', 'M']:
            print("You already guessed that position.")
        
        attempts -= 1
        show_debug_board(debug=False)
        print(f"Attempts left: {attempts}, Battleships sunk: {battleships_sunk}/{total_battleships}")

    if battleships_sunk == total_battleships:
        print("Congratulations! You've sunk all the battleships!")
    else:
        print("Game over! You've run out of attempts.")


def check_sunk():
    """
        Check if all battleships are sunk.
    """
    return all(space != 'B' for space in board)


def main():
    place_battleships()
    # show_debug_board()
    play_game()


if __name__ == "__main__":
    main()
