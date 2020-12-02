import API
import sys
import numpy as np
import math 


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
    log(string)
    if( np.array_equal(direction,[0,1]) ):
        return string;
    elif( np.array_equal(direction,[1,0]) ):
        return leftShift(string,1)
    elif( np.array_equal(direction,[0,-1]) ):
        return leftShift(string,2)
    elif( np.array_equal(direction,[-1,0]) ):
        return rightShift(string,1)

def leftShift(text,n):
    return text[n:] + text[:n]

def rightShift(text,n):
    return text[-n:] + text[:-n]

def updateDistanceGraphic(distanceMatrix):
    for row in range(16):
        for col in range(16):
            API.setText(row,col,distanceMatrix[row][col])
            API.setColor(row,col,'O')


def updateDistanceValue(currentCord,distanceMatrix,wallMatrix):
    rotationMap = np.array([[0,1],[1,0],[0,-1],[-1,0]])
    stack = []
    x = currentCord[0]
    y = currentCord[1]
    currentDistance = distanceMatrix[x][y]
    currentCell = (wallMatrix[x][y], currentDistance)
    stack.push(currentCell)
    while(not stack.empty()):
        cell = stack.pop()
        cellWalls = list(cell[0])
        #Get all open neighboring cells
        for i in range(4):
            if(cellWalls[i] == 0):
                neighborX = x+rotationMap[0]
                neighborY = y+rotationMap[1]
                #Save cell as wallString,Distance tuple
                neighborCell = ( wallMatrix[neighborX][neighborY], 
                        distanceMatrix[neighborX][neighborY] )
                neighbors.append(neighborCell)
        minimumDistance = min(neighbors, lambda n: n[1])
        if(currentDistance != 1 + minimumDistance):
            distanceMatrix[x][y] = 1 + minimumDistance
            for neighbor in neighbors:
                stack.push(neighbor)

def main():
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
    wallMatrix = np.chararray((16,16))
    wallMatrix[:] = 'xxxx' #NorthEastWestSouth bits clock-wise
    direction = np.array([0,1])
    currentCord = np.array([0,0])
    goalCords = np.array([[6,6],[6,7],[7,6],[7,7]])
    counter = 1;
    log("Running...")
    updateDistanceGraphic(distanceMatrix)
    API.setColor(0, 0, "R")
    API.setColor(8, 8, "G")
    API.setColor(7, 7, "G")
    API.setColor(8, 7, "G")
    API.setColor(7, 8, "G")

    while not arreq_in_list(currentCord,goalCords):
        if not API.wallRight():
            API.turnRight()
            direction = dirFunc(direction,'R')
        while API.wallFront():
            API.turnLeft()
            direction = dirFunc(direction,'L')
        API.moveForward()
        wallMatrix[currentCord[0]][currentCord[1]] = updateWallString(
                API.wallFront(),
                API.wallRight(),
                False,
                API.wallLeft(),
                direction
                )
        #Utilities
        currentCord = currentCord + direction;
        distanceMatrix[currentCord[0]][currentCord[1]] = counter
        API.setText(currentCord[0], currentCord[1], counter)
        API.setColor(currentCord[0], currentCord[1], 'C')
        counter = counter + 1
        log(currentCord)


if __name__ == "__main__":
    main()

