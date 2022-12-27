#!/usr/bin/python3

# sudo apt-get install python3-matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import ticker

#def plotPoints(headX, headY, tailX, tailY):
def plotPoints(headX, headY):
    # Used the modulus to place the tick marks on every 10...
    minXGraph = min(headX) - (min(headX) % 10)
    maxXGraph = max(headX)
    minYGraph = min(headY) - (min(headY) % 10)
    maxYGraph = max(headY)
    # Size of the Figure shown on the Monitor
    plt.rcParams["figure.figsize"] = [6, 6]
    plt.rcParams["figure.autolayout"] = True
    # Set the minX, maxX on the graph
    #plt.xlim(-12,13)
    plt.xlim(minXGraph, maxXGraph)
    # Set the minY, maxY on the graph
    #plt.ylim(-12,13)
    plt.ylim(minYGraph, maxYGraph)
    # Set horizontal and vertical lines at x=0 and y=0
    plt.axvline(0, c="black", ls="--")
    plt.axhline(0, c="black", ls="--")
    # Set Title
    plt.title("Day 9 - Advent of Cyber 2022")
    # Label the X axis
    plt.xlabel("X axis")
    # Label the Y axis
    plt.ylabel("Y axis")
    #plt.xticks(range(-12,12))
    plt.xticks(range(minXGraph, maxXGraph, 10))
    #plt.yticks(range(-12,12))
    plt.yticks(range(minYGraph, maxYGraph, 10))
    plt.grid()
    # Head of Rope Coords
    plt.plot(headX, headY, marker="o", markersize=1, color='green', label='ropeHead')
    # Tail of Rope Coords
    #tailX = [0, -240]
    #tailY = [0, 80]
    #plt.plot(tailX, tailY, marker="o", markersize=1, color='blue', label='ropeTail', linestyle='dashed')
    #plt.plot(tailX, tailY, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
    plt.show()

def appendCoords(x, y):
    global headRopeCoordsList
    coords = str(x) + "," + str(y)
    headRopeCoordsList.append(coords)

def calcMovementRope():
    #fileName = "sample.txt"
    fileName = "input.txt"
    f = open(fileName).readlines()
    listDirections = []
    for line in f:
        info = line.strip()
        listDirections.append(info)
    # Starting coordinates are (1,1) of the rope...
    startX = 1
    startY = 1
    appendCoords(startX, startY)
    currentRopeX = startX
    currentRopeY = startY
    for d in listDirections:
        match d.split():
            case ["R", spaces]:
                #print(spaces)
                for x in range(0,int(spaces)):
                    # Increment x of the coordinates --> x axis...
                    currentRopeX += 1
                    appendCoords(currentRopeX, currentRopeY)
            case ["L", spaces]:
                #print(spaces)
                for x in range(0,int(spaces)):
                    # Decrease x of the coordinates <-- x axis...
                    currentRopeX -= 1
                    appendCoords(currentRopeX, currentRopeY)
            case ["U", spaces]:
                #print(spaces)
                for y in range(0,int(spaces)):
                    # Increase y of the coordinates ^ Y axis...
                    currentRopeY += 1
                    appendCoords(currentRopeX, currentRopeY)
            case ["D", spaces]:
                #print(spaces)
                for y in range(0,int(spaces)):
                    # Increase y of the coordinates ^ Y axis...
                    currentRopeY -= 1
                    appendCoords(currentRopeX, currentRopeY)

def splitCoords():
    global headRopeCoordsList
    listX = []
    listY = []
    for item in headRopeCoordsList:
        i = item.split(",")
        listX.append(int(i[0]))
        listY.append(int(i[1]))
    return listX, listY

def main():
    global headRopeCoordsList 
    headRopeCoordsList = []
    headRopeCoordsX = []
    headRopeCoordsY = []
    tailRopeCoordsList = []
    calcMovementRope()
    headRopeCoordsX, headRopeCoordsY = splitCoords()
    #print(headRopeCoordsList)
    plotPoints(headRopeCoordsX, headRopeCoordsY)



if __name__ == '__main__':
    main()



