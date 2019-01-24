from Control.algorithms.algorithm import Algorithm
from Model.policy import Policy
import numpy as np


class ValueIteration(Algorithm):

    def run_algorithm(self):
        """
            V*(s) = max_a Q(S,A)
            Q(S,A) = sigma ( T(S,A,S') * ( R(S,A,S') + gamma * V*(S') ) )
            thus T(S,A,S') = 1, as it's deterministic
            then Q(S,A) = R(S,A,S') + gamma * V*(S')
        """
        no_states = len(self._states.get_no_states)
        states = self._states.get_states()
        actions = ['left', 'right', 'up', 'down']
        values = np.zeros((no_states,)).T
        gamma = 0.5
        policy_map = {}
        iterations = 30

        # iterate for N times.
        for k in range(iterations):
            new_values = np.zeros((no_states,)).T
            # Update for each state
            i = 0
            for ind, state in states.items():
                max_q = float('-inf')
                max_action = ''
                # for each state, see all actions
                for act in actions:
                    next_state = state.get_next_state(act)
                    q = next_state.get_reward() + gamma * values
                    if q > max_q:
                        max_q = q
                        max_action = act
                # update the value of the state
                new_values[i] = max_q
                # update the policy
                policy_map[ind] = max_action
                i += 1

        self._current_policy = Policy(policy_map)

