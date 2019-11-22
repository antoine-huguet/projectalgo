import unittest
from codeAnalysis.block_to_code import code_executable
from codeAnalysis.block_to_code import code_utilisateur
class TestStringMethods(unittest.TestCase):
    def __init__(self):
        self.blocklist = [[Bloc(5),Bloc(3,args=('a',1))],[Bloc(6),Bloc(3,args=('b',2))],[Bloc(7),Bloc(3,args=('c',1))],[Bloc(8),Bloc(3,args=('d',Calculstring('b²-4ac')))],[Bloc(2,args=(None,'d'))]]

    def test_code_executable(self):
        result='''A = 1
        B = 2
        C = 1
        D = B**2+4*A*C
        print(D)        
        '''
        self.assertEqual(code_executable(self.blocklist),result)
    
    def test_code_utilisateur(self):
        result = '''from time import sleep
        A=1
        sleep(0.2)
        display(bloc.args)
        B = 2
        sleep(0.2)
        display(bloc.args)
        C = 1
        sleep(0.2)
        display(bloc.args)
        D = B**2+4*A*C
        sleep(0.2)
        display(bloc.args)
        print(D) 
        ''' 
        self.assertEqual(code_utilisateur(self.blocklist),result)
        

if __name__ == '__main__':
    unittest.main()
