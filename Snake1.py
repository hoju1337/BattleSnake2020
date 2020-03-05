import json
import os
import random

import bottle
from bottle import HTTPResponse

from Util import *
from GameState import *
from SnakeLogic1 import *


g_gameStates = {}
g_youSnakeId = None     # Debugging helper so we can choose to only have one snake do print outs

################################################
def AddGame(gameData):
    global g_gameStates
    global g_youSnakeId

    game = gameData['game']
    gameId = game['id']
    if gameId not in g_gameStates:
        board = gameData['board']
        g_gameStates[gameId] = GameState(gameId, board['width'], board['height'], board['snakes'])

    you = gameData['you']
    youId = you['id']
    g_gameStates[gameId].youSnakeData[youId] = PersistantSnakeData(youId)

    if g_youSnakeId is None:
        g_youSnakeId = youId
    print("New Game you ", youId)

    return gameId

################################################
def GetYouSnakeId(gameData):
    you = gameData['you']
    return you['id']



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

    global g_gameStates
    global g_youSnakeId

    gameId = AddGame(gameData)

    gameBoard = GameBoard()
    gameBoard.InitFromGameData(gameData)

    youSnakeId = GetYouSnakeId(gameData)
    if g_youSnakeId == youSnakeId:
        PrintBoard(gameBoard, youSnakeId, g_gameStates[gameId].simpleSnakeIds)

    # Remember setup if snake logic needs it
#    ChoseMove_3_Init(gameState, gameBoard, youSnakeId)

    response = {"color": RandomColor(), "headType": RandomHead(), "tailType": RandomTail()}
#    print("setup ", json.dumps(response))

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

    global g_gameStates
    global g_youSnakeId

    move = None

    game = gameData['game']
    gameId = game['id']
    if gameId in g_gameStates:
        gameState = g_gameStates[gameId]

        youSnakeId = GetYouSnakeId(gameData)
        print("Move you ", youSnakeId)

        gameBoard = GameBoard()
        gameBoard.InitFromGameData(gameData)
#        if True:
        if g_youSnakeId == youSnakeId:
            PrintBoard(gameBoard, youSnakeId, g_gameStates[gameId].simpleSnakeIds)

        persistantSnakeData = gameState.youSnakeData[youSnakeId]

        if g_youSnakeId == youSnakeId:
            eMove = ChooseMove_3(gameState, gameBoard, youSnakeId)
        else:
            eMove = ChooseMove_2(gameState, gameBoard, youSnakeId)
        if eMove is not None:
            move = MoveEnumToText(eMove)
            print("Moving", move)
    else:
        print("!!! Failed to find gameId in gameState.  Id =", gameId)
        print("GameStates:", g_gameStates)

    # Shouldn't happen, but if it does just choose a random direction
    if move is None:
        directions = ["up", "down", "left", "right"]
        move = random.choice(directions)

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

    global g_gameStates

    game = gameData['game']
    gameId = game['id']
    if gameId in g_gameStates:
        del g_gameStates[gameId]

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
