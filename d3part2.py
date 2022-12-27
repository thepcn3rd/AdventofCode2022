#!/usr/bin/python3

#fileName = "sample.txt"
fileName = "input.txt"
f = open(fileName).readlines()
countLines = 0
line1 = ""
line2 = ""
line3 = ""
commonChar = []
commonChar2 = []
commonChar3 = []
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
totalCharValue = 0
for line in f:
    info = line.strip()
    #print(info)
    countLines += 1
    if countLines == 1:
        line1 = info
    if countLines == 2:
        line2 = info
    if countLines == 3:
        line3 = line.strip()
        #print("3rd Line")
        print("Line 1: " + line1)
        print("Line 2: " + line2)
        print("Line 3: " + line3)
        # Compare the Lines
        for a in line1:
            for b in line2:
                if a == b:
                    if a not in commonChar:
                        commonChar.append(a)
        for b in line2:
            for c in line3:
                if b == c:
                    if b not in commonChar2:
                        commonChar2.append(b)
        for d in commonChar:
            for e in commonChar2:
                if d == e:
                    if d not in commonChar3:
                        commonChar3.append(d)
        countLines = 0
        cChar = commonChar3[0]
        countLowercase = 1 
        for c in lowercase:
            if cChar == c:
                print("Char: " + c + " Value: " + str(countLowercase))
                totalCharValue += countLowercase
            countLowercase += 1
        countUppercase = 27
        for c in uppercase:
            if cChar == c:
                print("Char: " + c + " Value: " + str(countUppercase))
                totalCharValue += countUppercase
            countUppercase += 1
        commonChar = []
        commonChar2 = []
        commonChar3 = []
print(totalCharValue)
        