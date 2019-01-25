from model.maze import Maze
from control.algorithm_factory import AlgorithmFactory
from control.algorithms.algorithm import AlgorithmType


class Agent:
    def __init__(self, maze_rows, maze_cols):
        self.__agent_index = (0, 0)
        self.__maze_rows = maze_rows
        self.__maze_cols = maze_cols
        self.__maze = Maze(maze_rows, maze_cols)
        self.__agent_policy = None
        self.__state_values = self.get_mdp_solver(AlgorithmType.PolicyIteration).get_state_values()
        self.__policy_map = self.get_mdp_solver(AlgorithmType.PolicyIteration).get_current_policy().get_actions_map()

    def solve_maze(self, algorithm_type):
        mdp_algorithm = self.get_mdp_solver(algorithm_type)
        mdp_algorithm.run_algorithm()
        self.__agent_policy = mdp_algorithm.get_current_policy()
        self.__state_values = mdp_algorithm.get_state_values()
        self.__policy_map = self.__agent_policy.get_actions_map()

    def get_mdp_solver(self, algorithm_type):
        assert algorithm_type == AlgorithmType.PolicyIteration or algorithm_type == AlgorithmType.ValueIteration
        factory = AlgorithmFactory.get_instance()
        mdp_algorithm = factory.produce_algorithm(algorithm_type)
        return mdp_algorithm

    def advance_agent(self):
        if not self.is_goal():
            new_row, new_col = self.__agent_policy.apply_policy(self.__agent_index[0], self.__agent_index[1])
            self.__agent_index = (new_row, new_col)
        return self.get_agent_index()

    def restart_same_maze(self):
        self.__agent_index = (0, 0)

    def restart_diff_maze(self):
        self.__maze = Maze(self.__maze_rows, self.__maze_cols)
        self.__agent_index = (0, 0)

    def move_agent(self, row, col):
        self.__agent_index = (row, col)

    def get_agent_index(self):
        return self.__agent_index

    def is_goal(self):
        return self.__agent_index == (self.__maze_rows - 1, self.__maze_cols - 1)

    def get_maze(self):
        return self.__maze

    def get_state_values(self):
        return self.__state_values

    def get_policy_map(self):
        return self.__policy_map
