from control.algorithms.algorithm import Algorithm
from model.policy import Policy
import numpy as np


class PolicyIteration(Algorithm):

    def __init__(self, states):
        super(PolicyIteration, self).__init__(states)
        self.__initial_policy_map = {}
        for ind, state in self._states.get_states.items():
            self.__initial_policy_map[ind] = []
            actions = ['left', 'right', 'up', 'down']
            for action in actions:
                self.__initial_policy_map[ind].append(action)

    def run_algorithm(self):
        num_states = self._states.get_num_states
        state_values = np.zeros((num_states,))
        policy_map = self.__initial_policy_map
        iterations = 100

        for k in range(iterations):
            # policy evaluation
            policy_state_values = self.evaluate_policy(state_values, policy_map)
            state_values = policy_state_values
            # greedy policy improvement
            new_policy_map, changed = self.improve_policy(policy_state_values, policy_map)
            policy_map = new_policy_map
            # check convergence to the optimal policy
            if not changed:
                break

        self._current_policy = Policy(policy_map)

    def evaluate_policy(self, state_values, policy_map):
        """
            Vk+1(s) = sigma over actions a ( π(a | s) * ( R(S,a) + gamma * sigma ( T(S,a,S') * Vk(S') ) )
            since T(S,A,S') = 1, as it's deterministic
            since π(a | s) = 1/4 at frst only, then it will be 1 as it will be deterministic policy
            thus Vk+1(s) = sigma over actions a ( 1/(#actions in the policy map) * ( R(S,a) + gamma * Vk(S') ) )
        """
        gamma = 0.7
        iterations = 100
        convergence_error = 0.001

        for k in range(iterations):
            new_values = np.zeros((self._states.get_num_states,))
            max_delta = 0
            for ind, state in self._states.get_states.items():
                # for each state, see all actions
                all_actions = policy_map[ind]
                state_value = 0
                for action in all_actions:
                    next_state_ind = state.get_next_state(action)
                    next_state = self._states.get_states[next_state_ind]
                    state_value += state.get_reward + gamma * state_values[next_state.get_single_index]
                state_value *= (1.0 / len(all_actions))

                # update the value of the state
                new_values[state.get_single_index] = state_value
                max_delta = max(max_delta, abs(new_values[state.get_single_index] - state_values[state.get_single_index]))
            state_values = new_values
            if max_delta < convergence_error:
                break

        return new_values

    def improve_policy(self, policy_state_values, policy_map):
        """
            π'(s) = max arg over actions a( R(s,a) + gamma * sigma ( T(s,a,s') * Vπ(s') )
            since T(s,a,s') = 1, as it's deterministic
            then π'(s) = max arg over actions a( R(s,a) + gamma * Vπ(s') )
        """
        gamma = 0.7
        changed = False
        new_policy_map = {}
        for ind, state in self._states.get_states.items():
            actions = ['left', 'right', 'up', 'down']
            max_q = float('-inf')
            max_action = ''
            for action in actions:
                next_state_ind = state.get_next_state(action)
                next_state = self._states.get_states[next_state_ind]
                q = next_state.get_reward + gamma * policy_state_values[next_state.get_single_index]
                if q > max_q:
                    max_action = action

            new_policy_map[ind] = [max_action]
            if policy_map[ind] != new_policy_map[ind]:
                changed = True

        return new_policy_map, changed
