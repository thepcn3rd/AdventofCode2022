#!/usr/bin/python3

import math
import numpy
# sudo apt-get install python3-matplotlib
from matplotlib import pyplot as plt

def plotPoints(headX, headY, tX, tY, t2X, t2Y, t3X, t3Y, t4X, t4Y, t5X, t5Y, t6X, t6Y, t7X, t7Y, t8X, t8Y, t9X, t9Y):
    # Used the modulus to place the tick marks on every 10...
    minXGraph = int(min(headX) - (min(headX) % 10))
    maxXGraph = int(max(headX) + 2)
    minYGraph = int(min(headY) - (min(headY) % 10))
    maxYGraph = int(max(headY) + 2)
    # Size of the Figure shown on the Monitor
    plt.rcParams["figure.figsize"] = [6, 6]
    plt.rcParams["figure.autolayout"] = True
    # Set the minX, maxX on the graph
    plt.xlim(minXGraph, maxXGraph)
    # Set the minY, maxY on the graph
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
    plt.xticks(range(minXGraph, maxXGraph, 10))
    plt.yticks(range(minYGraph, maxYGraph, 10))
    plt.grid()
    # Head of Rope Coords
    plt.plot(headX, headY, marker="o", markersize=1, color='green', label='ropeHead')
    # Tail of Rope Coords
    plt.plot(tX, tY, marker="o", markersize=1, color='blue', label='ropeTail', linestyle='dashed')
    plt.plot(t2X, t2Y, marker="o", markersize=1, color='yellow', label='rope2Tail', linestyle='dotted')
    plt.plot(t3X, t3Y, marker="o", markersize=1, color='yellow', label='rope3Tail', linestyle='dotted')
    plt.plot(t4X, t4Y, marker="o", markersize=1, color='yellow', label='rope4Tail', linestyle='dotted')
    plt.plot(t5X, t5Y, marker="o", markersize=1, color='yellow', label='rope5Tail', linestyle='dotted')
    plt.plot(t6X, t6Y, marker="o", markersize=1, color='yellow', label='rope6Tail', linestyle='dotted')
    plt.plot(t7X, t7Y, marker="o", markersize=1, color='yellow', label='rope7Tail', linestyle='dotted')
    plt.plot(t8X, t8Y, marker="o", markersize=1, color='yellow', label='rope8Tail', linestyle='dotted')
    plt.plot(t9X, t9Y, marker="o", markersize=1, color='red', label='rope9Tail', linestyle='dotted')
    plt.legend()
    plt.show()

def headAppendCoords(x, y):
    global headRopeCoordsList
    coords = str(x) + "," + str(y)
    headRopeCoordsList.append(coords)

def tailAppendCoordsXY(x, y, tailList):
    coords = str(x) + "," + str(y)
    tailList.append(coords)

def calcMovementRope(fName, sCoords):
    listDirections = open(fName).readlines()
    # Starting coordinates are sCoords of the rope for head and tail...
    currentRopeX, currentRopeY = int(sCoords.split(",")[0]), int(sCoords.split(",")[1])
    for d in listDirections:
        print("\n\nDirections: " + d)
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

def moveTail(tail1, tail2, a, b):
    # Evaluated the code at https://github.com/markusschanta/advent-of-code-2022/blob/main/2022/09/day.09.ipynb
    # To understand the algorithm that needed to be executed to move the tail...
    print("-" + str(a) + "-")
    # Pull the current Tail 1 Coorindates
    headKnotX, headKnotY = tail1[-1].split(",")
    headKnotX = int(headKnotX)
    headKnotY = int(headKnotY)
    # Pull the last Tail 2 Coorindates
    tailKnotX, tailKnotY = tail2[-1].split(",")
    tailKnotX = int(tailKnotX)
    tailKnotY = int(tailKnotY)
    # Measure Distance Tail 1 to Tail 2
    print("Current Tail " + str(a) + " Coordinates: " + str(headKnotX) + ", " + str(headKnotY))
    print("Tail " + str(b) + " Last Coordinates: " + str(tailKnotX) + ", " + str(tailKnotY))
    
    distX = headKnotX - tailKnotX
    distY = headKnotY - tailKnotY
    if (abs(distX) >= 2) or (abs(distY) >= 2):
        coordsX = tailKnotX + numpy.sign(distX)
        coordsY = tailKnotY + numpy.sign(distY)
        tailAppendCoordsXY(coordsX, coordsY, tail2)
        print("Tail " + str(b) + " New Coordinates: " + str(coordsX) + ", " + str(coordsY))
    else:
        coordsX = tailKnotX
        coordsY = tailKnotY
        print("Tail " + str(b) + " New Coordinates: " + str(coordsX) + ", " + str(coordsY))

