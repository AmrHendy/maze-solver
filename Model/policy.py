class Policy:

    def __init__(self, state_actions_map):
        """
        :param state_actions_map: is dictionary where key is the state and the value is list of best possible actions
        """
        self.state_action_map = state_actions_map

    def __get_actions(self, state):
        return self.state_action_map[state]

    def __set_actions(self, state, actions):
        self.state_action_map[state] = actions
