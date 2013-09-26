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
  # terminal test or depth=0
  def terminalTest(self, gameState, depth):
    return gameState.isWin() or gameState.isLose() or depth == 0

  def maxValue(self, gameState, agentIndex, depth):
    # terminal test
    if self.terminalTest(gameState, depth):
      # utility of game state
      return self.evaluationFunction(gameState)

    v = float("-inf")

    # agentIndex should be 0, since max should be run only on pacman
    # calculate for each action, all possible new game states
    for action in gameState.getLegalActions(agentIndex):
      v = max(v, self.minValue(gameState.generateSuccessor(agentIndex, action), agentIndex+1, depth-1))
    return v

  def minValue(self, gameState, agentIndex, depth):
    # terminal test
    if self.terminalTest(gameState, depth):
      # utility of game state
      return self.evaluationFunction(gameState)

    v = float("inf")
    numAgents = gameState.getNumAgents()

    # need to minimize over all ghosts
    if agentIndex == numAgents-1:
      nextAgentIndex = 0
    else:
      nextAgentIndex = agentIndex+1

    if agentIndex == 0:
      nextDepth = depth-1
    else:
      nextDepth = depth

    for action in gameState.getLegalActions(agentIndex):
      if nextAgentIndex == 0: # go back to pacman, since all the ghosts are done
        v = min(v, self.maxValue(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, nextDepth))
      else:
        v = min(v, self.minValue(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, nextDepth))
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
    # current best score
    curBestScore = float("-inf")
    for action in gameState.getLegalActions(0):
      newScore = max(curBestScore, self.minValue(gameState.generateSuccessor(0, action), 1, self.depth))
      if newScore > curBestScore:
        curBestAction = action
        curBestScore = newScore
    print curBestScore
    return curBestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    def maxValue(gameState, agentIndex, alpha, beta, depth):
      # terminal test
      if gameState.isWin() or gameState.isLose() or depth == 0:
        # utility of game state
        return self.evaluationFunction(gameState)
      v = float("-inf")
      # calculate for each action, all possible new game states
      for action in gameState.getLegalActions(agentIndex):
        v = max(v, minValue(gameState.generateSuccessor(0, action), 1, alpha, beta, depth-1))
        # if better than beta, then we're done here
        if v >= beta:
          return v
        alpha = max(alpha, v)
      return v

    def minValue(gameState, agentIndex, alpha, beta, depth):
      # terminal test
      if gameState.isWin() or gameState.isLose() or depth == 0:
        # utility of game state
        return self.evaluationFunction(gameState)


      v = float("inf")
      numAgents = gameState.getNumAgents()

      for action in gameState.getLegalActions(agentIndex):

        # need to minimize over all ghosts
        if agentIndex == numAgents-1: # go back to pacman, did all the ghosts
          v = min(v, maxValue(gameState.generateSuccessor(agentIndex, action),0,alpha,beta,depth-1))
        else:
          v = min(v, minValue(gameState.generateSuccessor(agentIndex,action),agentIndex+1,alpha,beta,depth))
      if v <= alpha:
        return v
      beta = min(beta, v)
      return v

    bestAction = Directions.STOP
    score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for action in gameState.getLegalActions():
      newScore = max(score, minValue(gameState.generateSuccessor(0,action),1,alpha, beta, self.depth))
      if newScore > score:
        bestAction = action
        score = newScore
      if score >= beta: # WHERE DO YOU UPDATE BETA??
        return bestaction
      alpha = max(alpha, score)
    return bestAction


    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

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

