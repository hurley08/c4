def print_board(board):
    for row in board:
        print("|".join(row))
    print("1 2 3 4 5 6 7")


def check_winner(board, player):
    # Check horizontal
    for row in board:
        for i in range(4):
            if row[i : i + 4] == [player] * 4:
                return True

    # Check vertical
    for col in range(7):
        for i in range(3):
            if [board[j][col] for j in range(i, i + 4)] == [player] * 4:
                return True

    # Check diagonal (from top-left to bottom-right)
    for i in range(3):
        for j in range(4):
            if [board[i + k][j + k] for k in range(4)] == [player] * 4:
                return True

    # Check diagonal (from top-right to bottom-left)
    for i in range(3):
        for j in range(3, 7):
            if [board[i + k][j - k] for k in range(4)] == [player] * 4:
                return True

    return False


def is_board_full(board):
    return all(cell != " " for row in board for cell in row)


def main():
    board = [[" " for _ in range(7)] for _ in range(6)]
    players = ["X", "O"]
    turn = 0

    while True:
        print_board(board)
        player = players[turn % 2]
        column = int(input(f"Player {player}, choose a column (1-7): ")) - 1

        # Check if the chosen column is valid
        if 0 <= column < 7 and board[0][column] == " ":
            # Find the lowest empty row in the chosen column
            for row in range(5, -1, -1):
                if board[row][column] == " ":
                    board[row][column] = player
                    break

            # Check for a winner
            if check_winner(board, player):
                print_board(board)
                print(f"Player {player} wins!")
                break

            # Check for a tie
            if is_board_full(board):
                print_board(board)
                print("It's a tie!")
                break

            turn += 1
        else:
            print("Invalid move. Please choose a valid column.")


if __name__ == "__main__":
    main()
