#!/usr/bin/python
#Daniel Wilkinson - BG69TG - 1111863434 - thursday 20th of april 2017
#Get All Imports
import numpy
from heapq import *
import math
from  tkinter import *
import random
import unittest



#class to generate grid, handle clicks for walls, handle application of
# red path, start and finish
class GridGeneration:
    def __init__ (self,master,board):
        #location of elements in UI using Tkinker
        Rootframe = Frame(master)
        Rootframe.pack()
        self.GridFrame = Frame(Rootframe)
        self.GridFrame.pack()
        #draw the grid on load
        self.redrawGrid(board)
        #when a grid label is clicked....
    def on_click(self,i,j,event):
        #find the value in array
        value = BACKEND[i,j]
        #if 1 then remove the 1 apply 0 (remove wall)
        if value == 1:
            BACKEND[i][j] = 0
            if (i,j) in Grid_walls:
                Grid_walls.remove((i,j))
        #if 0 then add 1 apply wall
        elif value == 0:
            BACKEND[i,j] = 1
            color = 'black'
            fg = 'white'
            #ensure the colour change of the clicked button for clarity of algorithm path
            event.widget.config(bg=color, fg=fg)
            wallcoord = (i,j)
            Grid_walls.append(wallcoord)
        if PreviouslySelectedAlgorithm == 'A':
            beginWithAStar()
        elif PreviouslySelectedAlgorithm == 'B':
            beginWithBreath()
        elif PreviouslySelectedAlgorithm == 'D':
            beginWithDepth()
        #method to display start position
    def addstart(self,x,y):
        global matrixofbuttons
        matrixofbuttons[x][y].config(bg='orange',text='Start', fg='black')
        #display end
    def addend(self,x,y):
        global matrixofbuttons
        matrixofbuttons[x][y].config(bg='orange',text='End', fg='black')
    def addRedPath(self,x,y):
        #for each of the coords passed in change the colour too orange and add coordinates.
        global matrixofbuttons
        matrixofbuttons[x][y].config(bg='orange',text=''+str(x)+','+str(y)+'', fg='black')
    def addMazeWall(self,x,y):
        #add colour of walls whenever one is clicked or generated.
        global matrixofbuttons
        matrixofbuttons[x][y].config(bg='black',fg='white')
    #method to redraw the grid whenever is needed...
    def redrawGrid(self,board):
        for i,row in enumerate(board):
            for j,column in enumerate(row):
                L = Label(self.GridFrame,text=''+str(i)+','+str(j)+'', bg='grey')
                L.grid(padx=5, pady=5)
                L.grid(row=i,column=j)
                L.bind('<Button-1>',lambda e,i=i,j=j: self.on_click(i,j,e))
                GridButtons.append(L)
    #method to return the whole board to grey
    def resetGrid(self,board,matrix):
        #convert the whole board back to grey showing numbers...
        for i,row in enumerate(board):
            for j,column in enumerate(row):
                matrix[i][j].config(bg='grey',text=''+str(i)+','+str(j)+'', fg='black')
                BACKEND[i,j] = 0
        #But rememember walls may still be present... throw walls back onto the gird (up to user to remove..)
        for x in range(len(Grid_walls)):
            value = Grid_walls[x]
            matrix[value[0]][value[1]].config(bg='black', fg='white')
            BACKEND[value[0],value[1]] = 1
    def removeWalls(self):
        #option to remove all walls insead of clicking each individually
        global Grid_walls
        for x in range(len(Grid_walls)):
            value = Grid_walls[x]
            V1 = value[0]
            V2 = value[1]
            BACKEND[V1,V2] = 0
        Grid_walls = []
        #option to remove single wall changes colour.
    def removeSingleWall(self,x,y):
        global matrixofbuttons
        matrixofbuttons[x][y].config(bg='grey',fg='black')

