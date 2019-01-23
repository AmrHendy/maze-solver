class State:

    def __init__(self, row, col, maze_rows, maze_cols, value=0):
        self.index = (row, col)
        self.value = value
        self.next_states = {}
        actions = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
        for action_type, action_delta in zip(actions.keys(), actions.values()):
            next_index = (row + action_delta[0], col + action_delta[1])
            if next_index[0] < 0 or next_index[0] >= maze_rows or next_index[1] < 0 or next_index[1] >= maze_cols:
                next_index = self.index
            self.next_states[action_type] = next_index

    @property
    def get_next_state(self, action_type):
        assert action_type in self.next_states.keys()
        return self.next_states[action_type]

    @property
    def get_value(self):
        return self.value

    @property
    def set_value(self, value):
        self.value = value