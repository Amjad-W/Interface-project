import API
import sys
import numpy as np
import math 
from collections import deque,Counter
from time import sleep

SIZE = 8

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def dirFunc(direction,turnDir):
    #    [0,  1] North
    #    [1,  0] East
    #    [0, -1] South
    #   [-1,  0] West   
    rotationMap = np.array([[0,1],[1,0],[0,-1],[-1,0]])
    pos = np.where(rotationMap == direction)
    if turnDir == 'R':
        return rotationMap[ ( pos[0][1] + 1 ) % 4 ]
    elif turnDir == 'L':
        return rotationMap[ ( pos[0][1] - 1 ) % 4 ]

def arreq_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)

def updateWallString(north,east,west,south,direction):
    stringList = list("xxxx")
    stringList[0] = '1' if north else '0'
    stringList[1] = '1' if east else '0'
    stringList[2] = '1' if west else '0'
    stringList[3] = '1' if south else '0'
    string = "".join(stringList)
    log("Direction: "+str( direction) )
    if( np.array_equal(direction,[0,1]) ):
        returnString =  string;
    elif( np.array_equal(direction,[1,0]) ):
        returnString = rightShift(string,1)
    elif( np.array_equal(direction,[0,-1]) ):
        returnString = rightShift(string,2)
    elif( np.array_equal(direction,[-1,0]) ):
        returnString =  leftShift(string,1)
    log("Wall: "+returnString)
    return returnString

def leftShift(text,n):
    return text[n:] + text[:n]

def rightShift(text,n):
    return text[-n:] + text[:-n]

def setDistanceColor(distanceMatrix):
    for row in range(SIZE):
        for col in range(SIZE):
            API.setText(row,col,distanceMatrix[row][col])
            API.setColor(row,col,'O')

def updateDistanceGraphic(distanceMatrix):
    for row in range(SIZE):
        for col in range(SIZE):
            API.setText(row,col,distanceMatrix[row][col])


def checkDistanceValue(currentCord,distanceMatrix,wallMatrix, done):
    rotationMap = np.array([[0,1],[1,0],[0,-1],[-1,0]])
    stack = deque()
    x = currentCord[0]
    y = currentCord[1]
    initialCellDistance = distanceMatrix[x][y]
    initialCell = (wallMatrix[x][y], x,y, initialCellDistance)
    stack.append(initialCell)
    if not done:
        while(len( stack )):
            neighbors = []
            cell = stack.pop()
            cellWalls = list(cell[0])
            currentDistance = cell[3]
            neighborDistances = []
            x = cell[1]
            y = cell[2]
            #Get all open neighboring cells
            for i in range(4):
                if(cellWalls[i] == '0'):
                    neighborX = x+rotationMap[i][0]
                    neighborY = y+rotationMap[i][1]
                    #Save cell as wallString,Distance tuple
                    neighborCell = ( wallMatrix[neighborX][neighborY],
                            neighborX, neighborY,
                            distanceMatrix[neighborX][neighborY] )
                    neighbors.append(neighborCell)
            #Validate surrounding neighbors using minimum distance
            if(neighbors):
                if( ((x,y) == (initialCell[1],initialCell[2])) ):
                    filteredNeighbors = neighbors 
                else:
                    filteredNeighbors = [n for n in neighbors if 'xxxx' not in n]
                minimumDistance = min(filteredNeighbors, key=lambda n: n[3])
                minimumDistance = minimumDistance[ 3 ]
                if(currentDistance != 1 + minimumDistance):
                    #log(filteredNeighbors)
                    #log(f"Min: {minimumDistance}, Cur: {currentDistance}")
                    distanceMatrix[x][y] = 1 + minimumDistance
                    for neighbor in neighbors:
                        #log(f"Added {neighbor}")
                        stack.append(neighbor)
                if(x==0 and y==0):
                    break;

    #Finally return open neighbors as possible next cell destination
    cellWalls = initialCell[0]
    x = currentCord[0]
    y = currentCord[1]
    neighbors = []
    for i in range(4):
        if(cellWalls[i] == '0'):
            neighborX = x+rotationMap[i][0]
            neighborY = y+rotationMap[i][1]
            #Save cell as wallString,Distance tuple
            neighborCell = ( wallMatrix[neighborX][neighborY],
                    neighborX, neighborY,
                    distanceMatrix[neighborX][neighborY] )
            neighbors.append(neighborCell)
    return neighbors

def getNextDirection(currentCords,possibleNextDirs,distanceMatrix,done):
    rotationMap = np.array([[0,1],[1,0],[0,-1],[-1,0]])
    neighbors = possibleNextDirs
    nextNeighborCords = (99,99)
    x = currentCords[0]
    y = currentCords[1]
    if(done):
        possibleNextDirs = [n for n in neighbors if 'xxxx' not in n]
        possibleNextDirs = [n for n in possibleNextDirs if n[3] >= distanceMatrix[x][y]]
        possibleNextDirs.sort(key=lambda x:x[3])
        log(f"Possible: {possibleNextDirs}")
    else:
        possibleNextDirs.sort(key=lambda x:x[3])
    for nextDir in possibleNextDirs:
        if(nextDir[0] == 'xxxx' or done):
            nextNeighborCords = (nextDir[1],nextDir[2])
            break
    if(nextNeighborCords == (99,99)):
        nextNeighborCords = (possibleNextDirs[0][1],possibleNextDirs[0][2])
    return nextNeighborCords - currentCords

