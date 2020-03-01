from enum import Enum

#**********************************************#
class GameState:
    def __init__(self, gameId, width, height, snakes):
        self.gameId = gameId
        self.width = width
        self.height = height
        self.simpleSnakeIds = {}

        # Make id version of the snake GUIDs that will persist across calls to /move
        simpleSnakeId = 1
        for snake in snakes:
            self.simpleSnakeIds[snake['id']] = simpleSnakeId
            simpleSnakeId += 1

#**********************************************#
class CellState(Enum):
    EMPTY = 1
    FOOD = 2
    SNAKE = 3

#**********************************************#
class SnakeData:
    def __init__(self, id, health, body):
        self.id = id
        self.health = health
        self.body = body

    ############################################
    def GetHead(self):
        return self.body[0]

    ############################################
    def IsHead(self, x, y):
        head = self.GetHead()
        return head['x'] == x and head['y'] == y

    ############################################
    def GetTail(self):
        return self.body[len(self.body) - 1]

    ############################################
    def IsTail(self, x, y):
        tail = self.GetTail()
        return tail['x'] == x and tail['y'] == y

    ############################################
    def SnakeLength(self):
        return len(self.body)

#**********************************************#
class SnakePart:
    def __init__(self, x, y, snakeData):
        self.x = x
        self.y = y
        self.snakeData = snakeData

    ############################################
    def IsHead(self):
        return self.snakeData.IsHead(self.x, self.y)

    ############################################
    def IsTail(self):
        return self.snakeData.IsTail(self.x, self.y)

#**********************************************#
class GameCell:
    def __init__(self):
        self.state = CellState.EMPTY
        self.snakePart = None

    ############################################
    def DebugPrint(self):
        if self.state == CellState.EMPTY:
            print("EMPTY")
        elif self.state == CellState.FOOD:
            print("FOOD")
        else:
            if self.snakePart is None:
                print("Error: No snake part")
            else:
                if self.snakePart.IsHead():
                    print("Snake HEAD", self.snakePart.snakeData.id)
                elif self.snakePart.IsTail():
                    print("Snake TAIL", self.snakePart.snakeData.id)
                else:
                    print("Snake BODY", self.snakePart.snakeData.id)

#**********************************************#
class GameBoard:
    def __init__(self):
        self.board = None
        self.width = 0
        self.height = 0
        self.snakes = {}
        self.food = []

    ############################################
    def InitFromGameData(self, gameData):
        self.InitFromBoard(gameData['board'])

    ############################################
    def InitFromBoard(self, board):
        self.width = board['width']
        self.height = board['height']
        # Initalize all cells
        self.board = []
        for i in range(self.width):
            cells = []
            for j in range(self.height):
                cells.append(GameCell())
            self.board.append(cells)

        # Add the food
        self.food = board['food']
        for foodPos in self.food:
            self.board[foodPos['x']][foodPos['y']].state = CellState.FOOD

        for snake in board['snakes']:
            snakeId = snake['id']
            body = snake['body']
            snakeData = SnakeData(snakeId, snake['health'], body)
            self.snakes[snakeId] = snakeData
            for bodyPart in body:
                x = bodyPart['x']
                y = bodyPart['y']
                cell = self.board[x][y]
                cell.state = CellState.SNAKE
                cell.snakePart = SnakePart(x, y, snakeData)

    ############################################
    def GetSnake(self, snakeId):
        return self.snakes[snakeId]

    ############################################
    def GetSnakeHead(self, snakeId):
        snake = self.GetSnake(snakeId)
        if snake is None:
            return
        return snake.GetHead()
