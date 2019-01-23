from random import shuffle
from Model.state import State
import numpy as np


class Maze:

    def __init__(self, maze_rows, maze_cols):
        self.__maze_rows = maze_rows
        self.__maze_cols = maze_cols
        self.__maze = self.generate_random_grid()
        self.__states = {}
        for i in range(0, maze_rows):
            for j in range(0, maze_cols):
                self.__states[(i, j)] = State(i, j, self.__maze, 0)

        self.__agent_index = (0, 0)

    def generate_random_grid(self):
        """
            start cell is (1,1)
            end cell is (N,N)
            cells with value = one means barrier cells
            cells with value = zero means empty cells
        """
        barrier_count = self.__maze_rows * self.__maze_cols * 0.2
        grid = [1] * barrier_count + [0] * (self.__maze_rows * self.__maze_cols - barrier_count)
        shuffle(grid)
        # mark the start and the end
        grid[0] = 0
        grid[-1] = 0
        grid = np.reshape(grid, (self.__maze_rows, self.__maze_cols))
        return grid

    def get_state(self, row, col):
        return self.__states[(row, col)]

    def get_all_states(self):
        return self.__states

    def get_shape(self):
        return self.__maze_rows, self.__maze_cols

    def get_maze_grid(self):
        return self.__maze

    def move_agent(self, row, col):
        self.__agent_index = (row, col)