#Handles the build of the UI elements
class Inputs:
    def __init__(self,master,board):
        Rootframe = Frame(master)
        Rootframe.pack()
        inputframe = Frame(Rootframe)
        inputframe.pack(side=LEFT)
        #Create specific frame for
        self.usertext = StringVar()
        initalMessage = 'Algorithm Path is displayed here.'

        #create UI elements
        self.SelectedAlgorithm=Entry(inputframe,width=40)
        self.SelectedAlgorithm.delete(0, END)
        self.SelectedAlgorithm.insert(0, "Currently Selected Algorithm: None.")
        self.StartCoordLabel=Label(inputframe, text="Enter Starting Coordinates:")
        self.StartCoordTextbox = Entry(inputframe)
        self.StartCoordTextbox.delete(0, END)
        self.StartCoordTextbox.insert(0, "0,0>")
        self.EndCoordLabel=Label(inputframe, text="Enter Ending Coordinates:")
        self.EndCoordTextBox = Entry(inputframe)
        self.EndCoordTextBox.delete(0, END)
        self.EndCoordTextBox.insert(0, "<19,19")
        self.PathLabel=Label(inputframe, text="Algorithm Path (S-F)")
        self.PathLabelF=Label(inputframe, text="Algorithm Path (F-S)")
        self.PathTextbox = Text(inputframe,width=20,height=6,wrap=WORD,bg='grey',padx=20)
        self.PathTextbox.delete(0.0, END)
        self.PathTextbox.insert(0.0, initalMessage)
        self.PathTextboxF = Text(inputframe,width=20,height=6,wrap=WORD,bg='grey',padx=20)
        self.PathTextboxF.delete(0.0, END)
        self.PathTextboxF.insert(0.0, initalMessage)
        self.AlgorithmOptions=Label(inputframe, text="Algorithm Options",padx=20)
        self.btnDepth = Button(inputframe, text='Depth First Search', fg='black',command=beginWithDepth)
        self.btnBreath = Button(inputframe, text='Breadth First Search', fg='black',command=beginWithBreath)
        self.btnA = Button(inputframe, text=' A* Search', fg='black', command=beginWithAStar)
        self.btnWall = Button(inputframe, text='Remove All Walls', fg='black',command=GIRD.removeWalls)
        self.btnMaze = Button(inputframe, text='Add Walls', fg='black',command=randomMaze)
        self.WallLabel = Label(inputframe,text="Wall Options")
        self.emptyLabel1 = Label(inputframe,text=" ")
        self.emptyLabel2 = Label(inputframe,text=" ")
        self.emptyLabel3 = Label(inputframe,text=" ")
        self.emptyLabel4 = Label(inputframe,text=" ")
        #place elements in .grid rows and column s
        self.SelectedAlgorithm.grid(row=1,column=1, columnspan=3)
        self.emptyLabel4.grid(row=2,column=1)
        self.StartCoordLabel.grid(row=3, column=1 ,sticky=E)
        self.StartCoordTextbox.grid(row=3,column=2)
        self.EndCoordLabel.grid(row=4, column=1,sticky=E)
        self.EndCoordTextBox.grid(row=4,column=2)
        self.emptyLabel2.grid(row=5,column=1)
        self.emptyLabel3.grid(row=5)
        self.PathLabel.grid(row=6, column=1)
        self.PathTextbox.grid(row=7,column=1,columnspan=1,rowspan=3)
        self.PathTextboxF.grid(row=7,column=2,columnspan=1,rowspan=3)
        self.PathLabelF.grid(row=6,column=2)
        self.AlgorithmOptions.grid(row=1)
        self.btnBreath.grid(row=2)
        self.btnDepth.grid(row=3)
        self.btnA.grid(row=4)
        self.WallLabel.grid(row=7)
        self.btnWall.grid(row=8)
        self.btnMaze.grid(row=9)


#adds target for BFS/DFS
def addTarget(x,y):
    BACKEND[(x,y)] = 2
def removeTarget(x,y):
#removes target when Coordinates change
    BACKEND[(x,y)] = 0
#simple way to update a widget
def updateText(widget, data,value):
    widget.delete(value, END)
    widget.insert(value, data)
#algorithms ============================================================

def heuristic(a, b):
	return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
#A*
def astar(array, start, goal):
	#neighbours to search
    neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    #closed set the set of nodes already evaluated
    close_set = set()
    #stores the last known position
    came_from = {}
    #the cost of going from start to start is 0
    gscore = {start:0}
    #the first node is completely heuristic
    fscore = {start:heuristic(start, goal)}
    #code to store variables
    oheap = []
    heappush(oheap, (fscore[start], start))
    while oheap:
        current = heappop(oheap)[1]
        #if the current node is the goal node
        if current == goal:
            #create an array to store the returned path
            data = []
            #store all the data
            while current in came_from:
                data.append(current)
                current = came_from[current]
                #return the data
            return data
            #add the searched node to list of searched nodes
        close_set.add(current)
        #forloop to traverse Array by looking at the closest nodes
        for i, j in neighbors:
            #start to move
            neighbor = current[0] + i, current[1] + j
            #get the value of the gscore vs hurtistic
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            #do not collect values if hit X,Y & WALL
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # Opps, hit a Y wall
                    continue
            else:
                # Opps hit a X wall
                continue
                #also ignore if node is already evaluated
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                #current path is fine so store it.
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                #else return false so we know we cannot make it for example past a wall
    return (0,0)

