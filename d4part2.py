#!/usr/bin/python3

fileName = "input.txt"
f = open(fileName).readlines()
totalOverlaps = 0
for line in f:
    print(line.strip())
    info = line.strip()
    elfTeam1, elfTeam2 = info.split(",")
    assignmentRangeX1, assignmentRangeX2 = elfTeam1.split("-")
    assignmentRangeY1, assignmentRangeY2 = elfTeam2.split("-")
    # Calculate elfTeam1 Assignment
    # Difference from part 1 - Detect any overlaps between the pairs...
    # 
    if int(assignmentRangeX1) <= int(assignmentRangeY1) and int(assignmentRangeX2) >= int(assignmentRangeY1):
        print("Point Y1 matches or is within Points X1 to X2 - " + info)
        totalOverlaps += 1
    elif int(assignmentRangeY1) <= int(assignmentRangeX1) and int(assignmentRangeY2) >= int(assignmentRangeX1):
        print("Point X1 matches or is within Points Y1 to Y2 - " + info)
        totalOverlaps += 1
    
print("Total Overlaps: " + str(totalOverlaps))

    



