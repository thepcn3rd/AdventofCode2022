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
    # Example  2 <= 3                         and 8 >= 7         # 2-8, 3-7
    if int(assignmentRangeX1) <= int(assignmentRangeY1) and int(assignmentRangeX2) >= int(assignmentRangeY2):
        print("Range Y is within Range X - " + info)
        totalOverlaps += 1
    elif int(assignmentRangeY1) <= int(assignmentRangeX1) and int(assignmentRangeY2) >= int(assignmentRangeX2):
        print("Range X is within Range Y - " + info)
        totalOverlaps += 1
print("Total Overlaps: " + str(totalOverlaps))

    



