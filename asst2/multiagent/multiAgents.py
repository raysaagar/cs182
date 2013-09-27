# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

"""
Brandon Sim
Saagar Deshpande
CS182 Problem Set 2
9/26/13
"""

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  # terminal test, or depth=0
  def terminalTest(self, gameState, depth):
    return gameState.isWin() or gameState.isLose() or depth == 0

  def maxValue(self, gameState, agentIndex, depth):
    # terminal test, returns utility of terminal game state
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)

    v = float("-inf")

    actions = gameState.getLegalActions(agentIndex)
    actions.remove(Directions.STOP)
    # agentIndex should be 0, since max should be run only on pacman
    # calculate for each action, all possible new game states
    for action in gameState.getLegalActions(agentIndex):
      v = max(v, self.minValue(gameState.generateSuccessor(agentIndex, action), \
        agentIndex+1, depth))
    return v

  def minValue(self, gameState, agentIndex, depth):
    # terminal test, returns utility of terminal game state
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)

    v = float("inf")
    numAgents = gameState.getNumAgents()

    # need to minimize over all ghosts. if last ghost, then return to pacman and decrease depth
    nextAgentIndex = agentIndex+1
    nextDepth = depth
    nextFunction = self.minValue
    if agentIndex == numAgents-1:
      nextAgentIndex = 0
      nextDepth = depth-1
      nextFunction = self.maxValue

    for action in gameState.getLegalActions(agentIndex):
        v = min(v, nextFunction(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, nextDepth))
    return v

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1 

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    # current best action, default start is stop
    curBestAction = Directions.STOP
    curBestScore = float("-inf")
    actions = gameState.getLegalActions(0)
    actions.remove(Directions.STOP)
    for action in actions:
      newScore = self.minValue(gameState.generateSuccessor(0, action), 1, self.depth)
      if newScore > curBestScore:
        curBestAction = action
        curBestScore = newScore
    #print curBestScore #debug, test against Berkeley values
    return curBestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  # terminal test, or depth=0
  def terminalTest(self, gameState, depth):
    return gameState.isWin() or gameState.isLose() or depth == 0

  def maxValue(self, gameState, agentIndex, depth, alpha, beta):
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)
    v = float("-inf")
    actions = gameState.getLegalActions(agentIndex)
    actions.remove(Directions.STOP)

    for action in gameState.getLegalActions(agentIndex):
      v = max(v, self.minValue(gameState.generateSuccessor(agentIndex, action), \
        agentIndex+1, depth, alpha, beta))
      # if better than beta, then we're done here
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v

  def minValue(self, gameState, agentIndex, depth, alpha, beta):
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)

    v = float("inf")
    numAgents = gameState.getNumAgents()

    # need to minimize over all ghosts. if last ghost, then return to pacman and decrease depth
    nextAgentIndex = agentIndex+1
    nextDepth = depth
    nextFunction = self.minValue
    if agentIndex == numAgents-1:
      nextAgentIndex = 0
      nextDepth = depth-1
      nextFunction = self.maxValue

    for action in gameState.getLegalActions(agentIndex):
      v = min(v, nextFunction(gameState.generateSuccessor(agentIndex, action), \
        nextAgentIndex, nextDepth, alpha, beta))
      # if v is less than alpha, then we're done here
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # current best action, default start is stop
    curBestAction = Directions.STOP
    curBestScore = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    actions = gameState.getLegalActions(0)
    actions.remove(Directions.STOP)
    for action in actions:
      newScore = self.minValue(gameState.generateSuccessor(0, action), \
        1, self.depth, alpha, beta)
      if newScore > curBestScore:
        curBestAction = action
        curBestScore = newScore
      if curBestScore >= beta:
        return curBestAction
      alpha = max(alpha, curBestScore)
    # print curBestScore #debug, test against Berkeley values
    return curBestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def terminalTest(self, gameState, depth):
    return gameState.isWin() or gameState.isLose() or depth == 0

  def maxValue(self, gameState, agentIndex, depth):
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)
    v = float("-inf")
    actions = gameState.getLegalActions(0)
    actions.remove(Directions.STOP)
    for action in actions:
      v = max(v, float(self.chanceValue(gameState.generateSuccessor(agentIndex, action), \
        agentIndex+1, depth)))
    return v

  def chanceValue(self, gameState, agentIndex, depth):
    if self.terminalTest(gameState, depth):
      return self.evaluationFunction(gameState)
    v = float("inf")
    numAgents = gameState.getNumAgents()

    nextAgentIndex = agentIndex+1
    nextDepth = depth
    nextFunction = self.chanceValue
    if agentIndex == numAgents-1:
      nextAgentIndex = 0
      nextDepth = depth-1
      nextFunction = self.maxValue

    averageScore = 0
    actions = gameState.getLegalActions(agentIndex)
    for action in actions:
      averageScore += nextFunction(gameState.generateSuccessor(agentIndex, action), \
        nextAgentIndex, nextDepth)
    # assume uniform distribution over actions
    return averageScore / float(len(actions))

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    curBestAction = Directions.STOP
    curBestScore = float("-inf")
    actions = gameState.getLegalActions(0)
    actions.remove(Directions.STOP)
    for action in actions:
      newScore = float(self.chanceValue(gameState.generateSuccessor(0, action), \
        1, self.depth))
      if newScore > curBestScore:
        curBestAction = action
        curBestScore = newScore
    return curBestAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: We use the game's scoring functions so that Pacman will
    know not to die and that he knows that he gets points for eating ghosts,
    etc. In addition, we noticed that pacman often thrashes around without getting
    food in fear of getting caught by ghosts. To fix these problems, we use the 
    following:

    1)  we incentivize pacman to get food in the most efficient way possible
      this entails getting food while spending the least steps, since we lose 
      points for each step we take. to do this, we use the heuristic we used
      in our homework last week for search, which had a nodes expanded score of
      almost 7000. this calculates a higher score if pacman has to take a longer
      path to get to all the food, so we subtract it from the score to 
      incentivize shorter, more efficient paths.

    2)  next, we incentivize pacman to get capsules if there are not ghosts 
      ready to be eaten. we only deduct points for uneaten capsules if 
      the ghosts cannot be eaten, since we don't want pacman to waste a capsule
      by eating it when the ghosts are still in their weakened states.

    3)  finally, we incentivize pacman to eat ghosts which can be eaten.
    we check if the ghost's scared timer is higher than the ghost's distance from 
    pacman, which means that the ghost will remain scared for longer than the time
    it will take pacman to get there. if so, then we penalize pacman for not 
    going and eating the ghost. if the ghost timer is shorter than pacman's distance
    pacman cannot possibly eat the ghost, so we don't penalize pacman for not eating
    that ghost.

    4)  we strongly discourage pacman to not die, by returning -inf for dying.

    These four guiding principles helped us get very good results.

    Using n = 100 trials, we get a 91 percent win rate with an average 
    during wins of approximately 1500-1600.

  """
  "*** YOUR CODE HERE ***"
  manhattan = lambda c1, c2: abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
  position = currentGameState.getPacmanPosition()
  score = 0
  if currentGameState.isLose():
    return float("-inf")
  score = scoreEvaluationFunction(currentGameState)
  # incentivizes getting food in most efficient way possible
  score -= calculateFoodDistanceScore(currentGameState)
  ## If edible ghosts go eat
  # gets ghost states
  ghostStates = currentGameState.getGhostStates()
  # gets how long the ghosts are scared
  scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
  # gets the ghost positions
  ghostPositions = [ghostState.getPosition() for ghostState in ghostStates]
  # calculates manhattan distances to ghosts
  distancesToGhosts = [manhattan(gp, position) for gp in ghostPositions]
  # if pacman can reach the ghost before time runs out, give a penalty
  # which is more severe the farther away he is from the ghost
  distancePenaltyFactor = 1
  for i in range(len(scaredTimes)):
    if scaredTimes[i] > distancesToGhosts[i]:
      score -= distancePenaltyFactor * distancesToGhosts[i]
  # incentivizes getting capsules, but only if there aren't ghosts to eat
  capsuleLocs = currentGameState.getCapsules()
  if sum(scaredTimes) == 0:
    score -= 50*len(capsuleLocs)
  return score

def calculateFoodDistanceScore(currentGameState):
  foodGrid = currentGameState.getFood()
  position = currentGameState.getPacmanPosition()
  manhattan = lambda c1, c2: abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
  score = 0
  foodCoords = foodGrid.asList()

  # SOLUTION 1: Find bounding box around all uneaten food locations
  #finds bounding box around all uneaten food coordinates

  if foodCoords:
    minx = min([x[0] for x in foodCoords])
    miny = min([x[1] for x in foodCoords])
    maxx = max([x[0] for x in foodCoords])
    maxy = max([x[1] for x in foodCoords])
    bottomLeft = (minx, miny)
    bottomRight = (minx, maxy)
    topLeft = (maxx, miny)
    topRight = (maxx, maxy)
    cornerCoords = [bottomLeft, bottomRight, topLeft, topRight]
    # adds 'diagonal' manhattan distance
    score += manhattan(bottomLeft, topRight)
    # finds distance from current position to nearest corner of bounding box
    corner_dist = manhattan(position, min(cornerCoords, key=lambda c1: manhattan(c1, position)))
    # gets all foods on the edge
    #edgeFoodCoords = [x for x in foodCoords if x[0] == minx or x[0] == maxx or x[1] == miny or x[1] == maxy]
    #edgeFoodCoords = foodCoords
    # finds distance from current to closest food on edge
    closest_food = min(foodCoords, key=lambda c1: manhattan(c1, position))
    food_dist = manhattan(position, closest_food)
    score += max(corner_dist, food_dist)

    # if distance to closest food was added, add distance from food to closest corner
    if max(corner_dist, food_dist) == food_dist:
      score += manhattan(closest_food, min(cornerCoords, key=lambda c1: manhattan(c1, closest_food)))
  return score


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()