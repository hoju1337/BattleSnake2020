from enum import Enum
from GameState import *

#**********************************************#
class SnakeMoved(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    DIED = 5

#**********************************************#
class SnakeMovedResult(Enum):
    NORMAL = 1  # Didn't do anything interesting
    ATE = 2
    KILLED = 3

################################################
def PrintSnakeTurn(snakeTurn, gameState, snakeId):
    strMsg = "Snake " + str(gameState.simpleSnakeIds[snakeId])
    move = snakeTurn[0]
    if move == SnakeMoved.UP:
        strMsg += " moved UP"
    elif move == SnakeMoved.RIGHT:
        strMsg += " moved RIGHT"
    elif move == SnakeMoved.DOWN:
        strMsg += " moved DOWN"
    elif move == SnakeMoved.LEFT:
        strMsg += " moved LEFT"
    elif move == SnakeMoved.DIED:
        strMsg += " DIED"

    result = snakeTurn[1]
    if result == SnakeMovedResult.ATE:
        strMsg += " and ATE"
    elif result == SnakeMovedResult.KILLED:
        strMsg += " and KILLED"

    print(strMsg)

################################################
def GetSnakeSingleTurn(prevGameBoard, currGameBoard, snakeId):
    if snakeId not in prevGameBoard.snakes:
        return  # shouldn't happen, why do we still have a snakeId for a snake that was dead last turn?
    if snakeId not in currGameBoard.snakes:
        return [SnakeMoved.DIED, SnakeMovedResult.NORMAL]

    prevHeadPos = prevGameBoard.snakes[snakeId].GetHead()
    currHeadPos = currGameBoard.snakes[snakeId].GetHead()
    prevHeadX = prevHeadPos['x']
    prevHeadY = prevHeadPos['y']
    currHeadX = currHeadPos['x']
    currHeadY = currHeadPos['y']

    move = None
    if prevHeadX < currHeadX:
        move = SnakeMoved.RIGHT
    elif prevHeadX > currHeadX:
        move = SnakeMoved.LEFT
    elif prevHeadY < currHeadY:
        move = SnakeMoved.DOWN
    elif prevHeadY > currHeadY:
        move = SnakeMoved.UP
    else:
        print("Snake didn't move!!", snakeId)

    result = SnakeMovedResult.NORMAL
    prevCell = prevGameBoard.board[currHeadX][currHeadY]
    if prevCell.state == CellState.FOOD:
        result = SnakeMovedResult.ATE
    elif prevCell.state == CellState.SNAKE:
        # If you ran into another snake and you're still alive you must have killed it
        result = SnakeMovedResult.KILLED

    return [move, result]


################################################
def GetAllSnakeSingleTurns(prevGameBoard, currGameBoard, gameState):
    print("~~~~ Snake Moves ~~~~")
    snakeTurns = []
    for snakeId in prevGameBoard.snakes:
        snakeTurn = GetSnakeSingleTurn(prevGameBoard, currGameBoard, snakeId)
        snakeTurns.append(snakeTurn)
        PrintSnakeTurn(snakeTurn, gameState, snakeId)
    print("")

################################################
def AnalyseMoves(persistentData, currGameBoard, gameState):
    # If this is the first move we're just initializing things
    if not hasattr(persistentData, 'prevGameBoard'):
        persistentData.prevGameBoard = currGameBoard
        return

    allSnakeMoves = GetAllSnakeSingleTurns(persistentData.prevGameBoard, currGameBoard, gameState)

    persistentData.prevGameBoard = currGameBoard
