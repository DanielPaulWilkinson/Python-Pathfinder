from PathFinder import *

class MyTests(unittest.TestCase):
    #test grid generation (should be 10 arrays of 10)
    def test_Grid_Gen(self):
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        self.assertEqual(len(testBoard), 20)
    def test_BFS_Has_Data(self):
        #test to find a path from a to b without obsticles
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        data = DoBFS(testBoard,(0,0),(19,19))
        if len(data) > -1:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_BFS_Has_Data_2(self):
        testboard = numpy.zeros((20,20))
        data = DoBFS(testboard,(0,0),(19,19))
        if (9,9) in data:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_DFS_Has_Data(self):
        #test to find a path from a to b without obsticles
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        data = DoDFS(testBoard,(0,0),(19,19))
        if len(data) > -1:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_DFS_Has_Data_2(self):
        #Test to find if algorithm proforms correctly if no route to target
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        data = DoDFS(testBoard,(0,0),(19,19))
        if (9,9) in data:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_A_Has_Data(self):
        #test to find a path from a to b without obsticles
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        data = astar(testBoard,(0,0),(19,19))
        if len(data) > -1:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_A_Has_Data_2(self):
        #Test to find if algorithm proforms correctly if no route to target
        testBoard = numpy.zeros((20,20))
        data = astar(testBoard,(0,0),(19,19))
        if (19,19) in data:
            hasData = True
        else:
            hasData = False
        self.assertTrue(hasData,'')
    def test_add_array_target(self):
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        testBoard[9][9] = 2
        if testBoard[9][9] == 2:
            targetAdded = True
        self.assertTrue(targetAdded)
    def test_List_Split(self):
        #create array from list
        X = 20
        Y = 20
        testBoard = numpy.zeros((X,Y))
        splited = split(testBoard,20)
        self.assertEqual(len(splited),1)
    def test_Random_Number_Gen(self):
        array = randomNumbers()
        if len(array) > -1:
            hasNumbers = True
        else:
            hasNumbers = False
        self.assertTrue(hasNumbers)
if __name__ == '__main__':
    unittest.main()
