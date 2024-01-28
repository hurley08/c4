# c4/qLearningAgent.py
"""
I've created a QLearningAgent class that uses a Q-table
to store Q-values for each state-action pair. The choose_action
method is responsible for selecting an action based on the epsilon-
greedy policy. The update_q_value method updates the Q-value based
on the reward and the difference between the current Q-value and
the estimated future Q-value.

The ConnectFourRL class inherits from the original ConnectFour
class and uses the Q-learning agent to make decisions for player
2.

The Q-learning agent learns to play the game by updating Q-values
during each move.
"""
import numpy as np
import random


class QLearningAgent:
    def __init__(
        self,
        rows=6,
        cols=8,
        epsilon=0.1,
        alpha=0.5,
        gamma=0.9,
        smart=True,
        debug=False,
        wait=0,
    ):
        self.rows = rows
        self.cols = cols
        self.q_table = np.zeros((rows, cols, 2))  # Q-values for each state-action pair
        self.epsilon = epsilon  # Exploration-exploitation trade-off
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.smart = smart
        self.print_it = debug
        self.debug = debug
        self.wait = wait

    def __str__(self):
        return f"QTable Started with {self.epsilon=} {self.alpha=} and {self.gamma=}"

    def choose_action(self, state):
        """
        if self.smart is True this method will make determination on
        best move to make based on params. Otherwise it will choose
        a space randomly.
        """
        if self.smart:
            if random.uniform(0, 1) < self.epsilon:
                if self.debug:
                    print(
                        [col for col in range(self.cols) if any(state[0][:, col] == 0)]
                    )
                return random.choice(
                    [col for col in range(self.cols) if any(state[0][:, col] == 0)]
                )
            else:
                player_index = state[
                    1
                ]  # Convert player number to index (1-based to 0-based)
                return np.argmax(self.q_table[state[0], :, player_index])
        else:
            return random.choice(
                [col for col in range(self.cols) if any(state[0][:, col] == 0)]
            )

    def update_q_value(self, state, action, reward, next_state):
        """
        Current implementation will store and update a q table regardless
        of whether self.smart is enabled
        """
        try:
            self.q_table[state[0], action, state[1]] += self.alpha * (
                reward
                + self.gamma * np.max(self.q_table[next_state[0], :, next_state[1]])
                - self.q_table[state[0], action, state[1]]
            )
            if self.debug:
                print(self.q_table)
            return True

        except Exception as e:
            if self.print_it:
                print(f"{e=}, Something failed while updating Q table")
            return False
