'''
Created on Sep 23, 2013

@Saagar Deshpande, Brandon Sim
CS 182
'''

import random
from random import choice

# updates all literals in all clauses
def updateClauses(clauses, literal_dict):
    for c in clauses:
        for lit in c.literals:
            lit.setValue(literal_dict[lit.name])
    return clauses

# walkSAT algorithm
def WalkSAT(clauses, p, max_flips):
    """YOUR CODE HERE"""
    literal_dict = {}
    for c in clauses:
        for lit in c.literals:
            literal_dict[lit.name] = False

    # model <-- random assignment of true/false to symbols in clauses
    for key in literal_dict:
        if (random.random() > 0.5):
            literal_dict[key] = True
        else:
            literal_dict[key] = False

    clauses = updateClauses(clauses, literal_dict)
    numClauses = len(clauses)

    #for i = 1 to max_flips:
    for i in range(max_flips):
        # for max count in randomizer later
        notSatisfiedClauses = []

        for j in range(numClauses):
            if clauses[j].evaluate() == False:
                notSatisfiedClauses.append(j)

        numNotSatisfied = len(notSatisfiedClauses)

        if numNotSatisfied == 0:
            return clauses

        # clause = randomly selected clause from clauses that are false in model
        randClause = clauses[choice(range(numNotSatisfied))]
        literals = randClause.literals

        # with prob p:
        #     flip the value  of a randomly selected symbol in clause
        if random.random() <= p:
            randSymbolIndex = choice(range(len(literals)))
            literal_dict[literals[randSymbolIndex].name] = not literals[randSymbolIndex].value
            # update each literal
            clauses = updateClauses(clauses, literal_dict)
        # else:
        #     flip the symbol in clause that maximizes the number of satisfied clauses
        else:
            index = -1
            numSatisfied = 0
            newSatisfied = 0
            for k in range(len(literals)):
                literal_dict[literals[k].name] = not literals[k].value
                #literals[i].setValue(not literals[i].value)
                clauses = updateClauses(clauses, literal_dict)

                # check number satisfied
                for c in clauses:
                    if c.evaluate == True:
                        newSatisfied += 1
                if newSatisfied >= numSatisfied:
                    numSatisfied = newSatisfied
                    index = k
                literal_dict[literals[k].name] = not literals[k].value
                clauses = updateClauses(clauses, literal_dict)
                #literals[i].setValue(not literals[i].value)
            literal_dict[literals[index].name] = not literals[index].value
            clauses = updateClauses(clauses, literal_dict)
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
    kf  =   Literal('kidney_failure',       False)
    hf  =   Literal('heart_failure',        False)
    bff =   Literal('bloodflow_failure',    False)
    nf  =   Literal('neuro_failure',        False)
    lf  =   Literal('liver_failure',        False)
    nkf =   Literal('kidney_failure',       True)

    Cough                   = Clause([kf, hf])
    Fever                   = Clause([nf, bff])
    Blood_clot              = Clause([bff, lf])
    Stomachache             = Clause([nkf])
    High_blood_pressure     = Clause([kf, bff])
    Headache                = Clause([nf, hf, kf])

    clauses = [Cough, Fever, Blood_clot, Stomachache, High_blood_pressure, Headache]

    p = 0.2
    max_flips = 5

    model = WalkSAT(clauses, p, max_flips)

    if not model:
        print "Failure"
    else:
        print "diagnosis: patient has"
        diagnosis = {}
        for c in model:
            for lit in c.literals:
                diagnosis[lit.name] = lit.value
        print [c for c in diagnosis if diagnosis[c]]

    # print function is pretty wonky
    # print model.__str__()