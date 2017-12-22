# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

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
        legalMoves.remove('Stop')
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

        bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        for i in range(0,len(scores)):
            if(scores[i] == bestScore):
                return legalMoves[i]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # for ghostState in newGhostStates:
            # print manhattanDistance(newPos, ghostState.getPosition())
        # return successorGameState.getScore()
        foodlist = currentGameState.getFood().asList()
        distanceToClosestFood = min(map(lambda x: util.manhattanDistance(newPos, x), foodlist))
        distanceToClosestGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if distanceToClosestGhost == 0:
            return -50
        # print int(-8/distanceToClosestGhost)
        return -(8/distanceToClosestGhost)-distanceToClosestFood

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

    def getAction(self, gamestate):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def pacman(gameState, curDepth):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = gameState.getLegalActions(0)
            score = []
            for move in legalMoves:
                nextState = gameState.generateSuccessor(0, move)
                if nextState.isWin():
                        return self.evaluationFunction(nextState)
                score.append( ghost(nextState,curDepth,total_ghosts) )
            # print score,"score for pacman @",curDepth
            return max(score)

        def ghost(gameState, curDepth, ghost_idx):
            if curDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = gameState.getLegalActions(ghost_idx)
            score = []
            # Pacman's turn
            if ghost_idx == 1:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    score.append( pacman(nextState,curDepth+1) )
            # next ghost's turn
            else:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    score.append( ghost(nextState, curDepth, ghost_idx-1) )
            # print score,"score for ghost",ghost_idx,"@",curDepth
            return min(score)

        bestScore = -9999
        bestMove = 'Fail'
        total_ghosts = gamestate.getNumAgents()-1
        legalMoves = gamestate.getLegalActions(0)
        for move in legalMoves:
            nextState = gamestate.generateSuccessor(0, move)
            # if it can win immediately
            if nextState.isWin():
                return move
            tempScore = ghost(nextState, 1, total_ghosts)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove = move
        return bestMove

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gamestate):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def pacman(gameState, curDepth,A,B):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = [action for action in gameState.getLegalActions(0) if action!='Stop']
            score = -9999999
            for move in legalMoves:
                nextState = gameState.generateSuccessor(0, move)
                if nextState.isWin():
                        return self.evaluationFunction(nextState)
                score = max(score, ghost(nextState,curDepth,total_ghosts,A,B))
                if score > B:
                    return score
                A = max(A,score)
            # print score,"score for pacman @",curDepth
            return score

        def ghost(gameState, curDepth, ghost_idx,A,B):
            if curDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = gameState.getLegalActions(ghost_idx)
            score = 9999999
            # Pacman's turn
            if ghost_idx == 1:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    # score.append( pacman(nextState,curDepth+1) )
                    score = min(score, pacman(nextState,curDepth+1,A,B))
                    if score < A:
                        return score
                    B = min(B,score)
            # next ghost's turn
            else:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    # score.append( ghost(nextState, curDepth, ghost_idx-1) )
                    score = min(score, ghost(nextState, curDepth, ghost_idx-1,A,B))
            # print score,"score for ghost",ghost_idx,"@",curDepth
            return score

        bestScore = -99999999
        bestMove = 'Fail'
        total_ghosts = gamestate.getNumAgents()-1
        legalMoves = gamestate.getLegalActions(0)
        for move in legalMoves:
            nextState = gamestate.generateSuccessor(0, move)
            # if it can win immediately
            if nextState.isWin():
                return move
            tempScore = ghost(nextState, 1, total_ghosts,-9999999,9999999)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove = move
        return bestMove

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gamestate):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def pacman(gameState, curDepth):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = [action for action in gameState.getLegalActions(0) if action!='Stop']
            score = []
            for move in legalMoves:
                nextState = gameState.generateSuccessor(0, move)
                if nextState.isWin():
                        return self.evaluationFunction(nextState)
                score.append( ghost(nextState,curDepth,total_ghosts) )
            # print score,"score for pacman @",curDepth
            return max(score)

        def ghost(gameState, curDepth, ghost_idx):
            if curDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = gameState.getLegalActions(ghost_idx)
            score = 0
            # Pacman's turn
            if ghost_idx == 1:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    score += pacman(nextState,curDepth+1)
            # next ghost's turn
            else:
                for move in legalMoves:
                    nextState = gameState.generateSuccessor(ghost_idx, move)
                    if nextState.isLose():
                        return self.evaluationFunction(nextState)
                    score += ghost(nextState, curDepth, ghost_idx-1)
            # print score,"score for ghost",ghost_idx,"@",curDepth
            return (score*1.0)/len(legalMoves)

        bestScore = -999999
        bestMove = 'Fail'
        total_ghosts = gamestate.getNumAgents()-1
        legalMoves = gamestate.getLegalActions(0)
        for move in legalMoves:
            nextState = gamestate.generateSuccessor(0, move)
            # if it can win immediately
            if nextState.isWin():
                return move
            tempScore = ghost(nextState, 1, total_ghosts)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove = move
        return bestMove

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Farther the nearest food higher the score
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    foodlist = currentGameState.getFood().asList()
    distanceToClosestFood = min(map(lambda x: util.manhattanDistance(pacmanPos, x), foodlist))

    return currentGameState.getScore()+distanceToClosestFood

# Abbreviation
better = betterEvaluationFunction

