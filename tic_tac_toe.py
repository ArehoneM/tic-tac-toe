import sys
import json

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def display_board(board):
    return "\n".join(["|".join(row) for row in board])

def parse_issue(issue_body):
    try:
        lines = issue_body.split("\n")
        player = lines[0].split(":")[1].strip()
        move = tuple(map(int, lines[1].split(":")[1].strip().split(",")))
        return player, move
    except Exception as e:
        raise ValueError("Invalid issue format. Expected:\nPlayer: X\nMove: 1,2")

def is_valid_move(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " "

def make_move(board, row, col, player):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

if __name__ == "__main__":
    # Load the board from a file or initialize a new one
    try:
        with open("board.json", "r") as f:
            board = json.load(f)
    except FileNotFoundError:
        board = initialize_board()

    # Parse the issue content
    issue_body = sys.argv[1]
    try:
        player, (row, col) = parse_issue(issue_body)
        row, col = row - 1, col - 1  # Convert to 0-indexed
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Process the move
    if not make_move(board, row, col, player):
        print("Invalid move. Try again.")
        sys.exit(1)

    # Check for winner or draw
    winner = check_winner(board)
    if winner:
        print(f"Player {winner} wins!")
    elif is_draw(board):
        print("It's a draw!")
    else:
        print("Next player's turn.")

    # Save the updated board
    with open("board.json", "w") as f:
        json.dump(board, f)

    # Output the updated board
    print("Current board:")
    print(display_board(board))
