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

    def get_state(self, row, col):
        return self.__states[(row, col)]

    @property
    def get_states(self):
        return self.__states

    @property
    def get_num_states(self):
        num_states = len(self.__states)
        return num_states
