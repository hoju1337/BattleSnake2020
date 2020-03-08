from SnakeLogic1 import *
from Util import *
from GameState import *
from SnakeUtil import *
from TurnAnalysisBasic import *



################################################
def AdjustMoveIfTerrible(eMove, gameBoard, youSnakeId, simpleSnakeIds):
    # If we're not about to get eaten and there are at least as many open spaces as
    # our length it's probably a fairly safe move to accept
    possiblyEaten = CouldMoveGetYouEaten(eMove, gameBoard, youSnakeId)
    countWantedMove =  GetReachableCellsCountForMove(eMove, gameBoard, youSnakeId, simpleSnakeIds)
    if not possiblyEaten:
        if countWantedMove > gameBoard.GetSnakeLength(youSnakeId):
            return eMove

    # Let's pick the move with the most open space
    coordsUp = None
    coordsRight = None
    coordsDown = None
    coordsLeft = None
    if IsValidMove(SnakeMove.UP, gameBoard, youSnakeId):
        coordsUp = GetCoordsOfMove(SnakeMove.UP, gameBoard, youSnakeId)
    if IsValidMove(SnakeMove.RIGHT, gameBoard, youSnakeId):
        coordsRight = GetCoordsOfMove(SnakeMove.RIGHT, gameBoard, youSnakeId)
    if IsValidMove(SnakeMove.DOWN, gameBoard, youSnakeId):
        coordsDown = GetCoordsOfMove(SnakeMove.DOWN, gameBoard, youSnakeId)
    if IsValidMove(SnakeMove.LEFT, gameBoard, youSnakeId):
        coordsLeft = GetCoordsOfMove(SnakeMove.LEFT, gameBoard, youSnakeId)

    countUp = 0
    countRight = 0
    countDown = 0
    countLeft = 0

    # Get the open cell count for each direction.
    # For the originally requested direction we've already calculated it.
    if coordsUp is not None:
        if eMove == SnakeMove.UP:
            countUp = countWantedMove
        else:
            countUp = GetReachableCellsCountForMove(SnakeMove.UP, gameBoard, youSnakeId, simpleSnakeIds)
    if coordsRight is not None:
        if eMove == SnakeMove.RIGHT:
            countRight = countWantedMove
        else:
            countRight = GetReachableCellsCountForMove(SnakeMove.RIGHT, gameBoard, youSnakeId, simpleSnakeIds)
    if coordsDown is not None:
        if eMove == SnakeMove.DOWN:
            countDown = countWantedMove
        else:
            countDown = GetReachableCellsCountForMove(SnakeMove.DOWN, gameBoard, youSnakeId, simpleSnakeIds)
    if coordsLeft is not None:
        if eMove == SnakeMove.LEFT:
            countLeft = countWantedMove
        else:
            countLeft = GetReachableCellsCountForMove(SnakeMove.LEFT, gameBoard, youSnakeId, simpleSnakeIds)

    # Collect all the counts so we can sort them.  Don't include the requested direction
    # because we already know we don't really like it
    moves = []
    if coordsUp is not None:
        if eMove != SnakeMove.UP:
            moves.append([countUp, SnakeMove.UP])
    if coordsRight is not None:
        if eMove != SnakeMove.UP:
            moves.append([countRight, SnakeMove.RIGHT])
    if coordsDown is not None:
        if eMove != SnakeMove.UP:
            moves.append([countDown, SnakeMove.DOWN])
    if coordsLeft is not None:
        if eMove != SnakeMove.UP:
            moves.append([countLeft, SnakeMove.LEFT])

    if len(moves) > 0:
        # Sort from most space to least
        moves.sort(key = lambda val: val[0], reverse = True)
        for i in range(len(moves)):
            newMove = moves[i][1]
            if not CouldMoveGetYouEaten(newMove, gameBoard, youSnakeId):
                return newMove

        # Uhh seems like every move will or might get you killed.  Hope for the best
        return moves[0][1]

    # Options all look bad, go with the original
    return eMove

################################################
def GetKillMove(gameBoard, youSnakeId):
    youSnakeMoves = GetValidMoves(gameBoard, youSnakeId)
    if len(youSnakeMoves) == 0:
        return

    killMove = None
    killMoveSnakeSize = 0
    directions = [SnakeMove.UP, SnakeMove.RIGHT, SnakeMove.DOWN, SnakeMove.LEFT]
    ourSnakeLen = gameBoard.GetSnakeLength(youSnakeId)
    for coordOfMove in youSnakeMoves:
        for eMove in directions:    # Test all the directions
            coordsOfAdjacent = GetNewCoordsOfMoveFromXY(coordOfMove.x, coordOfMove.y, eMove, gameBoard)
            # Is this a valid direction and does it have a snake head (that isn't us)?
            if coordsOfAdjacent is not None:
                cell = gameBoard.board[coordsOfAdjacent[0]][coordsOfAdjacent[1]]
                if cell.state == CellState.SNAKE and cell.snakePart.GetSnakeId() != youSnakeId:
                    if cell.snakePart.IsHead():
                        # We have a snake head (that isn't us) that could potentially move
                        # into a cell we can move into.  Is that move its only option and
                        # would we kill it if we both moved there?
                        otherSnakeLen = cell.snakePart.SnakeLength()
                        if otherSnakeLen < ourSnakeLen:
                            otherSnakeMoves = GetValidMoves(gameBoard, cell.snakePart.GetSnakeId())
                            if len(otherSnakeMoves) == 1:
                                # We have a snake we can kill!  But is it the biggest snake we can kill?
                                if otherSnakeLen > killMoveSnakeSize:
                                    killMove = eMove
                                    killMoveSnakeSize = otherSnakeLen

#    if killMove is not None:
#        print("We're going for the kill!!!!!")
    return killMove


################################################
##########  dunno yet   ##########
def ChooseMove_3(gameState, gameBoard, youSnakeId, simpleSnakeIds):
    timerObj = ElapsedTime("ChooseMove_3 time")

#    persistentData = gameState.youSnakeData[youSnakeId]
#    allSnakeTurns = AnalyseMoves(persistentData, gameBoard, gameState)

    eMove = GetKillMove(gameBoard, youSnakeId)
    if eMove is not None and not CouldMoveGetYouEaten(eMove, gameBoard, youSnakeId):
        return eMove

    # Doing ChooseMove_2 for now
    nearestFood = FindNearestFoodToSnake(gameBoard, youSnakeId)
    eMove = GetMoveTowardsPoint(nearestFood[0], nearestFood[1], gameBoard, youSnakeId)
    if eMove is None:
        eMove = ChooseMove_1(gameState, gameBoard, youSnakeId)

    if eMove is not None:
        eMove = AdjustMoveIfTerrible(eMove, gameBoard, youSnakeId, simpleSnakeIds)
#        count = GetReachableCellsCountForMove(eMove, gameBoard, youSnakeId, simpleSnakeIds)
#        print("Reachable cell count =", count)

    timerObj.EndTiming()

    return eMove
