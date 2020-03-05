import random
import math

from GameState import *

################################################
def RandomColor():
    hexVals = ["00", "7F", "FF"]
    color = "FFFFFF"
    while (color == "FFFFFF"):
        color = random.choice(hexVals)
        color = color + random.choice(hexVals)
        color = color + random.choice(hexVals)

    return "#" + color

################################################
def RandomHead():
    heads = [
             "regular",
             "beluga",
             "bendr",
             "dead",
             "evil",
             "fang",
             "pixel",
             "safe",
             "sand-worm",
             "shades",
             "silly",
             "smile",
             "tongue",
             "bwc-bonhomme",
             "bwc-earmuffs",
             "bwc-rudolph",
             "bwc-scarf",
             "bwc-ski",
             "bwc-snow-worm",
             "bwc-snowman",
            ]
    return random.choice(heads)

################################################
def RandomTail():
    tails = [
             "regular",
             "block-bum",
             "bolt",
             "curled",
             "fat-rattle",
             "freckled",
             "hook",
             "pixel",
             "round-bum",
             "sharp",
             "skinny",
             "small-rattle",
             "bwc-bonhomme",
             "bwc-flake",
             "bwc-ice-skate",
             "bwc-present",
            ]
    return random.choice(tails)

################################################
def PrintColumnHeaders(width, height):
    # Print the ten's column
    if (width > 10):
        # First add spaces for Y coordinate columns
        strMsg = " "
        if (height > 10):
            strMsg += " "

        # Now add the ten's digit
        for i in range(width):
            tensDigit = int(math.floor(i / 10))
            strMsg += " " + str(tensDigit)
        print(strMsg)

    # Print the one's column
    # First add spaces for Y coordinate columns
    strMsg = " "
    if (height > 10):
        strMsg += " "

    # Now add the one's digit
    for j in range(width):
        strMsg += " " + str(j % 10)
    print(strMsg)

################################################
def PrintSeparatorRow(width, height):
    strMsg = " "
    if (height > 10):
        strMsg += " "

    for i in range(width):
        strMsg += "--"
    print(strMsg + "-")

################################################
def PrintBoardRow(curRow, gameBoard, youId, simpleSnakeIds):
    strMsg = ""
    if (gameBoard.height > 10):
        # Add the ten's digit
        tensDigit = int(math.floor(curRow / 10))
        strMsg += str(tensDigit)
    # Add the one's digit
    strMsg += str(curRow % 10)
    strMsg += "|"

    for i in range(gameBoard.width):
        cell = gameBoard.board[i][curRow]
        if cell.state == CellState.EMPTY:
            strMsg += " "
        elif cell.state == CellState.FOOD:
            strMsg += "F"
        else:   #cell.state == CellState.SNAKE
            if cell.snakePart.IsHead():
                strMsg += "H"
            elif cell.snakePart.IsTail():
                strMsg += "T"
            else:
                if cell.snakePart.snakeData.id == youId:
                    strMsg += "Y"
                else:
                    strMsg += str(simpleSnakeIds[cell.snakePart.snakeData.id])

        strMsg += "|"

    print(strMsg)


################################################
def PrintBoard(gameBoard, youId, simpleSnakeIds):
    width = gameBoard.width
    height = gameBoard.height

    # We're not going to print a massive board
    if width > 99 or height > 99:
        print("Board too large W", width, "H", height)
        return

    if width < 1 or height < 1:
        print("Invalid board dimensions W", width, "H", height)
        return

    PrintColumnHeaders(width, height)
    PrintSeparatorRow(width, height)

    for i in range(height):
        PrintBoardRow(i, gameBoard, youId, simpleSnakeIds)

