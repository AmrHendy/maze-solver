from control.algorithms.algorithm import AlgorithmType
from control.algorithms.policy_iteration import PolicyIteration
from control.algorithms.value_iteration import ValueIteration
from model.states_map import StateMap


class AlgorithmFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if AlgorithmFactory.__instance is None:
            AlgorithmFactory()
        return AlgorithmFactory.__instance

    def __init__(self):
        if AlgorithmFactory.__instance is None:
            AlgorithmFactory.__instance = self
        else:
            raise Exception("This Class is Singleton.")

    def produce_algorithm(self, algorithm_type):
        states = StateMap.get_instance()
        if algorithm_type == AlgorithmType.PolicyIteration:
            return PolicyIteration(states)
        elif algorithm_type == AlgorithmType.ValueIteration:
            return ValueIteration(states)
        else:
            raise Exception("This Algorithm is not implemented yet.")
