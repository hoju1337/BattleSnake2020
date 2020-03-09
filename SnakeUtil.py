from enum import Enum
from Util import *
from GameState import *
from TurnAnalysisBasic import *

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
#    print("bad move!!!", move)

#**********************************************#
class CoordsOfMove:
    def __init__(self, coords, snakeMove):
        self.coords = coords
        self.snakeMove = snakeMove
        self.x = coords[0]
        self.y = coords[1]

################################################
# Given an x, y apply snakeMove and return new coords
def GetNewCoordsOfMoveFromXY(x, y, snakeMove, gameBoard):
    # First let's check if we're going to hit a wall
    if snakeMove == SnakeMove.UP:
        if y == 0:
            return
    elif snakeMove == SnakeMove.RIGHT:
        if x >= (gameBoard.width - 1):
            return
    elif snakeMove == SnakeMove.DOWN:
        if y >= (gameBoard.height - 1):
            return
    elif snakeMove == SnakeMove.LEFT:
        if x == 0:
            return

    # Now let's calculate where the snake head will go
    newPosX = x
    newPosY = y
    if snakeMove == SnakeMove.UP:
        newPosY -= 1
    elif snakeMove == SnakeMove.RIGHT:
        newPosX += 1
    elif snakeMove == SnakeMove.DOWN:
        newPosY += 1
    elif snakeMove == SnakeMove.LEFT:
        newPosX -= 1
#    else:
#        print("You're passing the wrong type for snakeMove!!!", snakeMove)

    return [newPosX, newPosY]

################################################
# Given an [x,y] apply snakeMove and return new coords
def GetNewCoordsOfMoveFromCoords(coords, snakeMove, gameBoard):
    return GetNewCoordsOfMoveFromXY(coords[0], coords[1], snakeMove, gameBoard)

