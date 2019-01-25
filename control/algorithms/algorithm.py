from abc import ABC
from abc import abstractmethod
from enum import Enum
from model.policy import Policy
import numpy as np


class AlgorithmType(Enum):
    PolicyIteration = 1
    ValueIteration = 2


class Algorithm(ABC):

    def __init__(self, states):
        self._states = states
        initial_policy_map = {}
        for ind, state in self._states.get_states.items():
            initial_policy_map[ind] = []
            actions = ['left', 'right', 'up', 'down']
            for action in actions:
                initial_policy_map[ind].append(action)
        self._state_values = np.zeros((self._states.get_num_states,))
        self._current_policy = Policy(initial_policy_map)
        super().__init__()

    @abstractmethod
    def run_algorithm(self):
        pass

    def get_current_policy(self):
        return self._current_policy

    def get_state_values(self):
        return self._state_values
