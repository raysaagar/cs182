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
    return len(state) == len(self.goal) and all([s in self.goal for s in state])

  # returns list of tuples of (state, action)
  def getSuccessors(self, state):
    successors = []
    for action in [a for a in self.actions if all(preCond in state for preCond in a.getPre())]:
      # add all the adds to list of propositions in state, remove 'deletes' from the list of propositions in state
      # this applies an action onto state
      newState = state + action.getAdd()
      #print "BEFORE: ", len(newState)
      newState = [prep for prep in newState if prep not in action.getDelete()]
      #print "AFTER: ", len(newState)
      successors.append((newState, action))
    return successors

  def getCostOfActions(self, movelist):
    #print movelist
    return len(movelist)

def graphPlanHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=graphPlanHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  # use priority queue to have costs
  fringe = util.PriorityQueue()
  fringe.push((problem.getStartState(), []), 0)
  explored = []

  while not fringe.isEmpty():
    # get the next location
    #location, moves = fringe.pop()
    state, actions = fringe.pop()

    # if we find the goal state, then we should be done.
    # all other items in the p_queue will have worse cost
    if problem.isGoalState(state):
      return actions

    #for coordinates, direction in problem.getSuccessors(location):
    for propositions, action in problem.getSuccessors(state):
      if not propositions in explored:
        actionlist = actions + [action]
        print len(actionlist)
        new_cost = problem.getCostOfActions(actionlist) + heuristic(propositions, problem)
        # push explored to fringe. also append or a* will fail
        explored.append(propositions)
        fringe.push((propositions, actionlist), new_cost)

  return []


if __name__ == '__main__':
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  #gp = GraphPlan(domain, problem)
  problem = DWRProblem(domain, problem)
  print aStarSearch(problem, heuristic=graphPlanHeuristic)