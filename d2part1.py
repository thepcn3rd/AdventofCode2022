#!/usr/bin/python3

def outputInfo(lNumber, tScore, oOption, sOption):
    info = "Line: " + str(lNumber)
    info += " Total Score: " + str(tScore)
    if oOption == "A":
        info += " O: Rock (A)"
    elif oOption == "B":
        info += " O: Paper (B)"
    elif oOption == "C":
        info += " O: Scissors (C)"
    if sOption == "X":
        info += " S: Rock (X) [+1]"
    elif sOption == "Y":
        info += " S: Paper (Y) [+2]"
    elif sOption == "Z":
        info += " S: Scissors (Z) [+3]"
    return info

def main():
    fileName = "input.txt"
    lineNumber = 1
    totalScore = 0
    f = open(fileName, "r")
    for line in f:
        # Opponent
        # A = Rock
        # B = Paper
        # C = Scissors

        # Your strategy guide
        # Score is the shape selected
        # X = Rock - 1 pt.
        # Y = Paper - 2 pt.
        # Z = Scissors - 3 pt.

        # Rock over Scissors
        # Scissors over Paper
        # Paper over Rock

        # Outcome of the round
        # 0 - Lost
        # 3 - Draw
        # 6 - Won
        values = line.split(" ")
        opponent = values[0]
        strategy = values[1].strip()
        # Opponent Rock (A) over Scissors (Z)
        if opponent == "A" and strategy == "Z":
            # Score 3pt for Z
            totalScore += 3
            # Lost to opponent 0pt.
            o = outputInfo(lineNumber, totalScore, "A", "Z")
            print(o + " - Lost to Opponent")
        # Strategy Rock (X) over Scissors (C)
        elif strategy == "X" and opponent == "C":
            # Score 1pt. for X
            totalScore += 1
            # Strategy for the win 6pt.
            totalScore += 6
            o = outputInfo(lineNumber, totalScore, "C", "X")
            print(o + " - Winner! [+6]")
        # Opponent Paper (B) over Rock (X)
        elif opponent == "B" and strategy == "X":
            # Score 1pt. for X
            totalScore += 1
            # Lost to opponent 0pt.
            o = outputInfo(lineNumber, totalScore, "B", "X")
            print(o + " - Lost to Opponent")
        # Strategy Paper (Y) over Rock (A)
        elif strategy == "Y" and opponent == "A":
            # Score 2pt. for Y
            totalScore += 2
            # Strategy for the win 6pt.
            totalScore += 6
            o = outputInfo(lineNumber, totalScore, "A", "Y")
            print(o + " - Winner! [+6]")
        # Opponent Scissors (C) over Paper (Y)
        elif opponent == "C" and strategy == "Y":
            # Score 2 pt. for Paper
            totalScore += 2
            # Lost to opponent 0pt.
            o = outputInfo(lineNumber, totalScore, "C", "Y")
            print(o + " - Lost to Opponent")
        # Strategy Scissors (Z) over Paper (B)
        elif strategy == "Z" and opponent == "B":
            # Score 3pt. for Z
            totalScore += 3
            # Strategy for the win 6pt.
            totalScore += 6
            o = outputInfo(lineNumber, totalScore, "B", "Z")
            print(o + " - Winner! [+6]")
        # Draw
        else:
            # 3 Points for a Draw
            totalScore += 3
            if strategy == "X":
                totalScore += 1
            elif strategy == "Y":
                totalScore += 2
            elif strategy == "Z":
                totalScore += 3
            o = outputInfo(lineNumber, totalScore, opponent, strategy)
            print(o + " - ** Draw ** [+3]")
        #print(line)
        lineNumber += 1
    f.close()
    




if __name__ == '__main__':
    main()