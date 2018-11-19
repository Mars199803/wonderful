# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class MinimaxGhost(GhostAgent):

    """
      Your minimax agent (question 1)

      useage: python2 pacman.py -p ExpectimaxAgent -l specialNew -g MinimaxGhost -a depth=4
              python2 pacman.py -l specialNew -g MinimaxGhost

    """
    "*** YOUR CODE HERE ***"


   def __init__( self, index, evalFun='betterEvaluationFunctionGhost',depth='4'):
        self.index=index
        self.depth=int(depth)
        self.evaluationFunction=util.lookup(evalFun,globals())
    
    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:   
            return Directions.STOP
        else:
            start=1
            ghost_index=self.index
            move=self.MinimaxEvaluationFunction(state,start,ghost_index,ghost_index)
            return move
        
    
    def getDistribution(self, state,agent_index,scores,moving):
        if (agent_index!=0)&(state!=1):
            return min(scores)
        elif (agent_index==0)&(state!=1) :
            return max(scores)
        else:
            optimum_index=[]
            for index in range(len(scores)):
                if scores[index]==min(scores):
                    optimum_index.append(index)
            get_index=random.choice(optimum_index)
            return moving[get_index]
    
    def MinimaxEvaluationFunction(self,state,layer,ghost_index,current_index):
        if(state.isLose()) or (state.isWin()):
            return self.evalutionFunction(state)
        if layer>self.depth:
            return self.evalutionFunction(state)
        moving=[]
        for i in gstate.getLegalActions(current_index):
            moving=[]
        if current_index==0:
            scores=[]
            for i in moving:
                scores.append(self.MinimaxEvaluationFunction(state.generateSuccessor(current_index,i),layer+1,ghost_index,ghost_index))
            return self.getDistribution(layer,current_index,scores,moving)
        else:
            scores=[]
            for x in moving:
                scores.append(self.MinimacEvalutionFunction(state.generateSuccessor(current_index,x),layer,ghost_index,0))
            return self.getDistribution(layer,current_index,scores,moving)








def betterEvaluationFunctionGhost(currentGameState):
    """
        Ghost evaluation function
    """



# Abbreviation
ghostEval = betterEvaluationFunctionGhost