def calcMovementTail(cX, cY):
    global headRopeCoordsList
    global tailRopeCoordsList, tail2RopeCoordsList, tail3RopeCoordsList, tail4RopeCoordsList, tail5RopeCoordsList, tail6RopeCoordsList, tail7RopeCoordsList, tail8RopeCoordsList, tail9RopeCoordsList
    tailAllRopeCoordsList = [tailRopeCoordsList, tail2RopeCoordsList, tail3RopeCoordsList, tail4RopeCoordsList, tail5RopeCoordsList, tail6RopeCoordsList, tail7RopeCoordsList, tail8RopeCoordsList, tail9RopeCoordsList]
    print("--")
    # Head coordinates were already recorded pull the 2nd to last
    headLastX, headLastY = headRopeCoordsList[-2].split(",")
    headLastX = int(headLastX)
    headLastY = int(headLastY)
    # Pull Tail 1 Last Coords
    tailLastX, tailLastY = tailRopeCoordsList[-1].split(",")
    tailLastX = int(tailLastX)
    tailLastY = int(tailLastY)
    # Measure Distance Current Location to Tail 1
    print("Current Head Coordinates: " + str(cX) + ", " + str(cY))
    print("Head Last Coordinates: " + str(headLastX) + ", " + str(headLastY))
    print("Tail Last Coordinates: " + str(tailLastX) + ", " + str(tailLastY))
    distanceBetweenPoints = math.dist([cX, cY], [tailLastX, tailLastY])
    print("Distance between points H and T1: " + str(distanceBetweenPoints))
    # Append Coordinates to List
    if distanceBetweenPoints >= 2:
        tailAppendCoordsXY(headLastX, headLastY, tailRopeCoordsList)
    elif distanceBetweenPoints < 2:
        tailAppendCoordsXY(tailLastX, tailLastY, tailRopeCoordsList)
    # Move the tail respectively...
    for l in range(0, (len(tailAllRopeCoordsList)-1)):
        moveTail(tailAllRopeCoordsList[l], tailAllRopeCoordsList[l+1], l, l+1)

def splitCoords(tailList, n):
    listX = []
    listY = []
    for item in tailList:
        i = item.split(",")
        # Adding an offset of the lines to see the rope head and tail following a similar path
        listX.append((float(i[0])+(0.1*n)))
        listY.append((float(i[1])+(0.1*n)))
    return listX, listY

def main():
    # Setup the coordinates to start at (1,1)
    startCoords = '1,1'
    global headRopeCoordsList 
    headRopeCoordsList = [startCoords]
    headRopeCoordsX = headRopeCoordsY = []
    global tailRopeCoordsList, tail2RopeCoordsList, tail3RopeCoordsList
    tailRopeCoordsList = [startCoords]
    tail2RopeCoordsList = [startCoords]
    tail3RopeCoordsList = [startCoords]
    tailRopeCoordsX = tail2RopeCoordsX = tail3RopeCoordsX = []
    tailRopeCoordsY = tail2RopeCoordsY = tail3RopeCoordsY = []
    global tail4RopeCoordsList, tail5RopeCoordsList, tail6RopeCoordsList
    tail4RopeCoordsList = [startCoords] 
    tail5RopeCoordsList = [startCoords]
    tail6RopeCoordsList = [startCoords]
    tail4RopeCoordsX = tail5RopeCoordsX = tail6RopeCoordsX = []
    tail4RopeCoordsY = tail5RopeCoordsY = tail6RopeCoordsY = []
    global tail7RopeCoordsList, tail8RopeCoordsList, tail9RopeCoordsList
    tail7RopeCoordsList = [startCoords]
    tail8RopeCoordsList = [startCoords]
    tail9RopeCoordsList = [startCoords]
    tail7RopeCoordsX = tail8RopeCoordsX = tail9RopeCoordsX = []
    tail7RopeCoordsY = tail8RopeCoordsY = tail9RopeCoordsY = []
    
    #fileName = "sample.txt"
    #fileName = "sample2.txt"
    fileName = "input.txt"
    calcMovementRope(fileName, startCoords)

    headRopeCoordsX, headRopeCoordsY = splitCoords(headRopeCoordsList, 0)
    tailRopeCoordsX, tailRopeCoordsY = splitCoords(tailRopeCoordsList, 1)
    tail2RopeCoordsX, tail2RopeCoordsY = splitCoords(tail2RopeCoordsList, 2)
    tail3RopeCoordsX, tail3RopeCoordsY = splitCoords(tail3RopeCoordsList, 3)
    tail4RopeCoordsX, tail4RopeCoordsY = splitCoords(tail4RopeCoordsList, 4)
    tail5RopeCoordsX, tail5RopeCoordsY = splitCoords(tail5RopeCoordsList, 5)
    tail6RopeCoordsX, tail6RopeCoordsY = splitCoords(tail6RopeCoordsList, 6)
    tail7RopeCoordsX, tail7RopeCoordsY = splitCoords(tail7RopeCoordsList, 7)
    tail8RopeCoordsX, tail8RopeCoordsY = splitCoords(tail8RopeCoordsList, 8)
    tail9RopeCoordsX, tail9RopeCoordsY = splitCoords(tail9RopeCoordsList, 9)
        
    ### Part 1
    # Identify the coordinates where the tail visited at least once
    # Deduplicate the list
    tailRopeCoordsList = list(dict.fromkeys(tailRopeCoordsList))
    # Print the number of coordinates where the tail visited at least once
    print("Coordinates the Tail Visited at Least Once for Part 1: " + str(len(tailRopeCoordsList)))

    ### Part 2
    tail9RopeCoordsList = list(dict.fromkeys(tail9RopeCoordsList))
    print("Coordinates Tail 9 Visited at Least Once for Part 2: " + str(len(tail9RopeCoordsList)))
    plotPoints(headRopeCoordsX, headRopeCoordsY, tailRopeCoordsX, tailRopeCoordsY, tail2RopeCoordsX, tail2RopeCoordsY, tail3RopeCoordsX, tail3RopeCoordsY, tail4RopeCoordsX, tail4RopeCoordsY, tail5RopeCoordsX, tail5RopeCoordsY, tail6RopeCoordsX, tail6RopeCoordsY, tail7RopeCoordsX, tail7RopeCoordsY, tail8RopeCoordsX, tail8RopeCoordsY, tail9RopeCoordsX, tail9RopeCoordsY)


if __name__ == '__main__':
    main()
