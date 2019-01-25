from Model.maze import Maze
from Control.algorithm_factory import AlgorithmFactory
from Control.algorithms.algorithm import AlgorithmType


rows = cols = 10

maze = Maze(rows, cols)

factory = AlgorithmFactory.get_instance()

value_algorithm = factory.produce_algorithm(AlgorithmType.ValueIteration)

value_algorithm.run_algorithm()

p = value_algorithm.get_current_policy()

print(p)