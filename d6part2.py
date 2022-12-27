#!/usr/bin/python3

def evaluateChars(cList):
    global uniqueChars
    lengthSet = len(set(cList))
    lengthList = len(cList)
    #print("Length of Set: " + str(lengthSet) + " Length of List: " + str(lengthList) + " List: " + str(cList))
    if lengthSet == lengthList:
        uniqueChars = True

fileName = "input.txt"
f = open(fileName).readlines()
for line in f:
    info = line.strip()
    totalChars = 1
    charList = []
    uniqueChars = False
    for c in info:
        # Build the initial list of characters
        if len(charList) < 13:   # Length of a list starts at 0
            charList.append(c)
            totalChars += 1
        # With the list of characters evaluate them for 4 unique characters in a row
        elif len(charList) == 13:
            charList.append(c)
            evaluateChars(charList)
            totalChars += 1
        else:  
            charList.append(c)
            charList.pop(0)
            evaluateChars(charList)
            if (uniqueChars):
                print("Unique Chars Detected at Character Total: " + str(totalChars))
                #print(uniqueChars)
                break
            totalChars += 1
        #print(charList)
    print("Total Chars until Unique Chars Detected: " + str(totalChars))
