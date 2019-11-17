class Board:
    leftSignature = "87654321"
    topSignatureV = "A B C D E F G H"

    def __init__(self):
        self.positions = {"white": {"R": [co.Position(0, 0), co.Position(7, 0)], "N": [
            "b1", "g1"], "B": ["c1", "f1"], "Q": ["d1"], "K": ["e1"], "P": ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]},
            "black": {"R": ["a8", "h8"], "N": [
                "b8", "g8"], "B": ["c8", "f8"], "Q": ["d8"], "K": ["e8"], "P": ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]}}


class Position:
    def __init__(self, x, y):
        if isPositionInBoard(x, y):
            self.x = x
            self.y = y
        else:
            raise Exception("Position out of board")

    def isPositionInBoard(self, x, y):
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        else:
            return False

    def checkLengthOfTheMove(self, lengthOfTheMove):
        if lengthOfTheMove <= 0:
            raise Exception("Length of the move cant be zero nor negative")

    def getForward(self, white):
        if white:
            forward = 1
        else:
            forward = -1

    def moveForward(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionY = self.y + lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(self.x, newPositionY):
            self.y = newPositionY

    def moveBackward(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionY = self.y - lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(self.x, newPositionY):
            self.y = newPositionY

    def moveRight(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x + lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, self.y):
            self.x = newPositionX

    def moveLeft(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x - lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, self.y):
            self.x = newPositionX

    def moveSkewForwardRight(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x + lengthOfTheMove * self.getForward(white)
        newPositionY = self.y + lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, newPositionY):
            self.y = newPositionY
            self.x = newPositionX

    def moveSkewForwardLeft(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x - lengthOfTheMove * self.getForward(white)
        newPositionY = self.y + lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, newPositionY):
            self.y = newPositionY
            self.x = newPositionX

    def moveSkewBackwardRight(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x + lengthOfTheMove * self.getForward(white)
        newPositionY = self.y - lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, newPositionY):
            self.y = newPositionY
            self.x = newPositionX

    def moveSkewBackwardLeft(self, lengthOfTheMove, white):
        self.checkLengthOfTheMove(lengthOfTheMove)
        newPositionX = self.x - lengthOfTheMove * self.getForward(white)
        newPositionY = self.y - lengthOfTheMove * self.getForward(white)
        if self.isPositionInBoard(newPositionX, newPositionY):
            self.y = newPositionY
            self.x = newPositionX
