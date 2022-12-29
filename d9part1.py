#!/usr/bin/python3

import math
# sudo apt-get install python3-matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import ticker

def plotPoints(headX, headY, tailX, tailY):
#def plotPoints(headX, headY):
    # Used the modulus to place the tick marks on every 10...
    minXGraph = min(headX) - (min(headX) % 10)
    maxXGraph = max(headX) + 2
    minYGraph = min(headY) - (min(headY) % 10)
    maxYGraph = max(headY) + 2
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
    plt.xticks(range(minXGraph, maxXGraph, 1))
    #plt.yticks(range(-12,12))
    plt.yticks(range(minYGraph, maxYGraph, 1))
    plt.grid()
    # Head of Rope Coords
    plt.plot(headX, headY, marker="o", markersize=1, color='green', label='ropeHead')
    # Tail of Rope Coords
    #tailX = [0, -240]
    #tailY = [0, 80]
    plt.plot(tailX, tailY, marker="o", markersize=1, color='blue', label='ropeTail', linestyle='dashed')
    #plt.plot(tailX, tailY, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
    plt.legend()
    plt.show()

def headAppendCoords(x, y):
    global headRopeCoordsList
    coords = str(x) + "," + str(y)
    headRopeCoordsList.append(coords)

def tailAppendCoords(x, y):
    global tailRopeCoordsList
    coords = str(x) + "," + str(y)
    tailRopeCoordsList.append(coords)

def calcMovementRope():
    #fileName = "sample.txt"
    fileName = "input.txt"
    f = open(fileName).readlines()
    listDirections = []
    for line in f:
        info = line.strip()
        listDirections.append(info)
    # Starting coordinates are (1,1) of the rope for head and tail...
    startX = 1
    startY = 1
    headAppendCoords(startX, startY)
    tailAppendCoords(startX, startY)
    currentRopeX = startX
    currentRopeY = startY
    for d in listDirections:
        #print("Directions: " + d)
        match d.split():
            case ["R", spaces]:
                #print(spaces)
                for x in range(0,int(spaces)):
                    # Increment x of the coordinates --> x axis...
                    currentRopeX += 1
                    headAppendCoords(currentRopeX, currentRopeY)
                    calcMovementTail(currentRopeX, currentRopeY)
            case ["L", spaces]:
                #print(spaces)
                for x in range(0,int(spaces)):
                    # Decrease x of the coordinates <-- x axis...
                    currentRopeX -= 1
                    headAppendCoords(currentRopeX, currentRopeY)
                    calcMovementTail(currentRopeX, currentRopeY)
            case ["U", spaces]:
                #print(spaces)
                for y in range(0,int(spaces)):
                    # Increase y of the coordinates ^ Y axis...
                    currentRopeY += 1
                    headAppendCoords(currentRopeX, currentRopeY)
                    calcMovementTail(currentRopeX, currentRopeY)
            case ["D", spaces]:
                #print(spaces)
                for y in range(0,int(spaces)):
                    # Increase y of the coordinates ^ Y axis...
                    currentRopeY -= 1
                    headAppendCoords(currentRopeX, currentRopeY)
                    calcMovementTail(currentRopeX, currentRopeY)
        

def calcMovementTail(cX, cY):
    global headRopeCoordsList
    global tailRopeCoordsList
    if len(tailRopeCoordsList) > 1:
        # Pull the last tail coordinates from the list
        tailLastX, tailLastY = tailRopeCoordsList[-1].split(",")
        tailLastX = int(tailLastX)
        tailLastY = int(tailLastY)
        # Head coordinates were already recorded pull the 2nd to last
        headLastX, headLastY = headRopeCoordsList[-2].split(",")
        headLastX = int(headLastX)
        headLastY = int(headLastY)
        #print("Tail Last Coordinates: " + str(tailLastX) + ", " + str(tailLastY))
        #print("Head Last Coordinates: " + str(headLastX) + ", " + str(headLastY))
        #print("Current Head Coordinates: " + str(cX) + ", " + str(cY))
        distanceBetweenPoints = math.dist([cX, cY], [tailLastX, tailLastY])
        #print("Distance between points: " + str(distanceBetweenPoints))
        #print("--")
        if distanceBetweenPoints >= 2:
            tailAppendCoords(headLastX, headLastY)
        elif distanceBetweenPoints < 2:
            tailAppendCoords(tailLastX, tailLastY)
    else:
        #print("1st Tail Coorindates Recorded")
        # On first move the tail does not move from teh start (1,1) coords
        tailAppendCoords(1, 1)

def headSplitCoords():
    global headRopeCoordsList
    listX = []
    listY = []
    for item in headRopeCoordsList:
        i = item.split(",")
        listX.append(int(i[0]))
        listY.append(int(i[1]))
    return listX, listY

def tailSplitCoords():
    global tailRopeCoordsList
    listX = []
    listY = []
    for item in tailRopeCoordsList:
        i = item.split(",")
        # Adding an offset of the lines to see the rope head and tail following a similar path
        listX.append((float(i[0])+0.1))
        listY.append((float(i[1])+0.1))
    return listX, listY

def main():
    global headRopeCoordsList 
    headRopeCoordsList = []
    headRopeCoordsX = []
    headRopeCoordsY = []
    global tailRopeCoordsList
    tailRopeCoordsList = []
    tailRopeCoordsX = []
    tailRopeCoordsY = []
    calcMovementRope()
    headRopeCoordsX, headRopeCoordsY = headSplitCoords()
    tailRopeCoordsX, tailRopeCoordsY = tailSplitCoords()
    #print(headRopeCoordsList)
    # Moved the plotting of the points until after the calculation of Coordinates...
    #plotPoints(headRopeCoordsX, headRopeCoordsY, tailRopeCoordsX, tailRopeCoordsY)
    # Part 1
    # Identify the coordinates where the tail visited at least once
    # print(tailRopeCoordsList)
    #print(len(tailRopeCoordsList))
    # Deduplicate the list
    tailRopeCoordsList = list(dict.fromkeys(tailRopeCoordsList))
    # Print the number of coordinates where the tail visited at least once
    #print(tailRopeCoordsList)
    print("Coordinates the Tail Visited at Least Once: " + str(len(tailRopeCoordsList)))
    plotPoints(headRopeCoordsX, headRopeCoordsY, tailRopeCoordsX, tailRopeCoordsY)


if __name__ == '__main__':
    main()



