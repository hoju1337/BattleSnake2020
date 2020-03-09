import json
import os
import random

import bottle
from bottle import HTTPResponse

from Util import *
from GameState import *
from SnakeLogic1 import *
from SnakeLogic3 import *


################################################
def GetYouSnakeId(gameData):
    you = gameData['you']
    return you['id']

################################################
def GetSimpleSnakeIds(gameData):
    snakeIds = []
    for snake in gameData['board']['snakes']:
        snakeIds.append(snake['id'])

    snakeIds.sort()
    # Make id version of the snake GUIDs that will persist across calls to /move
    simpleSnakeIds = {}
    simpleSnakeId = 1
    for snakeId in snakeIds:
        simpleSnakeIds[snakeId] = simpleSnakeId
        simpleSnakeId += 1

    return simpleSnakeIds

################################################
################################################
###########  Bottle request handlers  ##########
################################################
################################################

@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    gameData = bottle.request.json
#    print("START:", json.dumps(gameData))

    gameBoard = GameBoard()
    gameBoard.InitFromGameData(gameData)

    youSnakeId = GetYouSnakeId(gameData)
    PrintBoard(gameBoard, youSnakeId, GetSimpleSnakeIds(gameData))

    response = {"color": RandomColor(), "headType": RandomHead(), "tailType": RandomTail()}

    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    gameData = bottle.request.json
#    print("MOVE:", json.dumps(gameData))

    move = None
    youSnakeId = GetYouSnakeId(gameData)
    print(youSnakeId, "turn---------------------------------------------------------")
    simpleSnakeIds = GetSimpleSnakeIds(gameData)

    gameBoard = GameBoard()
    gameBoard.InitFromGameData(gameData)
    PrintBoard(gameBoard, youSnakeId, simpleSnakeIds)

    eMove = ChooseMove_3(gameBoard, youSnakeId, simpleSnakeIds)
#    eMove = ChooseMove_2(gameBoard, youSnakeId)
    if eMove is not None:
        move = MoveEnumToText(eMove)

    # Shouldn't happen, but if it does just choose a random direction
    if move is None:
        directions = ["up", "down", "left", "right"]
        move = random.choice(directions)

    print(youSnakeId, "Moving", move, "------------------------------------------------")

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    gameData = bottle.request.json
#    print("END:", json.dumps(gameData))

    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()



#example game start
#START:
#{
#  "game":
#    {"id": "720f6d99-7b70-499a-baae-42e8e671a268"},
#  "turn": 0,
#  "board":
#    {
#      "height": 15,
#      "width": 15,
#      "food":
#        [
#          {"x": 4,  "y": 0},
#          {"x": 5,  "y": 11},
#          {"x": 14, "y": 4},
#          {"x": 10, "y": 8},
#          {"x": 3,  "y": 11},
#          {"x": 10, "y": 6},
#          {"x": 2,  "y": 7},
#          {"x": 10, "y": 11},
#          {"x": 13, "y": 2},
#          {"x": 4,  "y": 8}
#        ],
#      "snakes":
#        [
#          {
#            "id": "cb08415a-af82-4bee-87b8-5cd5f32ab6b7",
#            "name": "1",
#            "health": 100,
#            "body": [{"x": 5, "y": 8}, {"x": 5, "y": 8}, {"x": 5, "y": 8}]
#          },
#          {
#            "id": "7aad0a97-21fc-4244-8845-c1fbdabb06e4",
#            "name": "1",
#            "health": 100,
#            "body": [{"x": 14, "y": 13}, {"x": 14, "y": 13}, {"x": 14, "y": 13}]
#          }
#        ]
#    },
#  "you":
#    {
#      "id": "cb08415a-af82-4bee-87b8-5cd5f32ab6b7",
#      "name": "1",
#      "health": 100,
#      "body": [{"x": 5, "y": 8}, {"x": 5, "y": 8}, {"x": 5, "y": 8}]
#    }
#}
