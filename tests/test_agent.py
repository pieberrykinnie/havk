from backend.ml import QLearningAgent


def test_q_learning_converges():
    # Dummy env: state is always "s", reward +1 for action 1 else -1.
    actions = [0, 1]
    agent = QLearningAgent(actions, lr=0.5, gamma=0.0, epsilon=0.1)

    state = "s"
    for _ in range(200):
        action = agent.select_action(state)
        reward = 1 if action == 1 else -1
        agent.update(state, action, reward, state)

    # After learning, greedy policy should choose action 1
    assert agent.policy(state) == 1