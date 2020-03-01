import json
import os
import random

import bottle
from bottle import HTTPResponse

import Util
from Util import *
import GameState
from GameState import *
import SnakeLogic1
from SnakeLogic1 import *


g_gameStates = {}

################################################
def AddGame(gameData):
    global g_gameStates

    game = gameData['game']
    gameId = game['id']
    board = gameData['board']
    g_gameStates[gameId] = GameState(gameId, board['width'], board['height'], board['snakes'])

    you = gameData['you']
    print("New Game you ", you['id'])

    return gameId

################################################
def GetSnakeId(gameData):
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

    gameId = AddGame(gameData)

    gameBoard = GameBoard()
    gameBoard.InitFromGameData(gameData)
    snakeId = GetSnakeId(gameData)
    PrintBoard(gameBoard, snakeId, g_gameStates[gameId].simpleSnakeIds)

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

    move = None

    game = gameData['game']
    gameId = game['id']
    if gameId in g_gameStates:
        gameState = g_gameStates[gameId]

        snakeId = GetSnakeId(gameData)
        print("Move you ", snakeId)

        gameBoard = GameBoard()
        gameBoard.InitFromGameData(gameData)
        PrintBoard(gameBoard, snakeId, g_gameStates[gameId].simpleSnakeIds)

        eMove = ChooseMove_2(gameState, gameBoard, snakeId)
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