def turnToDirection(currentDirection, toDirection):
    while( not np.array_equal(currentDirection ,toDirection) ):
        API.turnRight()
        currentDirection = dirFunc(currentDirection,'R')
    return currentDirection

def main():
    if(SIZE == 16):
        distanceMatrix = np.array([
            [14, 13, 12, 11, 10, 9, 8, 7, 7, 8, 9, 10, 11, 12, 13, 14],
            [13, 12, 11, 10, 9,  8, 7, 6, 6, 7, 8, 9,  10, 11, 12, 13],
            [12, 11, 10, 9,  8,  7, 6, 5, 5, 6, 7, 8,  9,  10, 11, 12],
            [11, 10, 9,  8,  7,  6, 5, 4, 4, 5, 6, 7,  8,  9,  10, 11],
            [10, 9,  8,  7,  6,  5, 4, 3, 3, 4, 5, 6,  7,  8,  9,  10],
            [9,  8,  7,  6,  5,  4, 3, 2, 2, 3, 4, 5,  6,  7,  8,  9],
            [8,  7,  6,  5,  4,  3, 2, 1, 1, 2, 3, 4,  5,  6,  7,  8],
            [7,  6,  5,  4,  3,  2, 1, 0, 0, 1, 2, 3,  4,  5,  6,  7],
            [7,  6,  5,  4,  3,  2, 1, 0, 0, 1, 2, 3,  4,  5,  6,  7],
            [8,  7,  6,  5,  4,  3, 2, 1, 1, 2, 3, 4,  5,  6,  7,  8],
            [9,  8,  7,  6,  5,  4, 3, 2, 2, 3, 4, 5,  6,  7,  8,  9],
            [10, 9,  8,  7,  6,  5, 4, 3, 3, 4, 5, 6,  7,  8,  9,  10],
            [11, 10, 9,  8,  7,  6, 5, 4, 4, 5, 6, 7,  8,  9,  10, 11],
            [12, 11, 10, 9,  8,  7, 6, 5, 5, 6, 7, 8,  9,  10, 11, 12],
            [13, 12, 11, 10, 9,  8, 7, 6, 6, 7, 8, 9,  10, 11, 12, 13],
            [14, 13, 12, 11, 10, 9, 8, 7, 7, 8, 9, 10, 11, 12, 13, 14]
            ])
    else:
        distanceMatrix = np.array([
            [6,  5, 4, 3, 3, 4, 5, 6],
            [5,  4, 3, 2, 2, 3, 4, 5],
            [4,  3, 2, 1, 1, 2, 3, 4],
            [3,  2, 1, 0, 0, 1, 2, 3],
            [3,  2, 1, 0, 0, 1, 2, 3],
            [4,  3, 2, 1, 1, 2, 3, 4],
            [5,  4, 3, 2, 2, 3, 4, 5],
            [6,  5, 4, 3, 3, 4, 5, 6]
            ]);
    wallMatrix = np.full((SIZE,SIZE), "xxxx")
    #wallMatrix[:] = 'xxxx' #NorthEastWestSouth bits clock-wise
    direction = np.array([0,1])
    startingCord = np.array([0,0])
    currentCord = startingCord
    size2 = SIZE/2
    goalCords = np.array([
        [size2-1, size2-1],
        [size2-1, size2],
        [size2,   size2-1],
        [size2,   size2]
        ])
    counter = 1;
    log("Running...")
    setDistanceColor(distanceMatrix)
    API.setColor(0, 0, "R")
    for cord in goalCords:
        API.setColor(int(cord[0]),int(cord[1]), 'G')
    done = False
    while not arreq_in_list(currentCord,goalCords):
        log("Current cord: "+str(currentCord))
        wallMatrix[currentCord[0]][currentCord[1]] = updateWallString(
                API.wallFront(),
                API.wallRight(),
                False,
                API.wallLeft(),
                direction
                )
        possibleNextDirs = checkDistanceValue(currentCord, distanceMatrix, wallMatrix,done)
        updateDistanceGraphic(distanceMatrix)
        nextDir = getNextDirection(currentCord, possibleNextDirs,distanceMatrix,done)
        direction = turnToDirection(direction,nextDir)
        API.moveForward()
        #Utilities
        currentCord = currentCord + direction;
        API.setText(currentCord[0], currentCord[1], counter)
        API.setColor(currentCord[0], currentCord[1], 'R')
        log("")
    done = True
    log("Found shortest path!")
    while not np.array_equal(currentCord, startingCord):
        wallMatrix[currentCord[0]][currentCord[1]] = updateWallString(
                API.wallFront(),
                API.wallRight(),
                False,
                API.wallLeft(),
                direction
                )
        log(f"Current cord {currentCord}")
        possibleNextDirs = checkDistanceValue(currentCord, distanceMatrix, wallMatrix,done)
        nextDir = getNextDirection(currentCord, possibleNextDirs,distanceMatrix,done)
        direction = turnToDirection(direction,nextDir)
        currentCord = currentCord + direction;
        API.moveForward()
    
if __name__ == "__main__":
    main()
