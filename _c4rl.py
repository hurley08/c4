import numpy as np
import random
import time

from qLearningAgent import QLearningAgent
from _c4 import ConnectFour
from display import LED_Matrix


class ConnectFourRL(ConnectFour):
    def __init__(
        self,
        rows=None,
        cols=None,
        p1_smart=None,
        p2_smart=None,
        print_it=False,
        print_game=False,
        test=False,
        debug=False,
        display=False,
        wait=4,
        COM=None,
        BAUD=None,
    ):
        super().__init__(rows, cols, test)
        self.COM = COM
        self.p1_smart = p1_smart
        self.p2_smart = p2_smart
        self.debug = debug
        self.agent1 = QLearningAgent(
            rows=self.rows, cols=self.cols, smart=self.p1_smart, debug=self.debug
        )
        self.agent2 = QLearningAgent(
            rows=self.rows, cols=self.cols, smart=self.p2_smart, debug=self.debug
        )
        self.print_it = print_it
        self.print_game = print_game
        self.wait = wait
        self.move = 1
        self.winner = False
        self.COM = COM
        self.BAUD = BAUD
        self.display = display
        if self.display:
            self.matrix = LED_Matrix(
                port=self.COM, baudrate=9600, rows=self.rows, cols=self.cols
            )
            self.display = True

        # print(f"{self.rows=} {self.cols=} {self.p1_smart=} {self.p2_smart=} {self.wait=}")

    #    #    self.move = 1
    #    self.winner = False

    #    print(type(self.agent1))
    #   print(type(self.agent2))

    def get_state(self):
        # Retrieves state of the board
        return (self.board.copy(), self.current_player - 1)

    def update_q(self, p1_adj=None, p2_adj=None, col=None):
        # Updates Q tables of either or both players
        next_state = self.get_state
        if self.print_it:
            print(
                f"Attempting to update p1 q-table: {p1_adj} and p2 q-table: {p2_adj} "
            )
            print(f"{next_state=}, {col=}")

        if p1_adj:
            p1_adj = self.agent1.update_q_value(
                self.get_state(), col, p1_adj, next_state
            )
        if p2_adj:
            p2_adj = self.agent2.update_q_value(
                self.get_state(), col, p2_adj, next_state
            )
        return p1_adj, p2_adj

    def play_game(self):
        # Commences the game
        while not self.check_winner() and not self.is_full():
            print("Playing" + "." * (self.move // 10), end="\r", flush=True)

            while True:
                if self.current_player == 1:
                    # col = int(input(f"Player {self.current_player}, choose a column (1-{self.cols}): ")) - 1
                    col = self.agent1.choose_action(self.get_state())
                else:
                    col = self.agent2.choose_action(self.get_state())
                # print(f"Debug 33, {self.move=}, {col=},{self.current_player=}")
                if (0 <= col < self.cols) and self.drop_piece(col):
                    if self.display:
                        bit_board = self.matrix.to_bitmap(self.board)
                        self.matrix.output_to_serial(self.rows, self.cols, bit_board)
                        time.sleep(self.wait + 0.5)
                    self.move += 1
                    if self.print_game:
                        print("\n\n\n\n")
                        self.print_board()
                        # , end="", flush=True)

                    reward, penalty = (3, -1) if self.check_winner() else (1, None)
                    if self.current_player == 1:
                        p1, p2 = self.update_q(reward, penalty)
                    if self.current_player == 2:
                        p1, p2 = self.update_q(penalty, reward)
                    if self.print_it:
                        print(f"p1q: {p1} p2q: {p2}")

                    if self.check_winner():
                        if self.print_game:
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
                        if self.print_game:
                            self.print_board()
                            print("It's a tie!")
                        break
                    self.switch_player()
                    break
                else:
                    if self.print_it:
                        print("Invalid move. Try again.\n", flush=True, end="")
                        reward = None
                        penalty = -0.5
                        if self.current_player == 1:
                            self.update_q(penalty, reward, col)
                        if self.current_player == 2:
                            self.update_q(reward, penalty, col)
                    break
        return self.current_player, self.move


def split_wins(game_log=None):
    # Reporting function to to bin wins to each player
    p_1_wins = {}
    p_2_wins = {}
    if game_log:
        for index, data in enumerate(game_log):
            if index > 0:
                if isinstance(game_log[index], tuple):
                    data = game_log[index]

                    if data[0] == 1:
                        p_1_wins[index] = game_log[index][1]
                    else:
                        p_2_wins[index] = game_log[index][1]
    return p_1_wins, p_2_wins


def return_stats(
    num1,
    num2,
    mean_moves_1,
    mean_moves_2,
    win_margin,
    p1_moves_min_max,
    p2_moves_min_max,
):
    # Reporting function that prints win stats to terminal
    players = {num1: "Player 1", num2: "Player 2"}
    min_max = (p1_moves_min_max, p2_moves_min_max)
    tup = num1, num2
    winner_min_max = min_max[tup.index(max(tup))]
    return (
        f"winner: {players[max(tup)]}",
        f"avg moves to win: {max(mean_moves_1, mean_moves_2)}",
        f"margin: {win_margin}",
        f"moves max/min: {winner_min_max}",
    )


def compare_wins(p1_wins, p2_wins):
    # Reporting function that calculates individual values
    num_p1_wins = len(p1_wins)
    num_p2_wins = len(p2_wins)
    num_tup = (num_p1_wins, num_p2_wins)
    if len(p1_wins) > 0:
        p1_moves_min_max = (max(p1_wins.values()), min(p1_wins.values()))
    else:
        p1_moves_min_max = (0, 0)
    if len(p2_wins) > 0:
        p2_moves_min_max = (max(p2_wins.values()), min(p2_wins.values()))
    else:
        p2_moves_min_max = (0, 0)
    mean_p1_moves_win = sum(p1_wins.values()) // num_p1_wins if num_p1_wins > 0 else 0
    mean_p2_moves_win = sum(p2_wins.values()) // num_p2_wins if num_p2_wins > 0 else 0
    winner_margin = f"{max(num_tup)/sum(num_tup)*100:.2f}%" if sum(num_tup) > 0 else 0
    return return_stats(
        num_p1_wins,
        num_p2_wins,
        mean_p1_moves_win,
        mean_p2_moves_win,
        winner_margin,
        p1_moves_min_max,
        p2_moves_min_max,
    )
    if len(p1_wins) > 0:
        p1_moves_min_max = (max(p1_wins.values()), min(p1_wins.values()))
    else:
        p1_moves_min_max = (0, 0)
    if len(p2_wins) > 0:
        p2_moves_min_max = (max(p2_wins.values()), min(p2_wins.values()))
    else:
        p2_moves_min_max = (0, 0)
    mean_p1_moves_win = sum(p1_wins.values()) // num_p1_wins if num_p1_wins > 0 else 0
    mean_p2_moves_win = sum(p2_wins.values()) // num_p2_wins if num_p2_wins > 0 else 0
    winner_margin = f"{max(num_tup)/sum(num_tup)*100:.2f}%" if sum(num_tup) > 0 else 0
    return return_stats(
        num_p1_wins,
        num_p2_wins,
        mean_p1_moves_win,
        mean_p2_moves_win,
        winner_margin,
        p1_moves_min_max,
        p2_moves_min_max,
    )


"""
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
"""


def plot_progression():
    """
    It'd be interesting to see how moves-to-win tracked
    through the series of games.
    """
    pass


if __name__ == "__main__":
    start = time.time()
    n = int(input("how many iterations?: "))
    smarts = [(True, False), (False, True), (False, False), (True, True)]
    game_log = {}
    for sm in smarts:
        for i in range(n + 1)[1:]:
            game = ConnectFourRL(
                rows=8,
                cols=12,
                COM="/dev/ttyACM0",
                BAUD=9600,
                display=False,
                p1_smart=sm[0],
                p2_smart=sm[1],
                test=False,
                print_it=False,
                print_game=False,
                wait=4,
            )

            # game = ConnectFourRL(
            #    rows=6, cols=8, p1_smart=sm[0], p2_smart=sm[1], test=False, print_it=False
            # )
            game_log[i] = game.play_game()
        if game.print_it:
            print(game_log)
            print("\n\n", sm)
        split = split_wins(game_log)
        print(f"p1_smart: {sm[0]} p2_smart: {sm[1]} {compare_wins(split[0],split[1])}")
    end = time.time()
    print(
        f"\nTook {end-start:.3f} seconds to execute {n} games * {len(smarts)} variants ({n*len(smarts)} games)\n"
    )
