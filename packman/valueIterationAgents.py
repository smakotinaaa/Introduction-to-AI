# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.best_action_dict = dict()
        states = mdp.getStates()
        for iteration in range(self.iterations):
            prev_vals = self.values.copy()
            for state in states:
                action_values = util.Counter()
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    state_prob_list = self.mdp.getTransitionStatesAndProbs(state, action)
                    for next_state, prob in state_prob_list:
                        action_values[action] += self.discount * prob * prev_vals[next_state] + \
                                                 self.mdp.getReward(state, action, next_state) * prob
                best_action = action_values.argMax()
                self.best_action_dict[state] = best_action
                self.values[state] = action_values[best_action]

    def getValue(self, state):
        """
      Return the value of the state (computed in __init__).
    """
        return self.values[state]

    def getQValue(self, state, action):
        """
        The q-value of the state action pair
        (after the indicated number of value iteration
        passes).  Note that value iteration does not
        necessarily create this quantity and you may have
        to derive it on the fly.
        """
        q_val = 0
        state_prob_list = self.mdp.getTransitionStatesAndProbs(state,
                                                               action)
        for next_state, prob in state_prob_list:
            q_val += self.mdp.getReward(state, action, next_state) * prob + \
                     self.discount * prob * self.values[next_state]
        return q_val

    def getPolicy(self, state):
        """
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None
        return self.best_action_dict[state]

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
