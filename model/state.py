from model.states_map import StateMap
from enum import Enum


class CellType(Enum):
    end = 1
    empty = 2
    block = 3


class State:

    def __init__(self, row, col, grid, cell_type):
        self.__index = (row, col)
        self.__cell_type = cell_type
        # generate the next states
        actions = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
        # map from action to the next state = (next state row, next state col)
        self.__next_states = {}
        self.__reward = -1
        for action_type, action_delta in zip(actions.keys(), actions.values()):
            next_index = (row + action_delta[0], col + action_delta[1])
            if next_index[0] < 0 or next_index[0] >= grid.shape[0] \
                    or next_index[1] < 0 or next_index[1] >= grid.shape[1]\
                    or grid[next_index[0]][next_index[1]] == 1 or grid[row][col] == 1:
                next_index = self.__index
            self.__next_states[action_type] = next_index
        if row == grid.shape[0] - 1 and col == grid.shape[1] - 1:
            self.__reward = 20
        self.__single_index = row * grid.shape[1] + col

    def get_next_state(self, action_type):
        assert self.has_action(action_type)
        return self.__next_states[action_type]

    def has_action(self, action_type):
        return action_type in self.__next_states.keys()

    def get_reward(self, action):
        next_state_ind = self.get_next_state(action)
        next_state = StateMap.get_instance().get_states[next_state_ind]
        return next_state.get_state_reward()

    def get_state_reward(self):
        if self.__cell_type == CellType.empty:
            return -1
        elif self.__cell_type == CellType.block:
            return -1
        elif self.__cell_type == CellType.end:
            return 0

    @property
    def get_index(self):
        return self.__index

    @property
    def get_single_index(self):
        return self.__single_index
