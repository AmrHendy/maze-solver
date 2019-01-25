from control.algorithms.algorithm import Algorithm
from model.policy import Policy
import numpy as np


class ValueIteration(Algorithm):

    def run_algorithm(self):
        """
            V*(s) = max_A Q(S,A)
            Q(S,A) = R(S,A) + gamma * sigma ( T(S,A,S') * V*(S') )
            since T(S,A,S') = 1, as it's deterministic
            thus Q(S,A) = R(S,A) + gamma * V*(S')
        """
        num_states = self._states.get_num_states
        states = self._states.get_states
        values = np.zeros((num_states,))
        policy_map = {}
        iterations = 100
        convergence_error = 0.001

        # iterate for N times.
        for k in range(iterations):
            new_values = np.zeros((num_states,))
            max_delta = 0

            # Update for each state
            for ind, state in states.items():

                # for each state, see all actions
                max_q, max_action = self._get_max_q(state, states, values)

                # update the value of the state
                new_values[state.get_single_index] = max_q
                # state.set_value(max_q)
                max_delta = max(max_delta, abs(new_values[state.get_single_index] - values[state.get_single_index]))

                # update the policy
                policy_map[ind] = [max_action]

            values = new_values
            if max_delta < convergence_error:
                break

        self._current_policy = Policy(policy_map)

    def _get_max_q(self, curr_state, states, values):
        gamma = 0.7
        actions = ['left', 'right', 'up', 'down']
        max_q = float('-inf')
        max_action = ''
        for act in actions:
            next_state_ind = curr_state.get_next_state(act)
            next_state = states[next_state_ind]
            q = next_state.get_reward(act) + gamma * values[next_state.get_single_index]
            if q > max_q:
                max_q = q
                max_action = act
        return max_q, max_action
