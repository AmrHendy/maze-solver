class StateMap:
    __instance = None

    @staticmethod
    def get_instance():
        if StateMap.__instance is None:
            StateMap()
        return StateMap.__instance

    def __init__(self):
        if StateMap.__instance is None:
            StateMap.__instance = self
            self.__states = {}
        else:
            raise Exception("This Class is Singleton.")

    def add_state(self, row, col, state):
        self.__states[(row, col)] = state
