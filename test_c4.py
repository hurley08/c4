import pytest
import numpy as np
from unittest.mock import patch
from _c4 import ConnectFour


@pytest.fixture
def game_6x7():
    from _c4 import ConnectFour

    return ConnectFour(rows=6, cols=7, test=True)


@pytest.mark.parametrize(
    "col_test",
    [10, 15, 24],
)
@pytest.mark.parametrize(
    "target",
    [i for i in range(7)],
)
def test_drop_piece_valid(target, col_test):
    game = ConnectFour(rows=6, cols=col_test, test=False)

    assert game.drop_piece(target)  # Should return True for a valid move
    assert (
        game.board[0][target] == 1
    )  # Check if the piece was dropped in the correct position


def test_drop_piece_invalid_1(game_6x7):
    game = game_6x7
    assert not game.drop_piece(
        8
    )  # Should return False for a column that is already full


def test_drop_piece_invalid_2(game_6x7):
    game = game_6x7
    assert not game.drop_piece(
        8
    )  # Should return False for a column that is already full

def game_15x15():
    # Test if engine can make a big board
    from _c4 import ConnectFour
    assert ConnectFour(rows=15, cols=15, tests=True)

def game_30x30():
    # Test if engine can make an even bigger board
    from _c4 import ConnectFour
    assert ConnectFour(rows=30, cols=30, tests=True)

def test_is_full(game_6x7):
    game = game_6x7
    assert not game.is_full()  # Initially, the board is not full

    # Fill the board
    game.board[:, :] = 1
    assert game.is_full()  # Now, the board is full


def test_check_winner_horizontal(game_6x7):
    # Test horizontal win
    game = game_6x7
    game.board[0:4, 0] = 1
    assert game.check_winner()


def test_check_winner_vertical(game_6x7):
    # Test vertical win
    game = game_6x7
    game.board[0, 0:4] = 1
    assert game.check_winner()


def test_check_winner_diagonal(game_6x7):
    # Test diagonal win
    game = game_6x7
    game.board[0, 0] = game.board[1, 1] = game.board[2, 2] = game.board[3, 3] = 1
    assert game.check_winner()


def test_no_winner(game_6x7):
    # Test no winner
    game = game_6x7
    assert not game.check_winner()


def test_switch_player(game_6x7):
    # Test switch player method is functional
    game = game_6x7
    assert game.current_player == 1
    game.switch_player()
    assert game.current_player == 2
    game.switch_player()
    assert game.current_player == 1


if __name__ == "__main__":
    pytest.main()
