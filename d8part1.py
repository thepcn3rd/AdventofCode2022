#!/usr/bin/python3 

import os
import sqlite3
import shutil

class colors:
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'

    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2  = '\33[96m'
    CWHITE2  = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'

def createDB():
    # To create the database in memory use :memory:
    #dbFile = ":memory:"
    dbFile = "my.db"
    if not os.path.exists(dbFile):
        os.close(os.open(dbFile, os.O_CREAT))
    else:
        # Remove and recreate the database each execution...
        shutil.copyfile('my.db','backup.db')
        os.remove(dbFile)
        os.close(os.open(dbFile, os.O_CREAT))
    db = sqlite3.connect(dbFile)
    cursor = db.cursor()
    return db, cursor

def createTable(db, c):
    # Create the database
    
    # uniqueID for element in DB - 1
    tableName = "treeHouse"
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + tableName + "'")
    if c.fetchone()[0]==1:
        print("\nTable '" + tableName + "' exists, skipping the creation...\n")
    else:
        sql = "CREATE TABLE " + tableName + " ("
        sql += "uniqueID INTEGER PRIMARY KEY AUTOINCREMENT, "   # UniqueID of the element whether a file or a folder
        sql += "colX INTEGER, "                 # colX - X Coordinates
        sql += "rowY INTEGER, "                 # colY - Y Coodrindates
        sql += "heightTree INTEGER, "           # heightTree - Height of Tree 
        sql += "visibleNorth VARCHAR(5), "      # Is visible to the border from the north
        sql += "visibleSouth VARCHAR(5), "      # Is visible to the border from the south
        sql += "visibleEast VARCHAR(5), "       # Is visible to the border from the east
        sql += "visibleWest VARCHAR(5), "       # Is visible to the border from the west
        sql += "visibleAll VARCHAR(5))"        # Is visible from all directions
        c.execute(sql)
        # Insert root directory...
        #c.execute("INSERT INTO fileSystem (name, type, parentID, size) VALUES ('root', 'Folder', 1, 0)")
        #db.commit()

# Polpulate the database of what we know...
def populateDatabase(fName, db, cur):
    f = open(fName).readlines()
    rowY = 0    # y coordinate
    minY = 0
    maxY = 0    # Need to discover the max Y
    colX = 0    # x coordinate (starts at 0,0)
    minX = 0
    maxX = 0    # Need to discover the max X
    lookNorth = lookSouth = lookEast = lookWest = lookAll = "Undetermined"  # lookEast = Look Right
    listInserts = []
    for line in f:
        info = line.strip()
        for height in info:
            #print("X:" + str(colX) + " Y:" + str(rowY) + " Value: " + str(height))
            tupleInsert = (colX, rowY, height, lookNorth, lookSouth, lookEast, lookWest, lookAll)
            listInserts.append(tupleInsert)
            colX += 1
        if maxX == 0: maxX = colX
        colX = 0    # Reset to 0 for x when y advances... 
        rowY+=1
    if maxY == 0: maxY = rowY
    # Insert the rows into the database
    cur.executemany("INSERT INTO treeHouse (colX, rowY, heightTree, visibleNorth, visibleSouth, visibleEast, visibleWest, visibleAll) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", listInserts)
    db.commit()
    # The numbers are decreased by 1 to find the actual max...  
    # This is due to the count being placed after the max is calculated
    return (maxX-1), (maxY-1)

def updateVisibility(direction, uID, db, cur):
    sql = "UPDATE treeHouse SET " + direction + "='Visible' WHERE uniqueID=" + str(uID)
    db.execute(sql)
    db.commit()

def updateHidden(direction, uID, db, cur):
    sql = "UPDATE treeHouse SET " + direction + "='Hidden' WHERE uniqueID=" + str(uID)
    db.execute(sql)
    db.commit()

