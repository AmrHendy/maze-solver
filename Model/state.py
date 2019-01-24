class State:

    def __init__(self, row, col, grid, value=0):
        self.__index = (row, col)
        self.__value = value
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
            self.__reward = 100

    def get_next_state(self, action_type):
        assert action_type in self.__next_states.keys()
        return self.__next_states[action_type]

    @property
    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
