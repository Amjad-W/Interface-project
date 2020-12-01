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


def main():
    matrix = np.ones((16,16))*5
    direction = np.array([0,1])
    currentCord = np.array([0,0])
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    while True:
        if not API.wallLeft():
            API.turnLeft()
            direction = dirFunc(direction,'L')
        while API.wallFront():
            API.turnRight()
            direction = dirFunc(direction,'R')
        API.moveForward()
        currentCord = currentCord + direction;
        log(currentCord)

if __name__ == "__main__":
    main()