#breath first algorithm
def DoBFS(array,start,end):
    # Generate a grid to search in
    grid = array
	# we've been to
    visited = []
	# queue of new places to look
    toSearch = [start]
    while len(toSearch) > 0:
        # get the new position
        pos = toSearch.pop(0)
        visited.append(pos)
        if grid[pos[0]][pos[1]] == 2: # found it!
            break
        for off in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            newpos = (pos[0] + off[0], pos[1] + off[1])
            if newpos[0] < 0 or newpos[0] >= 20 or newpos[1] < 0 or newpos[1] >= 20: # invalid
                continue
            elif newpos in visited: # been here
                continue
            elif newpos in toSearch: # gonna be here
                continue
            elif grid[newpos] == 1: # avoid these walls
                continue
            toSearch.append(newpos)
    return (visited)

def DoDFS(array,start,end):
    grid = array
    visited = []
    toSearch = [start]
    while len(toSearch) > 0:
        pos = toSearch.pop()
        visited.append(pos)
        if grid[pos[1]][pos[0]] == 2: #unlike BFS search depth 1-0 instead of 0-1
            break
        for off in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            newpos = (pos[0] + off[0], pos[1] + off[1])
            if newpos[0] < 0 or newpos[0] >= 20 or newpos[1] < 0 or newpos[1] >= 20:
                continue
            elif newpos in visited:
                continue
            elif grid[newpos] == 1:
                continue
            elif newpos in toSearch: # gonna be here
                continue
            toSearch.append(newpos)
    return (visited)
#Algorithm settups =======================================================
#I.E: parse text input, start algorithm, apply start, path and end to grid.
def beginWithAStar():
    global PreviouslySelectedAlgorithm
    PreviouslySelectedAlgorithm = 'A'
    global matrixofbuttons
    updateText(INPUTS.SelectedAlgorithm,'Currently Selected Algorithm: A*.',0)
    GIRD.resetGrid(BOARD,matrixofbuttons)
    start  = INPUTS.StartCoordTextbox.get()
    end = INPUTS.EndCoordTextBox.get()
    startingStrings = list(map(int, re.findall(r'\d+', start)))
    endingStrings = list(map(int, re.findall(r'\d+', end)))
    S1	= int(startingStrings[0])
    S2	= int(startingStrings[1])
    S3	= int(endingStrings[0])
    S4	= int(endingStrings[1])
    checkStartandEnd((S1,S2),(S3,S4),'A')
    dataSF = astar(BACKEND, (S1,S2), (S3,S4))
    dataFS = astar(BACKEND, (S3,S4), (S1,S2))
    if (S1,S2) in dataFS:
        dataFS.reverse()
        updateText(INPUTS.PathTextboxF,dataFS,0.0)
    else:
        updateText(INPUTS.PathTextboxF,'Cannot Reach Target: '+str((S1,S2)),0.0)
    if (S3,S4) in dataSF:
        dataSF.reverse()
        dataSF.append((S1,S2))
        updateText(INPUTS.PathTextbox,dataSF,0.0)
    else:
        updateText(INPUTS.PathTextbox,'Cannot Reach Target: '+str((S3,S4)),0.0)
    try:
        if len(dataSF) > -1:
            for x in range(len(dataSF)):
                value = dataSF[x]
                if(value[0] > -1):
                    if(value[1] > -1):
                        GIRD.addRedPath(value[0],value[1])
    except:
        pass
    GIRD.addstart(S1,S2)
    GIRD.addend(S3,S4)

def beginWithBreath():
    global PreviouslySelectedAlgorithm
    PreviouslySelectedAlgorithm = 'B'
    global matrixofbuttons
    updateText(INPUTS.SelectedAlgorithm,'Currently Selected Algorithm: Breadth First Search.',0)
    GIRD.resetGrid(BOARD,matrixofbuttons)
    start  = INPUTS.StartCoordTextbox.get()
    end = INPUTS.EndCoordTextBox.get()
    startingStrings = list(map(int, re.findall(r'\d+', start)))
    endingStrings = list(map(int, re.findall(r'\d+', end)))
    S1	= int(startingStrings[0])
    S2	= int(startingStrings[1])
    S3	= int(endingStrings[0])
    S4	= int(endingStrings[1])
    checkStartandEnd((S1,S2),(S3,S4),'BFS')
    addTarget(S3,S4)
    dataSF= DoBFS(BACKEND, (S1,S2), (S3,S4))
    removeTarget(S3,S4)
    addTarget(S1,S2)
    dataFS = DoBFS(BACKEND,(S3,S4),(S1,S2))
    if (S1,S2) in dataFS:
        updateText(INPUTS.PathTextboxF,dataFS,0.0)
    else:
        updateText(INPUTS.PathTextboxF,'Cannot Reach Target.',0.0)
    if (S3,S4) in dataSF:
        updateText(INPUTS.PathTextbox,dataSF,0.0)
    else:
        updateText(INPUTS.PathTextbox,'Cannot Reach Target.',0.0)
    for x in range(len(dataSF)):
        value = dataSF[x]
        GIRD.addRedPath(value[0],value[1])
    GIRD.addstart(S1,S2)
    GIRD.addend(S3,S4)
