import pytest
import numpy as np
from qLearningAgent import QLearningAgent


@pytest.mark.xfail
def test_choose_action():
    agent = QLearningAgent(
        rows=6, cols=7, epsilon=0.1, alpha=0.5, gamma=0.9, smart=True
    )

    # Test when self.smart is True
    state_smart = (np.zeros((6, 7)), 1)
    action_smart = agent.choose_action(state_smart)
    assert action_smart in range(agent.cols)

    # Test when self.smart is False
    agent.smart = False
    state_not_smart = (np.zeros((6, 7)), 1)
    action_not_smart = agent.choose_action(state_not_smart)
    assert action_not_smart in range(agent.cols)


@pytest.mark.xfail
def test_update_q_value():
    agent = QLearningAgent(
        rows=6, cols=7, epsilon=0.1, alpha=0.5, gamma=0.9, smart=True
    )

    # Test the update_q_value method
    state = (np.zeros((6, 7)), 1)
    action = 2
    reward = 1
    next_state = (np.ones((6, 7)), 2)

    initial_q_value = agent.q_table[state[0], action, state[1]]
    agent.update_q_value(state, action, reward, next_state)
    updated_q_value = agent.q_table[state[0], action, state[1]]

    assert updated_q_value != initial_q_value
    assert isinstance(updated_q_value, np.float64)


if __name__ == "__main__":
    pytest.main()
