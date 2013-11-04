'''
Created on Oct 20, 2013

@author: Ofra
'''
from Action import Action
from ActionLayer import ActionLayer
from Pair import Pair
from Proposition import Proposition
from PropositionLayer import PropositionLayer

class PlanGraph(object):
    '''
    A class for representing a level in the plan graph. For each level i, the PlanGraph consists of the actionLayer and propositionLayer at this level
    '''


    def __init__(self, level, independentActions):
        '''
        Constructor
        '''
        self.level = level
        self.independentActions = independentActions # a list of the independent actions (this would be the same at each level)
        self.actionLayer = ActionLayer()
        self.propositionLayer = PropositionLayer();

    def getPropositionLayer(self):
        return self.propositionLayer

    def setPropositionLayer(self, propLayer):
        self.propositionLayer = propLayer

    def getActionLayer(self):
        return self.actionLayer

    def expand(self, previousLevel, allProps, allActions): #you can change the params the function takes if you like
        '''YOUR CODE HERE'''
        pass


    def mutexActions(self, a1, a2, mutexProps):
        '''YOUR CODE HERE: complete code for deciding whether actions a1 and a2 are mutex, given the previous proposition layer. Your exapnd function should call this function'''
        pass

    def mutexPropositions(self, prop1, prop2, mutexActions):
        '''YOUR CODE HERE: complete code for deciding whether propositions p1 and p2 are mutex, given the previous proposition layer. Your exapnd function should call this function'''
        pass
