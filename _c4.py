import numpy as np
import random


class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1

    def print_board(self):
        for row in reversed(range(self.rows)):
            print("|", end="")
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    print("   |", end="")
                elif self.board[row][col] == 1:
                    print(" X |", end="")
                elif self.board[row][col] == 2:
                    print(" O |", end="")
            print()
            print("|---" * self.cols + "|")

    def drop_piece(self, col):
        for row in range(self.rows):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False

    def check_winner(self):
        # Check rows
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col]
                    == self.board[row][col + 1]
                    == self.board[row][col + 2]
                    == self.board[row][col + 3]
                    != 0
                ):
                    return True

        # Check columns
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                    != 0
                ):
                    return True

        # Check diagonals
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col + 1]
                    == self.board[row + 2][col + 2]
                    == self.board[row + 3][col + 3]
                    != 0
                ):
                    return True

        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col]
                    == self.board[row - 1][col + 1]
                    == self.board[row - 2][col + 2]
                    == self.board[row - 3][col + 3]
                    != 0
                ):
                    return True

        return False

    def is_full(self):
        return np.all(self.board != 0)

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switch between 1 and 2

    def play_game(self):
        while not self.check_winner() and not self.is_full():
            while True:
                # self.print_board()
                col = input(
                    f"Player {self.current_player}, choose a column (1-{self.cols}): "
                )
                try:
                    col = int(col)
                    col -= 1
                    if 0 <= col < self.cols and self.drop_piece(col):
                        if self.check_winner():
                            # self.print_board()
                            print(f"Player {self.current_player} wins!")
                            break
                        elif self.is_full():
                            self.print_board()
                            print("It's a tie!")
                            break
                        self.switch_player()
                except ValueError:
                    break
                print("Invalid move. Try again.")


if __name__ == "__main__":
    game = ConnectFour(rows=8, cols=10)
    game.play_game()
