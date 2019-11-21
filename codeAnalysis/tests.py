from unittest import *

class TestStringMethods(unittest.TestCase):
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()

'''
blocklist=[[Bloc(5),Bloc(3,args=('a',1))],[Bloc(6),Bloc(3,args=('b',2))],[Bloc(7),Bloc(3,args=('c',1))],[Bloc(8),Bloc(3,args=('d',Calculstring('b²-4ac')))],[Bloc(2,args=(None,'d'))]]
'''
#code qui print le discriminant de aX²+bX+c
#code=1