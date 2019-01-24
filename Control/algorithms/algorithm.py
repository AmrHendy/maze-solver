from enum import Enum
from abc import ABC, abstractmethod


class AlgorithmType(Enum):
    PolicyIteration = 1
    ValueIteration = 2


class Algorithm(ABC):

    def __init__(self, states):
        self._states = states
        self._current_policy = None
        super().__init__()

    @abstractmethod
    def run_algorithm(self):
        pass

    def get_current_policy(self):
        return self._current_policy
