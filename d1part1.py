#!/usr/bin/python3


def stcContainsNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def main():
    # Day 1 Advent of Code - Counting Calories - Part 1
    fileName = "inputCalories.txt"
    f = open(fileName, "r")
    maxCalories = 0
    totalCalories = 0
    groupCount = 1
    lineCount = 1
    for line in f:
        if line == '\n':
            if totalCalories > maxCalories:
                maxCalories = totalCalories
                print("Group:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount) + " **New Max**")
            else:    
                print("Group:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount))
            totalCalories = 0
            groupCount += 1
        elif stcContainsNumbers(line):
            totalCalories += int(line)
        lineCount += 1
    # End of the file
    if totalCalories > maxCalories:
        maxCalories = totalCalories
        maxCalories = totalCalories
        print("Group:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount) + " **New Max**")
    else:    
        print("Group:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount))
    print("Max Calories: " + str(maxCalories))





if __name__ == '__main__':
    main()