def checkNeighborHeight(nX, nY, db, cur):
    sql = "SELECT heightTree FROM treeHouse WHERE colX=" + str(nX) + " AND rowY=" + str(nY)
    #print(sql)
    results = db.execute(sql)
    for row in results:
        heightNeighborTree = row[0]
    #print("Neighbor (" + str(nX) + ", " + str(nY) + ") - Height: " + str(heightNeighborTree))
    return heightNeighborTree

def determineVisibility(maxX, maxY, db, cur):
    for x in range(0, maxX+1):
        for y in range(0, maxY+1):
            print("\n-- Checking (" + str(x) + "," + str(y) + ")")
            # Lookup the height of the tree
            sql = "SELECT uniqueID, heightTree FROM treeHouse WHERE colX=" + str(x) + " AND rowY=" + str(y)
            #print(sql)
            results = db.execute(sql)
            for row in results:
                uniqueID = row[0]
                heightTree = row[1]
            rowY = y
            minY = 0
            #maxY 
            colX = x
            minX = 0
            lookNorth = lookSouth = lookEast = lookWest = lookAll = "Undetermined"
            # If coordinates are the edge, change undetermined to Visible
            # Check Visibility to the North
            if y == minY:
                lookNorth = "Visible"
                updateVisibility("visibleNorth", uniqueID, db, cur)
            if x == minX:
                lookWest = "Visible"
                updateVisibility("visibleWest", uniqueID, db, cur)
            if y == maxY:
                lookSouth = "Visible"
                updateVisibility("visibleSouth", uniqueID, db, cur)
            if x == maxX:
                lookEast = "Visible"
                updateVisibility("visibleEast", uniqueID, db, cur)
            ### Check visibility to the North to the border
            # Example (0,1) will have a neighbor of (0,0) to the North
            maxNeighborHeight = 0
            for neighborY in range(y-1, minY-1, -1):
                #print("Checking neighbor: (" + str(x) + "," + str(neighborY) + ")")
                neighborTreeHeight = checkNeighborHeight(x, neighborY, db, cur)
                if neighborTreeHeight > maxNeighborHeight:
                    maxNeighborHeight = neighborTreeHeight
                if maxNeighborHeight == 9: break
                #print(maxNeighborHeight)
            if heightTree > maxNeighborHeight:
                updateVisibility("visibleNorth", uniqueID, db, cur)
            if heightTree <= maxNeighborHeight and y != minY and y != maxY:
                #print("UID: " + str(uniqueID) + " Hidden to the North")
                updateHidden("visibleNorth", uniqueID, db, cur)
            ### Check visibility to the South to the border
            maxNeighborHeight = 0
            for neighborY in range(y+1, maxY+1):
                #print("Checking neighbor: (" + str(x) + "," + str(neighborY) + ")")
                neighborTreeHeight = checkNeighborHeight(x, neighborY, db, cur)
                if neighborTreeHeight > maxNeighborHeight:
                    maxNeighborHeight = neighborTreeHeight
                if maxNeighborHeight == 9: break
                #print(maxNeighborHeight)
            if heightTree > maxNeighborHeight:
                updateVisibility("visibleSouth", uniqueID, db, cur)
            if heightTree <= maxNeighborHeight and y != minY and y != maxY:
                #print("UID: " + str(uniqueID) + " Hidden to the North")
                updateHidden("visibleSouth", uniqueID, db, cur)
            ### Check visibility to the East to the border
            maxNeighborHeight = 0
            for neighborX in range(x+1, maxX+1):
                #print("Checking neighbor: (" + str(neighborX) + "," + str(y) + ")")
                neighborTreeHeight = checkNeighborHeight(neighborX, y, db, cur)
                if neighborTreeHeight > maxNeighborHeight:
                    maxNeighborHeight = neighborTreeHeight
                if maxNeighborHeight == 9: break
                #print(maxNeighborHeight)
            if heightTree > maxNeighborHeight:
                updateVisibility("visibleEast", uniqueID, db, cur)
            if heightTree <= maxNeighborHeight and x != minX and x != maxX:
                #print("UID: " + str(uniqueID) + " Hidden to the North")
                updateHidden("visibleEast", uniqueID, db, cur)
            ### Check visibility to the West to the border
            maxNeighborHeight = 0
            for neighborX in range(x-1, minX-1, -1):
                #print("Checking neighbor: (" + str(neighborX) + "," + str(y) + ")")
                neighborTreeHeight = checkNeighborHeight(neighborX, y, db, cur)
                if neighborTreeHeight > maxNeighborHeight:
                    maxNeighborHeight = neighborTreeHeight
                #print(maxNeighborHeight)
                if maxNeighborHeight == 9: break
            if heightTree > maxNeighborHeight:
                updateVisibility("visibleWest", uniqueID, db, cur)
            if heightTree <= maxNeighborHeight and x != minX and x != maxX:
                #print("UID: " + str(uniqueID) + " Hidden to the North")
                updateHidden("visibleWest", uniqueID, db, cur)
            
