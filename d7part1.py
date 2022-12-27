#!/usr/bin/python3

import os
import json
import sqlite3

def createDB():
    # To create the database in memory use :memory:
    #dbFile = ":memory:"
    dbFile = "my.db"
    if not os.path.exists(dbFile):
        os.close(os.open(dbFile, os.O_CREAT))
    db = sqlite3.connect(dbFile)
    c = db.cursor()
    # Create the database
    # Table - fileSystem
    # 
    # uniqueID for element in DB - 1
    # name of element in DB      - root equivalent to /
    # type                       - Folder, File
    # parentID                   - For a folder it is the parent folder, for a file it is the folder it is in
    # size                       - For a folder this is 0, For a file this is provided
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fileSystem'")
    if c.fetchone()[0]==1:
        print("\nTable 'fileSystem' exists, skipping the creation...\n")
    else:
        c.execute("CREATE TABLE fileSystem (uniqueID INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(40), type VARCHAR(10), parentID INTEGER, size INTEGER, sizeContents INTEGER DEFAULT 0, childFolders VARCHAR(50), allDependentFolders VARCHAR(100), allDependentFoldersSize INTEGER)")
        # Insert root directory...
        c.execute("INSERT INTO fileSystem (name, type, parentID, size) VALUES ('root', 'Folder', 1, 0)")
        db.commit()
    return db

