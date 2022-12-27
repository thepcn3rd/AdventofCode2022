#!/usr/bin/python3

#fileName = "sample.txt"
fileName = "input.txt"
f = open(fileName).readlines()
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
totalCharValue = 0
for line in f:
    lenLine = len(line.strip())
    middlePos = int(lenLine/2)
    part1 = line.strip()
    part1 = part1[0:middlePos]
    part2 = line.strip()
    part2 = part2[middlePos:]
    print(part1)
    print(part2)
    charList = []
    for x in part1:
        for y in part2:
            if x == y:
                if x not in charList:
                    charList.append(x)
    commonChar = charList[0]
    countLowercase = 1 
    for c in lowercase:
        if commonChar == c:
            print("Char: " + c + " Value: " + str(countLowercase))
            totalCharValue += countLowercase
        countLowercase += 1
    countUppercase = 27
    for c in uppercase:
        if commonChar == c:
            print("Char: " + c + " Value: " + str(countUppercase))
            totalCharValue += countUppercase
        countUppercase += 1
print(totalCharValue)