def beginWithDepth():
    global PreviouslySelectedAlgorithm
    PreviouslySelectedAlgorithm = 'D'
    global matrixofbuttons
    updateText(INPUTS.SelectedAlgorithm,'Currently Selected Algorithm: Depth First Search.',0)
    GIRD.resetGrid(BOARD,matrixofbuttons)
    start  = INPUTS.StartCoordTextbox.get()
    end = INPUTS.EndCoordTextBox.get()
    startingStrings = list(map(int, re.findall(r'\d+', start)))
    endingStrings = list(map(int, re.findall(r'\d+', end)))
    S1	= int(startingStrings[0])
    S2	= int(startingStrings[1])
    S3	= int(endingStrings[0])
    S4	= int(endingStrings[1])
    checkStartandEnd((S1,S2),(S3,S4),'DFS')
    addTarget(S3,S4)
    dataSF = DoDFS(BACKEND, (S1,S2), (S3,S4))
    removeTarget(S3,S4)
    addTarget(S1,S2)
    dataFS = DoDFS(BACKEND,(S3,S4),(S1,S2))
    if (S1,S2) in dataFS:
        updateText(INPUTS.PathTextboxF,dataFS,0.0)
    else:
        updateText(INPUTS.PathTextboxF,'Cannot Reach Target.',0.0)
    if (S3,S4) in dataSF:
        updateText(INPUTS.PathTextbox,dataSF,0.0)
    else:
        updateText(INPUTS.PathTextbox,'Cannot Reach Target.',0.0)
    for x in range(len(dataSF)):
        value = dataSF[x]
        GIRD.addRedPath(value[0],value[1])
    GIRD.addstart(S1,S2)
    GIRD.addend(S3,S4)
#split array into smaller arrays
def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs
#maze generation
def randomMaze():
    start  = INPUTS.StartCoordTextbox.get()
    end = INPUTS.EndCoordTextBox.get()
    startingStrings = list(map(int, re.findall(r'\d+', start)))
    endingStrings = list(map(int, re.findall(r'\d+', end)))
    S1	= int(startingStrings[0])
    S2	= int(startingStrings[1])
    S3	= int(endingStrings[0])
    S4	= int(endingStrings[1])
    newArrayWallS = randomNumbers()
    for x in newArrayWallS:
        if(x[0],x[1])!=(S1,S2):
            if(x[0],x[1])!=(S3,S4):
                    if(x[0],x[1]) not in Grid_walls:
                        Grid_walls.append((x[0],x[1]))
    for x in Grid_walls:
        GIRD.addMazeWall(x[0],x[1])
        BACKEND[(x[0],x[1])] = 1
    if PreviouslySelectedAlgorithm == 'A':
        beginWithAStar()
    elif PreviouslySelectedAlgorithm == 'B':
        beginWithBreath()
    elif PreviouslySelectedAlgorithm == 'D':
        beginWithDepth()
#random numbeer generation
def randomNumbers():
    randomArray = []
    for x in range(10):
        b = random.randint(0,19)
        y = random.randint(0,19)
        randomArray.append((b,y))
    return randomArray
def checkStartandEnd(start,end,algorithm):
    #Func required to find out if a wall has been placed over
    #a start or end point AS walls can be generated over this area
    if end in Grid_walls:
        if algorithm != 'A':
            BACKEND[end] = 2 #make a target
        else:
            BACKEND[end] = 0
    if start in Grid_walls:
        BACKEND[start] = 0
root = Tk()
root.title("Python Path Finder")
#Arrays, Lists etc...
Grid_walls = []#to store all walls
GridButtons = []
MazeWallList = []
# store all clickable labels (easy to config this way)
#constants = access to classes and grid back and frount end.
BACKEND = numpy.zeros((20,20))
BOARD = [ [0]*20 for _ in range(20) ]
#ensure clean grid/clean board
for x in BACKEND:
    x = 0
for x in BOARD:
    x = 0
#if a wall is placed over the algorithm this algorithm needs to adapt to its new path
#this means we need to remember the last selected algorithm the user clicked to update that algorithm
PreviouslySelectedAlgorithm = ''
#GENERATE GRID CLASS
GIRD = GridGeneration(root,BOARD)
#matrix of buttons (visual board) - gives access to X/Y of button to update text/colour
matrixofbuttons = split(GridButtons,20)
#INPUT class creates UI
INPUTS = Inputs(root,BOARD)
#start with an algarithm by default
beginWithAStar()
#tkinter main UI loop.
root.mainloop()
