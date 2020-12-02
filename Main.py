import API
import sys
import numpy as np


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def dirFunc(direction,turnDir):
#    [0,  1]
#    [1,  0]
#    [0, -1]
#   [-1,  0]
    rotationMap = np.array([[0,1],[1,0],[0,-1],[-1,0]])
    pos = np.where(rotationMap == direction)
    if turnDir == 'R':
        return rotationMap[ ( pos[0][1] + 1 ) % 4 ]
    elif turnDir == 'L':
        return rotationMap[ ( pos[0][1] - 1 ) % 4 ]

def arreq_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)

def main():
    matrix = np.ones((16,16))*5
    direction = np.array([0,1])
    currentCord = np.array([0,0])
    goalCords = np.array([[6,6],[6,7],[7,6],[7,7]])
    counter = 0;
    log("Running...")
    API.setColor(0, 0, "G")
    while not arreq_in_list(currentCord,goalCords):
        if not API.wallRight():
            API.turnRight()
            direction = dirFunc(direction,'R')
        while API.wallFront():
            API.turnLeft()
            direction = dirFunc(direction,'L')
        API.moveForward()
        currentCord = currentCord + direction;
        matrix[currentCord[0]][currentCord[1]] = counter
        API.setText(currentCord[0], currentCord[1], counter)
        counter = counter + 1
        log(currentCord)


if __name__ == "__main__":
    main()

