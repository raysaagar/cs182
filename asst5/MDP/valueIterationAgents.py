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
  def __init__(self, mdp, discount = 0.9, iterations = 100):
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
    "*** YOUR CODE HERE ***"
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # value of each state; a Counter is a dict with default 0
    
    # run for desired number of iterations
    for i in xrange(iterations):
      new_values = self.values.copy()
      for s in mdp.getStates():
        if not mdp.isTerminal(s):
          # the commented code works as well
          #curr_best = float("-inf")
          #for a in mdp.getPossibleActions(s):
          #temp_value = sum([p * (mdp.getReward(s, a, s2) + discount*prev[s2]) for s2, p in mdp.getTransitionStatesAndProbs(s, a)])
          #  if temp_value > curr_best:
          #    curr_best = temp_value
          #self.values[s] = curr_best       
          new_values[s] = max([self.getQValue(s, a) for a in mdp.getPossibleActions(s)])  
      self.values = new_values

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    "*** YOUR CODE HERE ***"
    return self.values[state]

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    return sum([p * (self.mdp.getReward(state, action, s2) + self.discount*self.getValue(s2)) 
      for s2, p in self.mdp.getTransitionStatesAndProbs(state, action)])

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    if self.mdp.isTerminal(state):
      return None
    possible_actions = self.mdp.getPossibleActions(state)
    best_action = None
    curr_best = float("-inf")
    for a in possible_actions:
      temp_value = self.getQValue(state, a)
      # or equal sign here, doesn't matter (tie)
      if temp_value >= curr_best:
        curr_best = temp_value
        best_action = a
    return best_action

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
