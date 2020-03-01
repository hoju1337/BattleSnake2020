import Util
from Util import *
import GameState
from GameState import *
import SnakeUtil
from SnakeUtil import *

################################################
#####  Just pick a random valid direction  #####
def ChooseMove_1(gameState, gameBoard, youSnakeId):
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

    if eMove is None:
        print("no move")
    return eMove

################################################
##########  Always eat nearest food   ##########
def ChooseMove_2(gameState, gameBoard, youSnakeId):
    nearestFood = FindNearestFoodToSnake(gameBoard, youSnakeId)
    eMove = GetMoveTowardsPoint(nearestFood[0], nearestFood[1], gameBoard, youSnakeId)
    if eMove is None:
        eMove = ChooseMove_1(gameState, gameBoard, youSnakeId)
    return eMove