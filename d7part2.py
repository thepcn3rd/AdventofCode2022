#!/usr/bin/python3

import os
import sqlite3

def createDB():
    # To create the database in memory use :memory:
    #dbFile = ":memory:"
    dbFile = "my.db"
    if not os.path.exists(dbFile):
        os.close(os.open(dbFile, os.O_CREAT))
    else:
        os.remove(dbFile)
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
        sql = "CREATE TABLE fileSystem ("
        sql += "uniqueID INTEGER PRIMARY KEY AUTOINCREMENT, "   # UniqueID of the element whether a file or a folder
        sql += "name VARCHAR(40), "                             # name - given name of folder or file
        sql += "type VARCHAR(10), "                             # type - Folder, File
        sql += "parentID INTEGER, "                             # parentID - Link backwards if this is the child 
        sql += "size INTEGER, "                                 # size - Relative to a file
        sql += "sizeContents INTEGER DEFAULT 0, "               # sizeContents - Size of the immediate children in the directory
        sql += "sizeAll INTEGER DEFAULT 0, "                    # sizeAll - Size of all of the sub-directories and files...
        sql += "sizeFlag INTEGER DEFAULT 'N', "                 # sizeFlag if sizeAll >100000
        sql += "parentFolders VARCHAR(50), "                    # parentFolders - IDs of all of the parent folders
        sql += "childFolders VARCHAR(50))"                     # childFolders - IDs of the direct child directories
        c.execute(sql)
        # Insert root directory...
        c.execute("INSERT INTO fileSystem (name, type, parentID, size) VALUES ('root', 'Folder', 1, 0)")
        db.commit()
    return db


def main():
    # Reviewed the following code and learned how to do the below case statement...
    # Also used the code to debug below and the functionality...
    # https://github.com/orfeasa/advent-of-code-2022/blob/main/day_07/main.py
    dbConnection = createDB()
    #fileName = "sample.txt"
    fileName = "input.txt"
    f = open(fileName).readlines()
    pwdUID = 1  # Present working directory UID
    parentFolderList = [1]
    for line in f:
        info = line.strip()
        match info.split():
            case ["$", "ls"]:
                print("Directory Listing: " + info)
                continue
            case ["$", "cd", "/"]:
                pwdUID = 1
                parentFolderList = [1]
            case ["$", "cd", ".."]:
                print("Go back a directory...")
                sql = "SELECT parentID FROM fileSystem WHERE uniqueID=" + str(pwdUID)
                results = dbConnection.execute(sql)
                for row in results:
                    pwdUID = row[0]
                print("Returned to parent directory " + str(pwdUID) + ": " + info)
                parentFolderList.pop()
            case ["$", "cd", dirName]:
                print("CD: " + dirName)
                # In the input multiple directories are given the same name
                # In the initial query I did not account for this, added type=Folder and the parentID=pwdUID
                # to fix the oversight...  This then produced the 17 files and folders with the name of tjhzggs
                sql = "SELECT uniqueID FROM fileSystem WHERE name='" + dirName + "' AND type='Folder' AND parentID=" + str(pwdUID)
                results = dbConnection.execute(sql)
                for row in results:
                    pwdUID = row[0]
                print("Changed to new directory " + dirName + " with UID of " + str(pwdUID) + ": " + info)
                # Add in the database the parentFolderList recorded in rootDirList
                sql = "UPDATE fileSystem SET parentFolders='" + str(parentFolderList) + "' WHERE uniqueID=" + str(pwdUID)
                dbConnection.execute(sql)
                dbConnection.commit()
                parentFolderList.append(pwdUID)
            case ["dir", dirName]:
                print("Create Directory: " + dirName)
                sql = "INSERT INTO fileSystem (name, type, parentID, size) VALUES ('" + dirName + "', 'Folder', " + str(pwdUID) + ", 0)"
                dbConnection.execute(sql)
                dbConnection.commit()
            case [size, filename]:
                print("Create Filename: " + filename + " Size: " + size + " parentFolderList: " + str(parentFolderList))
                sql = "INSERT INTO fileSystem (name, type, parentID, size) VALUES ('" + filename + "', 'File', " + str(pwdUID) + ", " + str(size) + ")"
                dbConnection.execute(sql)
                dbConnection.commit()
                # Add to the sizeContents column for the directory the file is in
                sql = "SELECT sizeContents FROM fileSystem WHERE uniqueID=" + str(pwdUID)
                results = dbConnection.execute(sql)
                for row in results:
                    sizeContents = row[0]
                print("Current size of sizeContents: " + str(sizeContents))
                totalSizeContents = sizeContents + int(size)     # Add current size contents + file size
                sql = "UPDATE fileSystem SET sizeContents=" + str(totalSizeContents) + " WHERE uniqueID=" + str(pwdUID)
                dbConnection.execute(sql)
                dbConnection.commit()
                # Find the sizeAll variable for the directory and then add the new file size to the sizeAll...
                for uid in parentFolderList:
                    sql = "SELECT sizeAll FROM fileSystem WHERE uniqueID=" + str(uid)
                    results = dbConnection.execute(sql)
                    for row in results:
                        sizeAll = row[0]
                    print("Current size of sizeAll: " + str(sizeAll))
                    totalSizeAll = sizeAll + int(size)     # Add current size contents + file size
                    if totalSizeAll > 100000:
                        sql = "UPDATE fileSystem SET sizeAll=" + str(totalSizeAll) + ", sizeFlag='Y' WHERE uniqueID=" + str(uid)
                    else:
                        sql = "UPDATE fileSystem SET sizeAll=" + str(totalSizeAll) + " WHERE uniqueID=" + str(uid)
                    dbConnection.execute(sql)
                    dbConnection.commit()
    # Output the answer for partOne
    sql = "SELECT sum(sizeAll) FROM fileSystem WHERE type='Folder' AND sizeFlag='N';"
    results = dbConnection.execute(sql)
    for row in results:
        totalPartOne = row[0]
    print("\nTotal for Part 1: " + str(totalPartOne) + "\n")
    # Output for partTwo
    # totalspace = 70000000
    # root = 46552309
    #space = 70000000 - 48381165  # Sample
    space = 70000000 - 46552309
    # Update needs 30000000
    spaceToFree = 30000000 - space
    print("Space needed to free: " + str(spaceToFree))  # 6,552,309  6552309
    sql = "SELECT name, sizeAll FROM fileSystem WHERE sizeAll>=6552309 AND type='Folder' ORDER BY sizeAll LIMIT 1;"
    results = dbConnection.execute(sql)
    for row in results:
        rName = row[0]
        rSizeAll = row[1]
    print("\nPart 2: Remove the directory " + rName + " to free up " + str(rSizeAll) + "\n")








if __name__ == '__main__':
    main()