'''
Created on Sep 23, 2013

@author: Your name here
'''

import random;

def WalkSAT(clauses,p,max_flips):
    """YOUR CODE HERE"""
    # model <-- random assignment of true/false to symbols in clauses

    for c in clauses:
        for lit in c.literals:
            if (random.random() > 0.5):
                lit.setValue(True)
            else:
                lit.setValue(False)

    #for i = 1 to max_flips:
    for i in range(0,max_flips):
        # for max count in randomizer later
        numSatisfied = 0

        # if model satifies clauses:
        #     return model
        for c in clauses:
            allTrue = True
            if c.evaluate == False:
                allTrue = False
                # don't break so we can count all clauses that are satisfied
            else:
                numSatisfied += 1

        if allTrue:
            return clauses

        # clause = randomly selected clause from clauses that are false in model
        randClauseIndex = int(random.random()*len(clauses))
        randClause = clauses[randClauseIndex]
        literals = randClause.literals

        # with prob p:
        #     flip the value of a randomly selected symbol in clause
        if random.random() <= p:
            randSymbolIndex = int(random.random()*len(literals))
            literals[randSymbolIndex].setValue(not literals[randSymbolIndex].value)
        # else:
        #     flip the symbol in clause that maximizes the number of satisfied clauses
        else:
            index = -1
            for i in range(0, len(literals)):
                literals[i].setValue(not literals[i].value)

                newSatisfied = 0
                # check number satisfied
                for c in clauses:
                    if c.evaluate == True:
                        newSatisfied += 1
                if newSatisfied >= numSatisfied:
                    numSatisfied = newSatisfied
                    index = i
                literals[i].setValue(not literals[i].value)
            literals[index].setValue(not literals[index].value)

    return False




class Literal:
    """Represents a literal"""

    def __init__(self, name, negated):
        self.name = name #literal name
        self.negated = negated #is the literal negated

    def __eq__(self, other):
        return self.name == other.name

    def setValue(self, value):
        self.value = value; # value of symbol (True or False)

    def evaluate(self):
    # evaluates whether overall the literal is true or false.
    # For example if value = true and negated = false, then the literal will be evaluated as true
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
    # ~C V KF V HF
    # ~F V NF V BF
    # ~BC V FF V LF
    # ~HBP V KF V BF
    # ~H V NF V HF V KF

    # C = Literal('C',True)
    # KF = Literal('KF', False)
    # HF = Literal('HF', False)
    clause1 = Clause([Literal('C',True),    Literal('KF', False),Literal('HF', False)])
    clause2 = Clause([Literal('F', True),   Literal('NF', False),Literal('BF', False)])
    clause3 = Clause([Literal('BC', True),  Literal('FF', False),Literal('LF', False)])
    clause4 = Clause([Literal('HBP', True), Literal('KF', False),Literal('BF', False)])
    clause5 = Clause([Literal('H', True),   Literal('NF', False),Literal('HF', False), Literal('KF', False)])

    clauses = [clause1, clause2, clause3, clause4, clause5]
    p = 0.5
    max_flips = 10

    model = WalkSAT(clauses, p, max_flips)

    if not model:
        print "Failure"
    else:
        for c in model:
            for lit in c.literals:
                print lit.__str__() + " "
            print "\n"
    # print function is pretty wonky
    # print model.__str__()