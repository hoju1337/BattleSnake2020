from enum import Enum
from Util import *
from GameState import *

#**********************************************#
class SnakeMove(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

################################################
def MoveEnumToText(move):
    if move == SnakeMove.UP:
        return "up"
    if move == SnakeMove.RIGHT:
        return "right"
    if move == SnakeMove.DOWN:
        return "down"
    if move == SnakeMove.LEFT:
        return "left"
    print("bad move!!!", move)

################################################
def IsValidMove(snakeMove, gameBoard, youSnakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(youSnakeId)
    if snakeHeadPos is None:
        return False

    headX = snakeHeadPos['x']
    headY = snakeHeadPos['y']
    print("checking move", snakeMove, "Head x", headX, "Head y", headY)

    # First let's make sure we're not going to hit a wall
    if snakeMove == SnakeMove.UP:
        if headY == 0:
            print("Wall bad up")
            return False
    elif snakeMove == SnakeMove.RIGHT:
        if headX >= (gameBoard.width - 1):
            print("Wall bad right")
            return False
    elif snakeMove == SnakeMove.DOWN:
        if headY >= (gameBoard.height - 1):
            print("Wall bad down")
            return False
    elif snakeMove == SnakeMove.LEFT:
        if headX == 0:
            print("Wall bad left")
            return False

    # Now let's calculate where the snake head will go
    newPosX = headX
    newPosY = headY
    if snakeMove == SnakeMove.UP:
        newPosY -= 1
    elif snakeMove == SnakeMove.RIGHT:
        newPosX += 1
    elif snakeMove == SnakeMove.DOWN:
        newPosY += 1
    elif snakeMove == SnakeMove.LEFT:
        newPosX -= 1
    else:
        print("You're passing the wrong type for snakeMove!!!", snakeMove)

    print("target cell x", newPosX, "y", newPosY)
    nextCell = gameBoard.board[newPosX][newPosY]
    nextCell.DebugPrint()

    # Empty cell is good
    # Food cell is good
    # Snake tails move after so they're bad
    # Snake heads are tricky:
    #     If they turn towards us and we're larger we kill them, smaller or equal we die.
    #     If they turn any other direction we run into what is now their neck and we die
    if nextCell.state == CellState.SNAKE:
        if not nextCell.snakePart.IsTail():
            # need to figure out if this snake has a chance to eat or not
            return False
        elif nextCell.snakePart.IsHead():
            # might be a chance we could survive this, harder to calculate
            return False
        else:
            return False

    return True

################################################
def FindNearestFoodToPoint(x, y, gameBoard):
    nearestFood = None
    for foodPoint in gameBoard.food:
        foodX = foodPoint['x']
        foodY = foodPoint['y']
        distSqr = (foodX - x)**2 + (foodY - y)**2
        if nearestFood is None:
            nearestFood = [distSqr, foodX, foodY]
        elif nearestFood[0] > distSqr:
            nearestFood = [distSqr, foodX, foodY]

    if nearestFood is None:
        return
    return [nearestFood[1], nearestFood[2]]

################################################
def FindNearestFoodToSnake(gameBoard, youSnakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(youSnakeId)
    if snakeHeadPos is None:
        return

    return FindNearestFoodToPoint(snakeHeadPos['x'], snakeHeadPos['y'], gameBoard)

################################################
def TryMoveToX(headX, targetX, gameBoard, youSnakeId):
    eMoveWanted = SnakeMove.RIGHT
    if headX > targetX:
        eMoveWanted = SnakeMove.LEFT
    if IsValidMove(eMoveWanted, gameBoard, youSnakeId):
        return eMoveWanted
    return None

################################################
def TryMoveToY(headY, targetY, gameBoard, youSnakeId):
    eMoveWanted = SnakeMove.DOWN
    if headY > targetY:
        eMoveWanted = SnakeMove.UP
    if IsValidMove(eMoveWanted, gameBoard, youSnakeId):
        return eMoveWanted
    return None

################################################
def GetMoveTowardsPoint(x, y, gameBoard, youSnakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(youSnakeId)
    if snakeHeadPos is None:
        return

    headPosX = snakeHeadPos['x']
    headPosY = snakeHeadPos['y']
    distX = abs(x - headPosX)
    distY = abs(y - headPosY)

    eMove = None
    if distX > distY:
        eMove = TryMoveToX(headPosX, x, gameBoard, youSnakeId)
        if eMove is None:
            eMove = TryMoveToY(headPosY, y, gameBoard, youSnakeId)
    else:
        eMove = TryMoveToY(headPosY, y, gameBoard, youSnakeId)
        if eMove is None:
            eMove = TryMoveToX(headPosX, x, gameBoard, youSnakeId)

    if eMove is None:
        # Couldn't move in a direction towards the food.
        # Try moving away from the nearest wall
        pass

    return eMove

