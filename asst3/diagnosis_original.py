'''
Created on Sep 23, 2013

@author: Your name here
'''

import random;

def WalkSAT(clauses,p,max_flips):
    """YOUR CODE HERE"""




class Literal:
    """Represents a literal"""
    
    def __init__(self, name, negated):
        self.name = name #literal name
        self.negated = negated #is the literal negated
    
    def __eq__(self, other):
        return self.name == other.name
    
    def setValue(self, value):
        self.value = value; # value of symbol (True or False)
    
    def evaluate(self): #evaluates whether overall the literal is true or false. For example if value = true and negated = false, then the literal will be evaluated as true
        if (self.value and not(self.negated)):
            return True
        elif (not(self.value) and self.negated):
            return True
        return False;
    def __str__(self):
        return self.name+";"+str(self.value)
        
class Clause:
    """represents a disjunctive clause"""
    def __init__(self, literals):
        self.literals = literals #a clause is composed of literals with disjunctions between them 
           
    def evaluate(self): #evaluated whether the clause is True or False
        for i in range(len(self.literals)):
            if (self.literals[i].evaluate()):
                return True #since this is a disjunction, one true literal is sufficient
        return False
    def __str__(self):
        return self.literals

if __name__ == '__main__':
    """"your code here: you should create the clauses that form an input to walkSAT and run walkSAT"""