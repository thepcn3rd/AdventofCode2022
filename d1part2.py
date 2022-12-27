#!/usr/bin/python3


def stcContainsNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def main():
    # Day 1 Advent of Code - Counting Calories - Part 2
    fileName = "inputCalories.txt"
    f = open(fileName, "r")
    maxCalories = 0
    listTotalCalories = []
    totalCalories = 0
    groupCount = 1
    lineCount = 1
    for line in f:
        if line == '\n':
            if totalCalories > maxCalories:
                maxCalories = totalCalories
                print("Elf:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount) + " **New Max**")
            else:    
                print("Elf:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount))
            listTotalCalories.append(totalCalories)
            totalCalories = 0
            groupCount += 1
        elif stcContainsNumbers(line):
            totalCalories += int(line)
        lineCount += 1
    # End of the file
    if totalCalories > maxCalories:
        maxCalories = totalCalories
        maxCalories = totalCalories
        print("Elf:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount) + " **New Max**")
    else:    
        print("Elf:" + str(groupCount) + " Calories:" + str(totalCalories) + " LineCount:" + str(lineCount))
    print("Max Calories carried by an Elf: " + str(maxCalories))
    print("")
    listTotalCalories.sort(reverse=True)
    #print("List of Total Calories: " + str(listTotalCalories))
    print("Top 3 Elves Calories that are Carried: ")
    print("Elf 1st: " + str(listTotalCalories[0]))
    print("Elf 2nd: " + str(listTotalCalories[1]))
    print("Elf 3rd: " + str(listTotalCalories[2]))
    print("Total: " + str(listTotalCalories[0] + listTotalCalories[1] + listTotalCalories[2]))





if __name__ == '__main__':
    main()



