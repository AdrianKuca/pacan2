import numpy


class Position:
    @property
    def x(self):
        return self.coordinates[0]

    @x.setter
    def x(self, a):
        if self.isCoordInBoard():
            self.coordinates[0] = a
        else:
            raise Exception("X out of board")

    @property
    def y(self):
        return self.coordinates[1]

    @y.setter
    def y(self, a):
        if self.isCoordInBoard():
            self.coordinates[1] = a
        else:
            raise Exception("Y out of board")

    def __init__(self, x, y):
        if self.isPositionInBoard(x, y):
            self.coordinates = numpy.array([x, y])
        else:
            return None
            # raise Exception("Position out of board")

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        else:
            return False

    def isPositionInBoard(self, x, y):
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        else:
            return False

    def isCoordInBoard(self, y):
        if y >= 0 and y < 8:
            return True
        else:
            return False


class Figure:
    def recalculatePossibleFigureMoves(self, position):
        raise NotImplementedError

    def isPossibleFigureMove(self, start, end):
        raise NotImplementedError


class Pawn(Figure):
    self.symbol = "P"

    def isPossibleFigureMove(self, start, end, direction):
        return end.x == start.x and (end.y == start.y + direction or end.x == start.y + direction + direction)

    def recalculatePossibleFigureMoves(self, position, direction):
        return [
            Position(position.x, position.y+direction),
            Position(position.x, position.y+direction+direction),
            Position(position.x+1, position.y+direction),
            Position(position.x-1, position.y+direction)
        ]


class Knight(Figure):
    self.symbol = "N"

    def recalculatePossibleFigureMoves(self, position):
        return [
            Position(position.x+1, position.y+2),
            Position(position.x+2, position.y+1),
            Position(position.x+2, position.y-1),
            Position(position.x+1, position.y-2),
            Position(position.x-1, position.y+2),
            Position(position.x-2, position.y+1),
            Position(position.x-2, position.y-1),
            Position(position.x-1, position.y-2),
        ]


class Rook(Figure):
    self.symbol = "R"

    def recalculatePossibleFigureMoves(self, position):
        possibleMoves = []
        for i in range(0, 8):
            if position.x != i:
                possibleMoves.append(Position(i, position.y))
        for j in range(0, 8):
            if position.y != j:
                possibleMoves.append(Position(position.x, j))
        return possibleMoves


class Bishop(Figure):
    self.symbol = "B"

    def recalculatePossibleFigureMoves(self, position):
        possibleMoves = []
        for i in range(1, 8 - position.x):
            possibleMoves.append(Position(position.x + i, position.y + i))
        for i in range(1, position.x):
            possibleMoves.append(Position(position.x - i, position.y - i))
        for i in range(1, 8 - position.x):
            possibleMoves.append(Position(position.x + i, position.y - i))
        for i in range(1, position.x):
            possibleMoves.append(Position(position.x - i, position.y + i))
        return possibleMoves


class Queen(Figure):
    self.symbol = "Q"

    def recalculatePossibleFigureMoves(self, position):
        possibleMoves = []
        for i in range(1, 8 - position.x):
            possibleMoves.append(Position(position.x + i, position.y + i))
        for i in range(1, position.x):
            possibleMoves.append(Position(position.x - i, position.y - i))
        for i in range(1, 8 - position.x):
            possibleMoves.append(Position(position.x + i, position.y - i))
        for i in range(1, position.x):
            possibleMoves.append(Position(position.x - i, position.y + i))
        for i in range(0, 8):
            if position.x != i:
                possibleMoves.append(Position(i, position.y))
        for j in range(0, 8):
            if position.y != j:
                possibleMoves.append(Position(position.x, j))
        return possibleMoves


class King(Figure):
    self.symbol = "K"

    def recalculatePossibleFigureMoves(self, position):
        return [
            Position(position.x, position.y+1),
            Position(position.x, position.y-1),

            Position(position.x+1, position.y+1),
            Position(position.x+1, position.y),
            Position(position.x+1, position.y-1),

            Position(position.x-1, position.y+1),
            Position(position.x-1, position.y),
            Position(position.x-1, position.y-1),
        ]


class Checker:
    def __init__(self, figure, position, color, facing):
        self.figure = figure
        self.position = position
        self.color = color
        self.facing = facing
        self.isProtectingKing = False
        self.isAttackingKing = False
        self.recalculatePossibleMoves()

    def recalculatePossibleMoves(self):
        self.figureMoves = self.figure.recalculatePossibleMoves(
            position)  # pionek nie wie gdzie są inne pionki

    def move(self):
        #move and then
        recalculatePossibleMoves()


class Board:
    pass  # więc liczenie kolizji zostawiamy dla board, która będzie znała pozycje wszystkich pionków
