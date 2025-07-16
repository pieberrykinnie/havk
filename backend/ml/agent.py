"""Reinforcement-Learning Agent (tabular Q-learning).

This minimal implementation allows IrrigaBot to adjust irrigation
recommendations based on binary farmer feedback (e.g. *too dry*, *too wet*).

* States: currently a string label such as "ok", "dry", "wet".  Can be expanded
  to include soil type, weather bins, etc.
* Actions: integer index representing adjustment to litres schedule.

The agent persists an in-memory Q-table; swapping to Redis or Supabase is left
as future work.
"""
from __future__ import annotations

from collections import defaultdict
from random import random, choice
from typing import Dict, Hashable, List, Tuple


class QLearningAgent:  # noqa: D101
    def __init__(
        self,
        actions: List[int],
        lr: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
    ) -> None:
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        # Q-table: state -> action -> value
        self.q: Dict[Hashable, Dict[int, float]] = defaultdict(lambda: defaultdict(float))

    # ---------------------------------------------------------------------
    # Core
    # ---------------------------------------------------------------------

    def select_action(self, state: Hashable) -> int:  # noqa: D401
        """Epsilon-greedy action selection."""
        if random() < self.epsilon:
            return choice(self.actions)
        return max(self.actions, key=lambda a: self.q[state][a])

    def update(self, state: Hashable, action: int, reward: float, next_state: Hashable) -> None:  # noqa: D401
        """Q-learning update."""
        best_next = max(self.actions, key=lambda a: self.q[next_state][a])
        td_target = reward + self.gamma * self.q[next_state][best_next]
        td_error = td_target - self.q[state][action]
        self.q[state][action] += self.lr * td_error

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def policy(self, state: Hashable) -> int:
        """Greedy policy (no exploration)."""
        return max(self.actions, key=lambda a: self.q[state][a])

    # ------------------------------------------------------------------
    # Persistence (placeholder)
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict:  # noqa: D401
        """Return serialisable snapshot of Q-table."""
        return {str(s): dict(a_map) for s, a_map in self.q.items()}

    def load(self, data: Dict[str, Dict[str, float]]) -> None:  # noqa: D401
        """Load Q-table from snapshot."""
        for s, a_map in data.items():
            for a, v in a_map.items():
                self.q[s][int(a)] = float(v)