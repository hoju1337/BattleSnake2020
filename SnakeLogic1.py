from Util import *
from GameState import *
from SnakeUtil import *
from TurnAnalysisBasic import *


################################################
#####  Just pick a random valid direction  #####
def ChooseMove_1(gameBoard, youSnakeId):
    timerObj = ElapsedTime("ChooseMove_1 time")

    directions = [SnakeMove.UP, SnakeMove.RIGHT, SnakeMove.DOWN, SnakeMove.LEFT]
    eMove = None
    movesTried = []
    while len(movesTried) < 4:
        eMove = random.choice(directions)
        if eMove not in movesTried:
            if IsValidMove(eMove, gameBoard, youSnakeId):
                break
            else:
                movesTried.append(eMove)

#    if eMove is None:
#        print("no move")

    timerObj.EndTiming()

    return eMove

################################################
##########  Always eat nearest food   ##########
def ChooseMove_2(gameBoard, youSnakeId):
    timerObj = ElapsedTime("ChooseMove_2 time")

    nearestFood = FindNearestFoodToSnake(gameBoard, youSnakeId)
    eMove = GetMoveTowardsPoint(nearestFood[0], nearestFood[1], gameBoard, youSnakeId)
    if eMove is None:
        eMove = ChooseMove_1(gameBoard, youSnakeId)

    timerObj.EndTiming()

    return eMove