def outputGrid(maxX, maxY, db, cur):
    # Update the records to show whcih ones are visibleAll='Hidden' from all directions
    sql = "SELECT uniqueID FROM treeHouse WHERE visibleNorth='Hidden' AND visibleSouth='Hidden' AND visibleEast='Hidden' AND visibleWest='Hidden'"
    #print(sql)
    results = db.execute(sql)
    listID = []
    for row in results:
        listID.append(row[0])
    #print(listID)
    for uID in listID:
        sqlUpdate = "UPDATE treeHouse SET visibleAll='Hidden' WHERE uniqueID=" + str(uID)
        db.execute(sqlUpdate)
        db.commit()
    # Output to a text file the grid with an H highlighting the Hidden trees to verify
    outputFile = open("output.grid", "w")
    outputString = ""
    hiddenTreeCoordinates = ""
    for rowY in range(0, maxY+1):
        for colX in range(0, maxX+1):
            sql = "SELECT heightTree, visibleAll FROM treeHouse WHERE colX=" + str(colX) + " AND rowY=" + str(rowY)
            #print(sql)
            results = db.execute(sql)
            for row in results:
                if row[1] == 'Hidden':
                    outputString += colors.CBLUE + "H" + colors.CEND
                    hiddenTreeCoordinates += "(" + str(colX) + "," + str(rowY) + ") "
                    #print(outputString)
                else:
                    outputString += str(row[0])
        print(outputString)
        outputFile.write(outputString + "\n")
        outputString = ""
    outputFile.write("\n\n")
    outputFile.write("Hidden Tree Coordinates:\n")
    outputFile.write(hiddenTreeCoordinates)
    outputFile.close()
    print("\n\n" + hiddenTreeCoordinates)
                



def main():
    dbConnection, dbCursor = createDB()
    createTable(dbConnection, dbCursor)
    #fileName = "sample.txt"
    fileName = "input.txt"
    maximumX = 0
    maximumX = 98
    maximumY = 0
    maximumY = 98
    # Populate the database...
    maximumX, maximumY = populateDatabase(fileName, dbConnection, dbCursor)
    # Determine Visibility
    determineVisibility(maximumX, maximumY, dbConnection, dbCursor)
    print("Max X: " + str(maximumX) + " Max Y: " + str(maximumY))
    # Output Total Trees accounted for minus the hidden ones...
    sql = "SELECT count(*) FROM treeHouse"
    results = dbConnection.execute(sql)
    for row in results:
        totalTrees = row[0]
    sqlHidden = "SELECT count(*) FROM treeHouse WHERE visibleNorth='Hidden' AND visibleSouth='Hidden' AND visibleEast='Hidden' AND visibleWest='Hidden'"
    results = dbConnection.execute(sqlHidden)
    for row in results:
        hiddenTrees = row[0]
    print("Total Trees: " + str(totalTrees) + " Hidden Trees: " + str(hiddenTrees) + " Visible Trees: " + str(totalTrees-hiddenTrees))
    # Output Hidden Trees diagram
    outputGrid(maximumX, maximumY, dbConnection, dbCursor)
    dbConnection.close()




if __name__ == '__main__':
    main()