################################################
# return new coords when applying snakeMove to the
# given snakes head
def GetCoordsOfMove(snakeMove, gameBoard, snakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(snakeId)
    if snakeHeadPos is None:
        return False
    return GetNewCoordsOfMoveFromXY(snakeHeadPos['x'], snakeHeadPos['y'], snakeMove, gameBoard)

################################################
# Is the requested move going to result in moving to
# a valid space (not considering snake collisions)
def IsValidMoveFromXY(x, y, snakeMove, gameBoard, snakeId):
    # First let's make sure we're not going to hit a wall
    if snakeMove == SnakeMove.UP:
        if y == 0:
#            print("Wall bad up")
            return False
    elif snakeMove == SnakeMove.RIGHT:
        if x >= (gameBoard.width - 1):
#            print("Wall bad right")
            return False
    elif snakeMove == SnakeMove.DOWN:
        if y >= (gameBoard.height - 1):
#            print("Wall bad down")
            return False
    elif snakeMove == SnakeMove.LEFT:
        if x == 0:
#            print("Wall bad left")
            return False

    # Now let's calculate where the snake head will go
    newPosX = x
    newPosY = y
    if snakeMove == SnakeMove.UP:
        newPosY -= 1
    elif snakeMove == SnakeMove.RIGHT:
        newPosX += 1
    elif snakeMove == SnakeMove.DOWN:
        newPosY += 1
    elif snakeMove == SnakeMove.LEFT:
        newPosX -= 1
#    else:
#        print("You're passing the wrong type for snakeMove!!!", snakeMove)

#    print("target cell x", newPosX, "y", newPosY)
    nextCell = gameBoard.board[newPosX][newPosY]
#    nextCell.DebugPrint()

    # Empty cell is good
    # Food cell is good
    # Snake heads move before tails so moving to a tail is bad
    # Snake heads are tricky:
    #   Not sure what happens if our heads are next to each other and we essentially swap head directions.
    #       Going to assume we die
    #   If they turn any other direction we run into what is now their neck and we die
    if nextCell.state == CellState.SNAKE:
        # The above comments basically boil down to any snake part is bad
        return False

    return True

################################################
# Is the requested move going to result in moving to
# a valid space (not considering snake collisions)
def IsValidMove(snakeMove, gameBoard, snakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(snakeId)
    if snakeHeadPos is None:
        return False

    headX = snakeHeadPos['x']
    headY = snakeHeadPos['y']
#    print("checking move", snakeMove, "Head x", headX, "Head y", headY)

    return IsValidMoveFromXY(headX, headY, snakeMove, gameBoard, snakeId)

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

################################################
def CouldPosEatYou(coords, youSnakeLength, gameBoard):
    if coords is not None:
        cell = gameBoard.board[coords[0]][coords[1]]
        if cell.state == CellState.SNAKE and cell.snakePart.IsHead():
            if youSnakeLength <= cell.snakePart.SnakeLength():
                return True
    return False

################################################
def CouldMoveGetYouEaten(eMove, gameBoard, youSnakeId):
    moveCoords = GetCoordsOfMove(eMove, gameBoard, youSnakeId)

    # check all the directions from where we'd move to to see if another snake could eat us
    adjacentUp = None
    adjacentRight = None
    adjacentDown = None
    adjacentLeft = None

    # no need to check the direction we're coming from
    if eMove != SnakeMove.DOWN:
        adjacentUp = GetNewCoordsOfMoveFromCoords(moveCoords, SnakeMove.UP, gameBoard)
    if eMove != SnakeMove.LEFT:
        adjacentRight = GetNewCoordsOfMoveFromCoords(moveCoords, SnakeMove.RIGHT, gameBoard)
    if eMove != SnakeMove.UP:
        adjacentDown = GetNewCoordsOfMoveFromCoords(moveCoords, SnakeMove.DOWN, gameBoard)
    if eMove != SnakeMove.RIGHT:
        adjacentLeft = GetNewCoordsOfMoveFromCoords(moveCoords, SnakeMove.LEFT, gameBoard)

    youSnakeLength = gameBoard.GetSnakeLength(youSnakeId)

    eaten = CouldPosEatYou(adjacentUp, youSnakeLength, gameBoard)
    if eaten:
        print("We could get eaten!! Up")
        return True
    eaten = CouldPosEatYou(adjacentRight, youSnakeLength, gameBoard)
    if eaten:
        print("We could get eaten!! Right")
        return True
    eaten = CouldPosEatYou(adjacentDown, youSnakeLength, gameBoard)
    if eaten:
        print("We could get eaten!! Down")
        return True
    eaten = CouldPosEatYou(adjacentLeft, youSnakeLength, gameBoard)
    if eaten:
        print("We could get eaten!! Left")
        return True
    return False

################################################
# Helper function for FlagReachableCells
def WorthRecursing_FlagReachableCells(x, y, gameBoard):
    newCell = gameBoard.board[x][y]
    return newCell.metadata is False and (newCell.state == CellState.EMPTY or newCell.state == CellState.FOOD)

################################################
# Recursive helper function for ReachableCells
def FlagReachableCells(x, y, gameBoard):
    gameBoard.board[x][y].metadata = True   # Validation for this cell happens before call to this function

    # Check Up
    if y > 0:
        newY = y - 1
        if WorthRecursing_FlagReachableCells(x, newY, gameBoard):
            FlagReachableCells(x, newY, gameBoard)

    # Check Right
    if x < (gameBoard.width - 1):
        newX = x + 1
        if WorthRecursing_FlagReachableCells(newX, y, gameBoard):
            FlagReachableCells(newX, y, gameBoard)

    # Check Down
    if y < (gameBoard.height - 1):
        newY = y + 1
        if WorthRecursing_FlagReachableCells(x, newY, gameBoard):
            FlagReachableCells(x, newY, gameBoard)

    # Check Left
    if x > 0:
        newX = x - 1
        if WorthRecursing_FlagReachableCells(newX, y, gameBoard):
            FlagReachableCells(newX, y, gameBoard)

################################################
def CountReachableCells(gameBoard):
    count = 0
    for cells in gameBoard.board:
        for cell in cells:
            if cell.metadata is True:
                count += 1
    return count

################################################
def PrintReachableCellState(cell, snakeId, simpleSnakeIds):
    strMsg = ""
    if cell.state == CellState.EMPTY or cell.state == CellState.FOOD:
        if cell.metadata is True:
            strMsg += "t"
        else:
            strMsg += "f"
    else:   #cell.state == CellState.SNAKE
        if cell.metadata is True:
            strMsg += "n"
        else:
            if cell.snakePart.IsHead():
                strMsg += "H"
            elif cell.snakePart.IsTail():
                strMsg += "T"
            else:
                if cell.snakePart.snakeData.id == snakeId:
                    strMsg += "Y"
                else:
                    strMsg += str(simpleSnakeIds[cell.snakePart.snakeData.id])
    return strMsg

################################################
def PrintReachableState(gameBoard, snakeId, simpleSnakeIds):
    PrintBoard(gameBoard, snakeId, simpleSnakeIds, PrintReachableCellState)

################################################
# Returns count of open cells reachable from the
# given cell coordinate (including the cell itself)
def GetReachableCellsCountFromCoord(x, y, gameBoard, snakeId, simpleSnakeIds):
    gameBoardTracking = gameBoard.DuplicateGameBoard()
    # We're going to use the cell.metadata field as a boolean
    # True is reachable, False is not.
    # So all we need to do is flag the reachable ones, then count

    # Start with everything unreachable
    for cells in gameBoardTracking.board:
        for cell in cells:
            cell.metadata = False

    FlagReachableCells(x, y, gameBoardTracking)

#    PrintReachableState(gameBoardTracking, snakeId, simpleSnakeIds)

    return CountReachableCells(gameBoardTracking)

################################################
# Returns count of open cells reachable from the
# the move (including the moved to cell itself)
def GetReachableCellsCountForMove(snakeMove, gameBoard, snakeId, simpleSnakeIds):
    coords = GetCoordsOfMove(snakeMove, gameBoard, snakeId)
    if coords is None:
        return 0

    return GetReachableCellsCountFromCoord(coords[0], coords[1], gameBoard, snakeId, simpleSnakeIds)

################################################
def GetValidMovesFromXY(x, y, gameBoard, snakeId):
    moves = []
    directions = [SnakeMove.UP, SnakeMove.RIGHT, SnakeMove.DOWN, SnakeMove.LEFT]
    for eMove in directions:
        if IsValidMoveFromXY(x, y, eMove, gameBoard, snakeId):
            coords = GetNewCoordsOfMoveFromXY(x, y, eMove, gameBoard)
            moves.append(CoordsOfMove(coords, eMove))

    return moves

################################################
def GetValidMoves(gameBoard, snakeId):
    snakeHeadPos = gameBoard.GetSnakeHead(snakeId)
    if snakeHeadPos is None:
        return

    headX = snakeHeadPos['x']
    headY = snakeHeadPos['y']

    return GetValidMovesFromXY(headX, headY, gameBoard, snakeId)

