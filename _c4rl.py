import numpy as np
import random
import time
from qLearningAgent import QLearningAgent
from _c4 import ConnectFour


class ConnectFourRL(ConnectFour):
    def __init__(self, rows=6, cols=7, p1_smart=False, p2_smart=True, print_it=True):
        super().__init__(rows, cols)
        self.agent1 = QLearningAgent(rows=rows, cols=cols, smart=p1_smart)
        self.agent2 = QLearningAgent(rows=rows, cols=cols, smart=p2_smart)
        self.move = 1
        self.winner = False
        self.print_it = print_it

    def get_state(self):
        return (self.board.copy(), self.current_player - 1)

    def play_game(self):
        while not self.check_winner() and not self.is_full():
            print("Playing" + "." * (self.move // 10), end="\r", flush=True)

            while True:

                if self.current_player == 1:
                    # col = int(input(f"Player {self.current_player}, choose a column (1-{self.cols}): ")) - 1
                    col = self.agent1.choose_action(self.get_state())
                else:
                    col = self.agent2.choose_action(self.get_state())

                if 0 <= col < self.cols and self.drop_piece(col):
                    time.sleep(0.75)
                    self.move += 1
                    if self.print_it:
                        print("\n\n\n\n")
                        self.print_board()
                        # , end="", flush=True)
                    next_state = self.get_state()
                    reward = (3, -1) if self.check_winner() else (1, 0)
                    if self.current_player == 1:
                        self.agent1.update_q_value(
                            self.get_state(), col, reward[0], next_state
                        )
                        self.agent2.update_q_value(
                            self.get_state(), col, reward[1], next_state
                        )

                    if self.check_winner():
                        if self.print_it:
                            self.print_board()
                        self.winner = self.current_player
                        if self.print_it:
                            print(
                                f"Player {self.current_player} won in {self.move} moves",
                                flush=True,
                                end="\r",
                            )
                        break
                    elif self.is_full():
                        self.print_board()
                        print("It's a tie!")
                        break
                    self.switch_player()
                    break
                else:
                    if self.print_it:
                        print("Invalid move. Try again.\n", flush=True, end="")
                    break
        return self.current_player, self.move


def get_trend(game_log=None):
    if game_log:
        p_1_wins = {}
        p_2_wins = {}
        for index, data in enumerate(game_log):
            if index > 0:
                if isinstance(game_log[index], tuple):
                    data = game_log[index]

                    if data[0] == 1:
                        p_1_wins[index] = game_log[index][1]
                    else:
                        p_2_wins[index] = game_log[index][1]

        print(
            f"p1 wins: {len(p_1_wins)}, average moves to win: {(sum(p_1_wins.values())/len(p_1_wins)):.3f}"
        )
        print(
            f"p2 wins: {len(p_2_wins)}, average moves to win: {(sum(p_2_wins.values())/len(p_2_wins)):.3f}"
        )
        better = "p1" if len(p_1_wins) > len(p_2_wins) else "p2"
        print(
            f"{better} win % at {max(len(p_1_wins), len(p_2_wins))/len(game_log)*100:.3f}%  "
        )


def plot_progression():
    """
    It'd be interesting to see how moves-to-win tracked
    through the series of games.
    """
    pass


if __name__ == "__main__":
    start = time.time()
    n = int(input("how many iterations?: "))
    smarts = [(True, False), (False, False), (False, True), (True, True)]
    game_log = {}
    for sm in smarts:
        for i in range(n + 1)[1:]:
            game = ConnectFourRL(rows=6, cols=8, p1_smart=sm[0], p2_smart=sm[1])
            game_log[i] = game.play_game()
        if game.print_it:
            print(game_log)
        print("\n\n", sm)
        get_trend(game_log)
    end = time.time()
    print(
        f"\nTook {end-start:.3f} seconds to execute {n} games * {len(smarts)} variants ({n*len(smarts)})"
    )
