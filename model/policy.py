from Model.states_map import StateMap


class Policy:

    def __init__(self, state_actions_map):
        """
        :param state_actions_map: is dictionary where key is the state and the value is list of best possible actions
        """
        self.__state_action_map = state_actions_map

    def __get_actions(self, state):
        return self.__state_action_map[state]

    def __set_actions(self, state, actions):
        self.__state_action_map[state] = actions

    def apply_policy(self, row, col):
        current_state = StateMap.get_instance().get_state(row, col)
        action_type = self.__state_action_map[(row, col)][0]
        return current_state.get_next_state(action_type)

    def __str__(self):
        return str(self.__state_action_map)
