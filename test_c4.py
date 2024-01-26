import pytest
import numpy as np
from unittest.mock import patch
from _c4 import ConnectFour


@pytest.mark.parametrize(
    "col_test",
    [10, 15, 24],
)
@pytest.mark.parametrize(
    "target",
    [i for i in range(7)],
)
def test_drop_piece_valid(target, col_test):
    game = ConnectFour(rows=6, cols=col_test)

    assert game.drop_piece(target)  # Should return True for a valid move
    assert (
        game.board[0][target] == 1
    )  # Check if the piece was dropped in the correct position


def test_drop_piece_invalid_1():
    game = ConnectFour(rows=6, cols=7, test=True)
    assert not game.drop_piece(
        8
    )  # Should return False for a column that is already full


@pytest.mark.xfail
def test_drop_piece_invalid_2():
    game = ConnectFour(rows=6, cols=7, test=False)
    assert not game.drop_piece(
        8
    )  # Should return False for a column that is already full


def test_is_full():
    game = ConnectFour(rows=2, cols=2)
    assert not game.is_full()  # Initially, the board is not full

    # Fill the board
    game.board[:, :] = 1
    assert game.is_full()  # Now, the board is full


def test_check_winner_horizontal():
    # Test horizontal win
    game = ConnectFour(rows=6, cols=7)
    game.board[0:4, 0] = 1
    assert game.check_winner()


def test_check_winner_vertical():
    # Test vertical win
    game = ConnectFour(rows=6, cols=7)
    game.board[0, 0:4] = 1
    assert game.check_winner()


def test_check_winner_diagonal():
    # Test diagonal win
    game = ConnectFour(rows=6, cols=7)
    game.board[0, 0] = game.board[1, 1] = game.board[2, 2] = game.board[3, 3] = 1
    assert game.check_winner()


def test_no_winner():
    # Test no winner
    game = ConnectFour(rows=6, cols=7)
    assert not game.check_winner()


def test_switch_player():
    game = ConnectFour(rows=2, cols=2)

    assert game.current_player == 1
    game.switch_player()
    assert game.current_player == 2
    game.switch_player()
    assert game.current_player == 1


if __name__ == "__main__":
    pytest.main()