def main():
    dbConnection = createDB()
    # Load input file
    #fileName = "sample.txt"
    fileName = "input.txt"
    f = open(fileName).readlines()
    # Starting Directory is root
    pwdUID = 1
    for line in f:
        info = line.strip()
        #print(info)
        ############ Work with commands ####################
        if info[0] == "$":
            command = info[2:]
            print("Command: " + command)
            if " " in command:
                cProgram, cDirectory = command.split(" ")
            else:
                cProgram = command
            # Process commands received...
            if cProgram == "cd":
                if cDirectory == "/":
                    print("Changed to root folder: " + info)
                    pwdUID = 1
                elif cDirectory == "..":
                    sql = "SELECT parentID FROM fileSystem WHERE uniqueID=" + str(pwdUID)
                    results = dbConnection.execute(sql)
                    for row in results:
                        pwdUID = row[0]
                    print("Returned to parent directory " + str(pwdUID) + ": " + info)
                # Assume the cDirectory is the name of the directory to switch to...
                else:
                    sql = "SELECT uniqueID FROM fileSystem WHERE name='" + cDirectory + "'"
                    results = dbConnection.execute(sql)
                    for row in results:
                        pwdUID = row[0]
                    print("Changed to new directory " + cDirectory + " with UID of " + str(pwdUID) + ": " + info)
            elif cProgram == "ls":
                print("Directory Listing: " + info)
                continue
        elif info[0:3] == "dir":
            print("Adding folder to database: " + info)
            fType, fName = info.split(" ")
            sql = "INSERT INTO fileSystem (name, type, parentID, size) VALUES ('" + fName + "', 'Folder', " + str(pwdUID) + ", 0)"
            dbConnection.execute(sql)
            dbConnection.commit()
        elif info[0].isdigit():
            # Add file to the database
            print("Adding file to database: " + info)
            fSize, fName = info.split(" ")
            sql = "INSERT INTO fileSystem (name, type, parentID, size) VALUES ('" + fName + "', 'File', " + str(pwdUID) + ", " + str(fSize) + ")"
            dbConnection.execute(sql)
            dbConnection.commit()
        else:
            print("Unable to process: " + info)
    # Identify all of the folders that need to be evaluated...
    print("\nIdentifying all of the folders that need to be evaluated...")
    sql = "SELECT uniqueID, name, parentID FROM fileSystem WHERE type='Folder'"
    results = dbConnection.execute(sql)
    allFolderList = []
    for row in results:
        folderList = []
        uniqueID = row[0]
        name = row[1]
        parentID = row[2]
        print("UniqueID: " + str(uniqueID) + " FolderName: " + name + " ParentID: " + str(parentID))
        folderList.append(uniqueID)
        folderList.append(name)
        folderList.append(parentID)
        allFolderList.append(folderList)
    print("All of the folders needing evaluation: " + str(allFolderList))
    # Identify the size of the contents of each folder...
    print("\nIdentifying the size of the contents in the respective folders...")
    lengthListAllFolders = len(allFolderList)
    for i in range(0, lengthListAllFolders):
        # Gather total size of contents in a folder...
        uniqueID = allFolderList[i][0]
        #print(uniqueID)
        sql = "SELECT size FROM fileSystem WHERE type='File' AND parentID=" + str(uniqueID)
        results = dbConnection.execute(sql)
        totalSize = 0
        for row in results:
            totalSize += row[0]
        print("Total Size: " + str(totalSize) + " FolderList: " + str(allFolderList[i]))
        # Save total size of the contents of the folder in the database
        sqlUpdate = "UPDATE fileSystem SET sizeContents=" + str(totalSize) + " WHERE uniqueID=" + str(uniqueID)
        dbConnection.execute(sqlUpdate)
        dbConnection.commit()
        # Find all child folders of a parent folder and record in the database
        sql = "SELECT uniqueID FROM fileSystem WHERE type='Folder' AND parentID=" + str(uniqueID)
        results = dbConnection.execute(sql)
        listChildFolders = []
        for row in results:
            listChildFolders.append(row[0])
        sqlUpdate = "UPDATE fileSystem SET childFolders='" + str(listChildFolders) + "' WHERE uniqueID=" + str(uniqueID)
        dbConnection.execute(sqlUpdate)
        dbConnection.commit()
    # Identify grandchild relationships to folders and record...
    print("\nIdentifying grandchild folder dependencies...")
    sql = "SELECT uniqueID, childFolders FROM fileSystem WHERE type='Folder'"
    results = dbConnection.execute(sql)
    for i in results:
        print("Folder Unique ID: " + str(i[0]) + " Child Folders: " + str(i[1]))
        # Identify the child dependencies of the children
        childDependencies = json.loads(i[1])  # childDependencies becomes a new list...
        if len(childDependencies) > 0:
            for j in childDependencies:
                #print(j)
                sqlChild = "SELECT childFolders FROM fileSystem WHERE uniqueID=" + str(j)
                resultsChild = dbConnection.execute(sqlChild)
                for rowChild in resultsChild:
                    possibleNewDependencies = json.loads(rowChild[0])
                    for k in possibleNewDependencies:
                        if k not in childDependencies:
                            childDependencies.append(k)
        print("All Folder Dependencies for Unique ID " + str(i[0]) + " " + str(childDependencies))
        sqlUpdate = "UPDATE fileSystem SET allDependentFolders='" + str(childDependencies) + "' WHERE uniqueID=" + str(i[0])
        dbConnection.execute(sqlUpdate)
        dbConnection.commit()
    # Introduce 10 loops to calculate all of the greats of the children...
    for i in range(0,10):
        # Identify great-grandchildren relationships to folders and record
        sql = "SELECT uniqueID, allDependentFolders FROM fileSystem WHERE type='Folder'"
        results = dbConnection.execute(sql)
        for i in results:
            print("Folder Unique ID: " + str(i[0]) + " Child Folders: " + str(i[1]))
            # Identify the child dependencies of the children
            childDependencies = json.loads(i[1])  # childDependencies becomes a new list...
            if len(childDependencies) > 0:
                for j in childDependencies:
                    #print(j)
                    sqlChild = "SELECT childFolders FROM fileSystem WHERE uniqueID=" + str(j)
                    resultsChild = dbConnection.execute(sqlChild)
                    for rowChild in resultsChild:
                        possibleNewDependencies = json.loads(rowChild[0])
                        for k in possibleNewDependencies:
                            if k not in childDependencies:
                                childDependencies.append(k)
            childDependencies.sort()
            print("All Folder Dependencies for Unique ID " + str(i[0]) + " " + str(childDependencies))
            sqlUpdate = "UPDATE fileSystem SET allDependentFolders='" + str(childDependencies) + "' WHERE uniqueID=" + str(i[0])
            dbConnection.execute(sqlUpdate)
            dbConnection.commit()
    # Calculate the size of the dependent folders and the folder that has the dependencies
    sql = "SELECT uniqueID, sizeContents, allDependentFolders FROM fileSystem WHERE type='Folder'"
    results = dbConnection.execute(sql)
    for i in results:
        print("Folder Unique ID: " + str(i[0]) + " Child Folders: " + str(i[2]))
        # Identify the child dependencies of the children
        childDependencies = json.loads(i[2])  # childDependencies becomes a new list...
        totalSizeContents = i[1]    # Add the original folders size
        if len(childDependencies) > 0:
            for j in childDependencies:
                #print(j)
                sqlChild = "SELECT sizeContents FROM fileSystem WHERE uniqueID=" + str(j)
                resultsChild = dbConnection.execute(sqlChild)
                for rowChild in resultsChild:
                    totalSizeContents += rowChild[0]
        print("For Folder Unique ID " + str(i[0]) + " Total Size Contents of Dependencies is " + str(totalSizeContents))
        sqlUpdate = "UPDATE fileSystem SET allDependentFoldersSize='" + str(totalSizeContents) + "' WHERE uniqueID=" + str(i[0])
        dbConnection.execute(sqlUpdate)
        dbConnection.commit()
    # Calculate the total of the totalSize of the allDependentFoldersSize <= 100000
    sql = "SELECT allDependentFoldersSize FROM fileSystem WHERE type='Folder' AND allDependentFoldersSize <= 100000 AND allDependentFoldersSize <> 0"
    results = dbConnection.execute(sql)
    total = 0
    for i in results:
        total += i[0]
    print("Total of allDependentFoldersSize: " + str(total))
    dbConnection.close()




if __name__ == '__main__':
    main()


