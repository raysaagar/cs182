import util
from collections import deque
from GraphPlan import GraphPlan
from Parser import Parser
from PlanGraph import PlanGraph
from Pair import Pair
from Action import Action

class DWRProblem:
  def __init__(self, domain, problem):
    p = Parser(domain, problem)
    domainKB = p.parseActionsAndPropositions()
    self.actions = domainKB[0]
    self.propositions = domainKB[1]
    prob = p.pasreProblem()
    self.initialState = prob[0]
    self.goal = prob[1]

  def getStartState(self):
    return self.initialState

  def isGoalState(self, state):
    return all([s in state for s in self.goal])

  # returns list of tuples of (state, action)
  def getSuccessors(self, state):
    successors = []

    for action in [a for a in self.actions if all(preCond in state for preCond in a.getPre())]:
      # add all the adds to list of propositions in state, remove 'deletes' from the list of propositions in state
      # this applies an action onto state
      newState = state + [prep for prep in action.getAdd() if prep not in state]
      newState = [prep for prep in newState if prep not in action.getDelete()]
      successors.append((newState, action, 0))
    return successors

  def getCostOfActions(self, movelist):
    return len(movelist)

def graphPlanHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def parameterizedSearch(problem, FrontierDataStructure, priorityFunction=None, heuristic=None):
  """
  Parameterized, generalized search problem

  Args:
      problem: The SearchProblem object
      frontierDataStructure: the data structure to use, i.e. queue, stack, priority queue
      heuristic: a heuristic function
      
  Returns:
      The path to the goal state that was found by the search
  """
  if heuristic:
    # x[0] is the current node. x[2] is the cost it took to get to the node
    priorityFunction = lambda x: heuristic(x[0], problem) + x[2]

  if priorityFunction:
    frontier = FrontierDataStructure(priorityFunction)
  else:
    frontier = FrontierDataStructure()

  visited = []
  node = problem.getStartState()
  frontier.push((node, None, 0, []))
  visited.append(node)

  while not frontier.isEmpty():
    # represent each step of search as a four-tuple
    # actionHistory is a list of all actions up to but not including
    # the current node
    node, action, currentCost, actionHistory = frontier.pop()
    if problem.isGoalState(node):
      return actionHistory + [action]

    for (successor, nextAction, stepCost) in problem.getSuccessors(node):
      if successor not in visited: ## CHANGE THIS LATER (propositions could be in different order)
        visited.append(successor)
        frontier.push((successor, nextAction, currentCost + stepCost, 
          actionHistory + [action] if action else []))

def aStarSearch(problem, heuristic=graphPlanHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  return parameterizedSearch(problem, util.PriorityQueueWithFunction, None, heuristic)

if __name__ == '__main__':
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  #gp = GraphPlan(domain, problem)
  problem = DWRProblem(domain, problem)
  plan = aStarSearch(problem, heuristic=graphPlanHeuristic)
  for action in plan:
    print action