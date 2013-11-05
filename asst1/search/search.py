# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).

Code written by: Saagar Deshpande
"""

import util
from game import Directions

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  # from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


def genericSearch(problem, fringe):
  # start state
  fringe.push((problem.getStartState(), [], []))
  while not fringe.isEmpty():
    # pop the last location off fringe
    location, moves, visited = fringe.pop()
    # get successors and look at each one
    for coordinates, direction, cost in problem.getSuccessors(location):
      # if we haven't visited this location before
      if not coordinates in visited:
        # add the move to the list
        movelist = moves + [direction]
        if problem.isGoalState(coordinates):
          return movelist
        # add the visited location and continue
        visited.append(coordinates)
        fringe.push((coordinates, movelist, visited))
  # generic empty return if we get here.
  return []

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  # fringe should contain (coordinate, directions to coordinate, visited)
  # stack is for DFS
  return genericSearch(problem, util.Stack())


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"

  # fringe should contain (coordinate, directions to coordinate, visited)
  # use queue for BFS
  return genericSearch(problem, util.Queue())

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  fringe = util.PriorityQueue()
  # start state (coordinates, moves)
  fringe.push((problem.getStartState(), []), 0)

  explored = []

  while not fringe.isEmpty():
    # pop the last location off queue
    location, moves = fringe.pop()

    # if we find the goal state, then we should be done.
    # all other items in the p_queue will have worse cost
    if problem.isGoalState(location):
      return moves

    for coordinates, direction, cost in problem.getSuccessors(location):
      # if we haven't visited this location before
      if not coordinates in explored:
        # add the move to the list
        movelist = moves + [direction]
        # push location with cost, also append here or UCS will fail
        explored.append(coordinates)
        fringe.push((coordinates, movelist), problem.getCostOfActions(movelist))

  # generic empty return if we get here.
  return []


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"

  # use priority queue to have costs
  fringe = util.PriorityQueue()
  fringe.push((problem.getStartState(), []), 0)
  explored = []

  while not fringe.isEmpty():
    # get the next location
    location, moves = fringe.pop()

    # if we find the goal state, then we should be done.
    # all other items in the p_queue will have worse cost
    if problem.isGoalState(location):
      return moves

    for coordinates, direction, cost in problem.getSuccessors(location):
      if not coordinates in explored:
        movelist = moves + [direction]
        new_cost = problem.getCostOfActions(movelist) + heuristic(coordinates, problem)
        # push explored to fringe. also append or a* will fail
        explored.append(coordinates)
        fringe.push((coordinates, movelist), new_cost)

  return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch