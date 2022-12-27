#!/usr/bin/python3

def outputInfo(lNumber, tScore, oOption, sOption, guess):
    info = "Line: " + str(lNumber)
    info += " Total Score: " + str(tScore)
    if oOption == "A":
        info += " O: Rock (A)"
    elif oOption == "B":
        info += " O: Paper (B)"
    elif oOption == "C":
        info += " O: Scissors (C)"
    if sOption == "X":
        info += " S: Loose (X) [+0]"
    elif sOption == "Y":
        info += " S: Draw (Y) [+3]"
    elif sOption == "Z":
        info += " S: Win (Z) [+6]"
    if guess == "Scissors":
        info += " G: Scissors [+3]"
    elif guess == "Paper":
        info += " G: Paper [+2]"
    elif guess == "Rock":
        info += " G: Rock [+1]"
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
        # X = Loose - 0 pt.
        # Y = Draw - 3 pt.
        # Z = Win - 6 pt.

        # Guess
        # Rock [+1]
        # Paper [+2]
        # Scissors [+3]

        # Rock over Scissors
        # Scissors over Paper
        # Paper over Rock
        print(line.strip())
        values = line.split(" ")
        opponent = values[0]
        strategy = values[1].strip()
        if strategy == "Z":
            # Score 6pt for Z
            totalScore += 6
            # Opponent Rock (A) over Win (Z) Guess: Paper
            if opponent == "A":    
                # Guess to Paper
                totalScore += 2
                o = outputInfo(lineNumber, totalScore, "A", "Z", "Paper")
            # Opponent Paper (B) over Win (Z) Guess: Scissors
            elif opponent == "B":
                # Guess to Scissors
                totalScore += 3
                o = outputInfo(lineNumber, totalScore, "B", "Z", "Scissors")
            # Opponent Scissors (C) over Win (Z) Guess: Rock
            elif opponent == "C":
                # Guess to Rock
                totalScore += 1
                o = outputInfo(lineNumber, totalScore, "C", "Z", "Rock")
            print(o + " - Win! [+6]")
        elif strategy == "Y":
            # Score 3pt. for Draw
            totalScore += 3
            # Opponent Rock (A) with Draw Guess: Rock
            if opponent == "A":
                # Guess to Rock
                totalScore += 1
                o = outputInfo(lineNumber, totalScore, "A", "Y", "Rock")
            # Opponent Paper (B) with Draw Guess: Paper
            elif opponent == "B":
                # Guess to Paper
                totalScore += 2
                o = outputInfo(lineNumber, totalScore, "B", "Y", "Paper")
            # Opponent Scissors (C) with Draw Guess: Scissors
            elif opponent == "C":
                # Guess to Scissors
                totalScore += 3
                o = outputInfo(lineNumber, totalScore, "C", "Y", "Scissors")
            print(o + " - ** Draw ** [+3]")
        elif strategy == "X":
            # Score 0pt. for a loss
            # Opponent Rock (A) loose to Guess: Scissors
            if opponent == "A":
                # Guess of Scissors
                totalScore += 3
                o = outputInfo(lineNumber, totalScore, "A", "X", "Scissors")
            # Opponent Paper (B) loose to Guess: Rock
            elif opponent == "B":
                # Guess of Rock
                totalScore += 1
                o = outputInfo(lineNumber, totalScore, "B", "X", "Rock")
            # Opponent Scissors (C) loose to Guess: Paper
            elif opponent == "C":
                # Guess of Paper
                totalScore += 2
                o = outputInfo(lineNumber, totalScore, "C", "X", "Paper")
            print(o + " Lost")
        #print(line)
        lineNumber += 1
    f.close()
    




if __name__ == '__main__':
    main()