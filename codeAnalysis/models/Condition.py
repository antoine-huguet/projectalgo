'''The class for the Condition objects.
Conditions are either Conjonction XOR Disjonction or a list of either Condition or smallCondition.
smallCondition are either an inequality XOR an equality between the left and the right member.
'''

import Variable

class Condition():

    #Constructor
    def __init__(self, arg, type=None):
        if type not in ["or","and"]:
            self.type = "and" #We take the arbitrary decisions to favorise 'and' and not 'or', might be better solutions tho
        else:
            self.type = type
        self.arg = arg #List of all conditions which compose the condition
        self.numberOfArg = len(arg)
    
    #Private methods


    # Public methods

    def writeCondition(self):
        '''Recursively write the condition'''
        conditionWritten = ""
        for condition in self.arg:
            conditionWritten += condition.writeCondition() + type
        return conditionWritten

    def evaluateCondition(self):
        '''Evaluate recursively the conditions'''
        evaluation = [condition.evaluationCondition() for condition in self.arg]
        if type=='or':
            return any(evaluation)
        elif type=='and':
            return all(evaluation)
        #No default return, one more safety

class SmallCondition():

    #Constructor

    def __init__(self,sign,lMember,rMember):
        if type(lMember)!=type(Variable) or type(rMember)!=type(Variable) or sign not in ["==","=","<=","<",">",">="]:
            raise ValueError "Incorrect smallConidtion arguments."
        #We assume we have correct value here
        self.lMember = lMember
        self.rMember = rMember
        self.sign = sign
        #We allow the possibility to just enter '=' for equality, might be easier down the road
        if self.sign = '=':
            self.sign = '=='
        self.__checkCoherence__()

    # Private methods

    def __checkCoherence__(self):
        '''Check that both types of the test have the same types'''
        if self.lMember.type != self.rMember.type:
            raise ValueError "The two members don't have the same type."
    
    # Public methods

    def writeCondition(self):
        '''Write the code as it will be in the actual python code'''
        lMemberWrite = self.lMember.realName
        rMemberWrite = self.rMember.realName
        condition = '(' + lMemberWrite + sign + rMemberWrite + ')'
        return condition


    def evaluateCondition(self):
        '''Returns whether or not the condition is true with the current states of the members'''
        if self.sign == '==':
            return self.lMember.value == self.rMember.value
        elif self.sign == '>':
            return self.lMember.value > self.rMember.value
        elif self.sign == '<':
            return self.lMember.value < self.rMember.value
        elif self.sign == '>=':
            return self.lMember.value >= self.rMember.value
        elif self.sign == '<=':
            return self.lMember.value <= self.rMember.value
        else:
            return False #Probably not needed as we check the sign early on, but still useful