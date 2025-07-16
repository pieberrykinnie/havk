# Reinforcement Learning – Schedule Optimisation

The **QLearningAgent** in `backend/ml/agent.py` fine-tunes irrigation advice based on farmer feedback.

* **States**: qualitative feedback bucket – `dry`, `ok`, `wet` (prototype uses a single default).
* **Actions**: discrete adjustment factors `[-10 %, 0 %, +10 %]` (encoded as `-1, 0, +1`).
* **Algorithm**: tabular Q-learning with ε-greedy exploration.
* **Update trigger**: when a farmer messages `done` along with optional rating.

Future improvements: replace with Deep Q-Network using temporal weather features.