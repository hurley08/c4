import pytest
import numpy as np
from unittest.mock import patch
from _c4rl import ConnectFourRL, split_wins, return_stats


@pytest.fixture
def test_play_n_vary_smarts(n=50, sm0=None, sm1=None):
    game = ConnectFourRL(rows=6, cols=8, p1_smart=sm0, p2_smart=sm1, test=False)
    game_log = {}
    for i in range(n + 1)[1:]:
        game_log[i] = game.play_game()
    return game_log


@pytest.fixture
def game_obj():
    from _c4rl import ConnectFourRL

    game = ConnectFourRL(rows=6, cols=8, p1_smart=True, p2_smart=False, test=False)
    return game


@pytest.fixture
def Connect():
    from _c4rl import ConnectFourRL

    return ConnectFourRL


@pytest.fixture
def winner():
    from _c4rl import split_wins, return_stats

    return split_wins


@pytest.fixture
def compare():
    from _c4rl import compare_wins, return_stats

    return compare_wins


@pytest.fixture
def test_get_state():
    game = ConnectFourRL(rows=6, cols=7)
    state = game.get_state()

    assert isinstance(state, tuple)
    assert len(state) == 2
    assert isinstance(state[0], np.ndarray)
    assert isinstance(state[1], int)


def test_play_single_game():
    from _c4rl import ConnectFourRL as Connect

    game_obj = Connect(
        rows=8, cols=10, p1_smart=False, p2_smart=False, print_it=False, test=False
    )
    winner, moves = game_obj.play_game()
    assert winner
    # assert winner in [1, 2]  # The winner should be either player 1 or player 2
    # assert isinstance(moves, int)  # The number of moves should be an integer


def test_split_win(winner):
    from _c4rl import ConnectFourRL as Connect

    game_obj = Connect(
        rows=8, cols=10, p1_smart=False, p2_smart=False, print_it=False, test=False
    )
    game_log = {}
    game_log[1] = game_obj.play_game()
    split = winner(game_log)
    assert split


def test_compare_wins(winner):
    from _c4rl import ConnectFourRL as Connect

    game_obj = Connect(
        rows=8, cols=10, p1_smart=False, p2_smart=False, print_it=False, test=False
    )
    from _c4rl import compare_wins, split_wins

    game_log = {}
    game_log[1] = game_obj.play_game()
    split = split_wins(game_log)
    res = compare_wins(split[0], split[1])
    assert res


@pytest.mark.parametrize("ns", [10, 20, 50, 100])
@pytest.mark.parametrize(
    ("sm0", "sm1"),
    [(True, False), (False, False), (False, True), (True, True)],
)
def test_smarts_sweep(Connect, compare, winner, sm0, sm1, ns):
    try:
        game_log = {}
        for i in range(ns + 1)[1:]:
            game = Connect(rows=6, cols=8, p1_smart=sm0, p2_smart=sm1)
            game_log[i] = game.play_game()

    except:
        assert False
    results = split_wins(game_log)
    results = compare(results[0], results[1])
    print(
        f"p1_smart: {sm0} | p2_smart: {sm1} | N: {ns} | {results[0]} | {results[1]} | {results[2]}"
    )
    if sm0 == True and sm1 == False:
        assert "Player 1" in results[0]
    if sm0 == False and sm1 == True:
        assert "Player 2" in results[0]
    if sm0 == sm1:
        assert 25 < float(results[2].split(" ")[1].replace("%", "")) < 80


if __name__ == "__main__":
    pytest.main()
