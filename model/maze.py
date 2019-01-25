from random import shuffle
from model.state import State
from model.states_map import StateMap
import numpy as np


class Maze:

    def __init__(self, maze_rows, maze_cols):
        self.__maze_rows = maze_rows
        self.__maze_cols = maze_cols
        self.__maze = self.generate_random_grid()
        self.__states = StateMap.get_instance()
        for i in range(0, maze_rows):
            for j in range(0, maze_cols):
                s = State(i, j, self.__maze, 0)
                self.__states.add_state(i, j, s)

    def generate_random_grid(self):
        """
            start cell is (1,1)
            end cell is (N,N)
            cells with value = one means barrier cells
            cells with value = zero means empty cells
        """
        valid_grid = False
        while not valid_grid:
            print('Generating Random Grid')
            blocks_ratio = 0.2
            barrier_count = int(self.__maze_rows * self.__maze_cols * blocks_ratio)
            grid = [1] * barrier_count + [0] * (self.__maze_rows * self.__maze_cols - barrier_count)
            shuffle(grid)
            # mark the start and the end
            grid[0] = 0
            grid[-1] = 0
            grid = np.reshape(grid, (self.__maze_rows, self.__maze_cols))
            valid_grid = self.__is_valid(grid)
        return grid

    def get_state(self, row, col):
        return self.__states[(row, col)]

    def get_all_states(self):
        return self.__states

    def get_shape(self):
        return self.__maze_rows, self.__maze_cols

    def get_maze_grid(self):
        return self.__maze

    def get_grid_value(self, row, col):
        return self.__maze[row][col]

    def __is_valid(self, grid):
        vis = np.zeros(shape=grid.shape, dtype='int')
        q = list()
        q.append((0, 0))
        while len(q) != 0:
            row, col = q.pop(0)
            if vis[row, col] == 1:
                continue
            vis[row, col] = 1
            # check we reach the end cell
            if row == self.__maze_rows - 1 and col == self.__maze_cols - 1:
                return True
            # expand to children
            dx = [-1, 1, 0, 0]
            dy = [0, 0, -1 , 1]
            for i in range(4):
                new_row, new_col = row + dx[i], col + dy[i]
                if self.__is_valid_index(new_row, new_col) and vis[new_row, new_col] == 0 and grid[new_row, new_col] == 0:
                    q.append((new_row, new_col))
        return False

    def __is_valid_index(self, row, col):
        if row < 0 or row >= self.__maze_rows or col < 0 or col >= self.__maze_cols:
            return False
        return True
