

class Position:

    def __init__(self, x, y):
        if self.isPositionInBoard(x, y):
            self.x = x
            self.y = y
        else:
            return None

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        else:
            return False

    @staticmethod
    def isPositionInBoard(self, x, y):
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        else:
            return False

    @staticmethod
    def isCoordInBoard(self, y):
        if y >= 0 and y < 8:
            return True
        else:
            return False


class Figure:
    @staticmethod
    def getPossibleFigureMoves(position):
        raise NotImplementedError

    @staticmethod
    def isPossibleFigureMove(start, end):
        raise NotImplementedError


class Pawn(Figure):
    self.symbol = "P"

    @staticmethod
    def isPossibleFigureMove(start, end, direction):
        return end.x == start.x and (end.y == start.y + direction or end.y == start.y + direction + direction)

    @staticmethod
    def getPossibleFigureMoves(position, forwardNumber):
        possibleMoves = [
            Position(position.x, position.y+forwardNumber),
            Position(position.x, position.y+forwardNumber+forwardNumber)
        ]
        for i in range(0, len(possibleMoves)):
            if possibleMoves[i] is None:
                possibleMoves.pop(i)
        return possibleMoves


class Knight(Figure):
    self.symbol = "N"

    @staticmethod
    def getPossibleFigureMoves(position):
        possibleMoves = [
            Position(position.x+1, position.y+2),
            Position(position.x+2, position.y+1),
            Position(position.x+2, position.y-1),
            Position(position.x+1, position.y-2),
            Position(position.x-1, position.y+2),
            Position(position.x-2, position.y+1),
            Position(position.x-2, position.y-1),
            Position(position.x-1, position.y-2),
        ]
        for i in range(0, len(possibleMoves)):
            if possibleMoves[i] is None:
                possibleMoves.pop(i)
        return possibleMoves


class Rook(Figure):
    self.symbol = "R"

    @staticmethod
    def getPossibleFigureMoves(position):
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

    @staticmethod
    def getPossibleFigureMoves(position):
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

    @staticmethod
    def getPossibleFigureMoves(position):
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

    @staticmethod
    def getPossibleFigureMoves(position):
        possibleMoves = [
            Position(position.x, position.y+1),
            Position(position.x, position.y-1),

            Position(position.x+1, position.y+1),
            Position(position.x+1, position.y),
            Position(position.x+1, position.y-1),

            Position(position.x-1, position.y+1),
            Position(position.x-1, position.y),
            Position(position.x-1, position.y-1),
        ]
        for i in range(0, len(possibleMoves)):
            if possibleMoves[i] is None:
                possibleMoves.pop(i)
        return possibleMoves


class Checker:
    def __init__(self, figure, position, isWhite, forwardNumber):
        self.figure = figure
        self.position = position
        self.isWhite = isWhite
        self.forwardNumber = forwardNumber
        self.isProtectingKing = False
        self.isAttackingKing = False
        self.isVulnerableToPassant = False
        self.recalculatePossibleMoves()

    def recalculatePossibleMoves(self):
        if issubclass(self.figure, Pawn):
            self.figureMoves = self.figure.getPossibleFigureMoves(
                position, self.forwardNumber)
        else:
            self.figureMoves = self.figure.getPossibleFigureMoves(
                position)

    def move(self, position):
        if position is None:
            raise Exception("Position out of board.")
        self.position = position
        recalculatePossibleMoves()


class Board:
            # pionek nie wie gdzie są inne pionki
    pass  # więc liczenie kolizji i bić zostawiamy dla board, która będzie znała pozycje wszystkich pionków
