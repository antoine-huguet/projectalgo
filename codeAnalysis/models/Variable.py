'''The class for the Variable objects.
The Variable objects are used to link real python variable to bloc types affectation.
As of now the only accepted types for a Variable object are :
- int
- bool
- string
'''

import config #Get the global variable

#TODO : add dict/list to associate id to variable object

class Variable():

    #Constructor
    def __init__(self,name,initValue=None,type=None):
        self.name = name #name given by the user
        self.value = value #Value of the variable
        self.__checkValue__()
        self.__setId__()
        self.__setRealName__() #Name used in the code : variable.realName

    #Internal methods, to consider private

    def __setId__(self):
        '''Auto incr global id counting, and set id for the variable'''
        global config.variableId
        self.id = config.variableId
        config.variableId +=1

    def __setType__(self):
        '''Set type of the value according to its value'''
        if self.value==None:
            self.type==None
        else:
            self.type = type(self.value)

    def __checkValue__(self):
        '''As of now, we only allow for int, bool, and string''''
        self.__setType__()
        if self.type not in [type(int),type(str),type(bool)]:
            self.value=None
        self.__setType__()
    
    def __setRealName__(self):
        '''Give the real name of the variable, ie the one used in the code'''
        self.realName = "var"+str(self.id)

    # Public methods
    
    # TODO : add public mehods (if any needed)

    