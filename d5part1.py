#!/usr/bin/python3

import re

# Stacks from the Puzzle Input
#[M]                     [N] [Z]    
#[F]             [R] [Z] [C] [C]    
#[C]     [V]     [L] [N] [G] [V]    
#[W]     [L]     [T] [H] [V] [F] [H]
#[T]     [T] [W] [F] [B] [P] [J] [L]
#[D] [L] [H] [J] [C] [G] [S] [R] [M]
#[L] [B] [C] [P] [S] [D] [M] [Q] [P]
#[B] [N] [J] [S] [Z] [W] [F] [W] [R]
# 1   2   3   4   5   6   7   8   9 

stack1 = ["B", "L", "D", "T", "W", "C", "F", "M"]
stack2 = ["N","B","L"]
stack3 = ["J","C","H","T","L","V"]
stack4 = ["S","P","J","W"]
stack5 = ["Z","S","C","F","T","L","R"]
stack6 = ["W","D","G","B","H","N","Z"]
stack7 = ["F","M","S","P","V","G","C","N"]
stack8 = ["W","Q","R","J","F","V","C","Z"]
stack9 = ["R","P","M","L","H"]
allStacks = [stack1, stack2, stack3, stack4, stack5, stack6, stack7, stack8, stack9]
print(allStacks)

fileName = "input.txt"
f = open(fileName).readlines()
for line in f:
    info = line.strip()
    regex = 'move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)'
    result = re.search(regex, info)
    print(str(result.groups()) + " - " + info)
    # Crates to move 
    cratesMoving = int(result.group(1))
    print("Crates Moving: " + str(cratesMoving))
    # From Stack
    fromStack = int(result.group(2))
    # To Stack
    toStack = int(result.group(3))
    ##### 
    for crate in range(0, cratesMoving):  # Number of crates 3 would be equivalent to 0 to 2
        # Length of From Stack
        lenFromStack = len(allStacks[fromStack-1]) # Length of stack counts at 1
        print("Items on From Stack (" + str(fromStack) + ") : " + str(lenFromStack) + " - " + str(allStacks[fromStack-1]))
        # Item on From Stack
        itemMovingFromStack = allStacks[fromStack-1][lenFromStack-1] # Subtract 1 from Length of Stack due to item starts at 0
        print("Item Moving: " + itemMovingFromStack)
        print("Items on To Stack (" + str(toStack) + ") prior to Move: " + str(allStacks[toStack-1]))
        # Move item to stack
        allStacks[toStack-1].append(itemMovingFromStack)
        print("Items on To Stack (" + str(toStack) + ") after Move: " + str(allStacks[toStack-1]))
        # Remove item from initial stack
        allStacks[fromStack-1].pop()
        print("Items remaining on From Stack (" + str(fromStack) + ") after removal: " + str(allStacks[fromStack-1]))
        print("")
# Print what is remaining on the stacks
print("Stack 1: " + str(allStacks[0]))
print("Stack 2: " + str(allStacks[1]))
print("Stack 3: " + str(allStacks[2]))
print("Stack 4: " + str(allStacks[3]))
print("Stack 5: " + str(allStacks[4]))
print("Stack 6: " + str(allStacks[5]))
print("Stack 7: " + str(allStacks[6]))
print("Stack 8: " + str(allStacks[7]))
print("Stack 9: " + str(allStacks[8]))

# Top Label of Stack from Each
lenStack1 = len(allStacks[0])
lenStack2 = len(allStacks[1])
lenStack3 = len(allStacks[2])
lenStack4 = len(allStacks[3])
lenStack5 = len(allStacks[4])
lenStack6 = len(allStacks[5])
lenStack7 = len(allStacks[6])
lenStack8 = len(allStacks[7])
lenStack9 = len(allStacks[8])
message = allStacks[0][lenStack1-1] + allStacks[1][lenStack2-1] + allStacks[2][lenStack3-1]
message += allStacks[3][lenStack4-1] + allStacks[4][lenStack5-1] + allStacks[5][lenStack6-1]
message += allStacks[6][lenStack7-1] + allStacks[7][lenStack8-1] + allStacks[8][lenStack9-1]
print(message)




    

