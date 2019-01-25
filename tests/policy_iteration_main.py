from Model.maze import Maze
from Control.algorithm_factory import AlgorithmFactory
from Control.algorithms.algorithm import AlgorithmType


rows = cols = 10

maze = Maze(rows, cols)

factory = AlgorithmFactory.get_instance()

policy_iteration_algorithm = factory.produce_algorithm(AlgorithmType.PolicyIteration)

policy_iteration_algorithm.run_algorithm()

p = policy_iteration_algorithm.get_current_policy()

print(p)