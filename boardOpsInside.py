import copy
import chessObjects as co
topSignature = "abcdefgh"
topSignatureV = "A B C D E F G H"
leftSignature = "87654321"
startingPos = {
    "white": {
        "R": [co.Position(0, 0), co.Position(7, 0)],
        "N": [co.Position(1, 0), co.Position(6, 0)],
        "B": [co.Position(2, 0), co.Position(5, 0)],
        "Q": [co.Position(3, 0)],
        "K": [co.Position(4, 0)],
        "P": [co.Position(0, 2), co.Position(1, 2), co.Position(2, 2), co.Position(3, 2), co.Position(4, 2), co.Position(5, 2), co.Position(6, 2), co.Position(7, 2)]},
    "black": {
        "R": [co.Position(0, 7), co.Position(7, 7)],
        "N": [co.Position(1, 7), co.Position(6, 7)],
        "B": [co.Position(2, 7), co.Position(5, 7)],
        "Q": [co.Position(3, 7)],
        "K": [co.Position(4, 7)],
        "P": [co.Position(0, 6), co.Position(1, 6), co.Position(2, 6), co.Position(3, 6), co.Position(4, 6), co.Position(5, 6), co.Position(6, 6), co.Position(7, 6)]}}


def findPawn(p, positions):
    for color in ["white", "black"]:
        for pawnType in positions[color]:
            i = 0
            for square in positions[color][pawnType]:
                if square == p:
                    return color, pawnType, i
                i += 1


def getPawnTypeOnPosition(p, positions):
    for color in ["white", "black"]:
        for pawnType in positions[color]:
            for square in positions[color][pawnType]:
                if p == square:
                    return pawnType
    return " "


def isWhiteSquare(position):
    if position.y % 2 == 0 and position.x % 2 == 0:
        return False
    if position.y % 2 == 0 and not position.x % 2 == 0:
        return True
    if not position.y % 2 == 0 and position.x % 2 == 0:
        return True


def skewCollision(startPosition, endPosition, allPositions, hit):
    leftToRight = True if endPosition.x > startPosition.x else False
    topToBottom = True if endPosition.y > startPosition.y else False
    distance = abs(endPosition.x - startPosition.x)

    obstacles = []
    for color in allPositions:
        for pawnType in allPositions[color]:
            for obstacle in allPositions[color][pawnType]:
                for i in range(1, distance+(1 if not hit else 0)):
                    x = i if leftToRight else -i
                    y = i if topToBottom else -i
                    if obstacle.x == startPosition.x+x and obstacle.y == startPosition.y+y:
                        obstacles.append(obstacle)
    if len(obstacles) > 0:
        return True, obstacles
    else:
        return False, []

# Kontynuuj


def hvCollision(start, end, allPositions):
    if start[0] != end[0] and start[1] != end[1]:
        return False, ["error"]
    horizontal = False if start[0] == end[0] else True
    endI = topSignature.find(
        end[0]) if horizontal else leftSignature.find(end[1])
    startI = topSignature.find(
        start[0])if horizontal else leftSignature.find(start[1])
    difference = endI - startI
    right = True if difference > 0 else False
    obstacles = []
    for color in allPositions:
        for pawn in allPositions[color]:
            for p in allPositions[color][pawn]:
                obstacleI = topSignature.find(
                    p[0]) if horizontal else leftSignature.find(p[1])
                if (p[1] == start[1]) if horizontal else (p[0] == start[0]):  # wtedy kod
                    if right:
                        if obstacleI < endI and obstacleI > startI:
                            obstacles.append(p)
                    else:
                        if obstacleI > endI and obstacleI < startI:
                            obstacles.append(p)
    if len(obstacles) > 0:
        return True, obstacles
    else:
        return False, []


# 259, 7, FALSE, NE7


def isKingsProtector(pos, white, allPositions, target):
    color = "white" if white else "black"
    king = allPositions[color]["K"][0]
    enemyColor = "white" if not white else "black"
    enemyPos = allPositions[enemyColor]
    enemyLetters = "RBQ"
    for letter in enemyLetters:
        for enemy in enemyPos[letter]:
            if letter == "R":
                col = hvCollision(enemy, king, allPositions)
                if col[0] == True:
                    if len(col[1]) == 1 and pos == col[1][0] and target != enemy:
                        return True, enemy, letter
            elif letter == "B":
                col = skewCollision(enemy, king, allPositions, True)
                if col[0] == True:
                    if len(col[1]) == 1 and pos == col[1][0] and target != enemy:
                        return True, enemy, letter
            elif letter == "Q":
                col1 = hvCollision(enemy, king, allPositions)
                col2 = skewCollision(enemy, king, allPositions, True)
                col = col1 if col1[0] == True else col2 if col2[0] == True else (
                    False, False)
                if col[0] == True:
                    if len(col[1]) == 1 and pos == col[1][0] and target != enemy:
                        return True, enemy, letter
    return False, False, False


def willProtectKing(pos, letter, enemy, enemyLetter, white, allPositions):
    color = "white" if white else "black"
    king = allPositions[color]["K"][0]
    if enemyLetter == "R":
        col = hvCollision(enemy, king, allPositions)
        if col[0] == True:
            if len(col[1]) == 1 and pos == col[1][0]:
                return True
    elif enemyLetter == "B":
        col = skewCollision(enemy, king, allPositions, True)
        if col[0] == True:
            if len(col[1]) == 1 and pos == col[1][0]:
                return True
    elif enemyLetter == "Q":
        col1 = hvCollision(enemy, king, allPositions)
        col2 = skewCollision(enemy, king, allPositions, True)
        col = col1 if col1[0] == True else col2 if col2[0] == True else (
            False, False)
        if col[0] == True:
            if len(col[1]) == 1 and pos == col[1][0]:
                return True
    return False


def isPossibleKnightMove(start, end):
    x = topSignature.find(start[0])  # 1
    y = leftSignature.find(start[1])  # 7
    x0 = x-2
    x1 = x-1
    x2 = x+1
    x3 = x+2
    y0 = y-2
    y1 = y-1
    y2 = y+1
    y3 = y+2
    moves = [  # ruchy honia
        topSignature[x0] + \
        leftSignature[y2] if x0 <= 7 and x0 >= 0 and y2 >= 0 and y2 <= 7 else " ",
        topSignature[x0] + \
        leftSignature[y1]if x0 <= 7 and x0 >= 0 and y1 >= 0 and y1 <= 7 else " ",
        topSignature[x3] + \
        leftSignature[y2]if x3 <= 7 and x3 >= 0 and y2 >= 0 and y2 <= 7 else " ",
        topSignature[x3] + \
        leftSignature[y1]if x3 <= 7 and x3 >= 0 and y1 >= 0 and y1 <= 7 else " ",
        topSignature[x1] + \
        leftSignature[y3]if x1 <= 7 and x1 >= 0 and y3 >= 0 and y3 <= 7 else " ",
        topSignature[x2] + \
        leftSignature[y3]if x2 <= 7 and x2 >= 0 and y3 >= 0 and y3 <= 7 else " ",
        topSignature[x1] + \
        leftSignature[y0]if x1 <= 7 and x1 >= 0 and y0 >= 0 and y0 <= 7 else " ",
        topSignature[x2] + \
        leftSignature[y0]if x2 <= 7 and x2 >= 0 and y0 >= 0 and y0 <= 7 else " "
    ]
    for m in moves:
        if end == m:
            return True
    return False


def isPossibleBishopMove(start, end, allPositions, hit=False):
    col = skewCollision(start, end, allPositions, hit)
    return isWhiteSquare(end) == isWhiteSquare(start) and col[0] == False and len(col[1]) == 0


def isPossibleTowerMove(start, end, allPositions):
    return (end[0] == start[0] or end[1] == start[1]) and hvCollision(start, end, allPositions)[0] == False


def isPossibleQueenMove(start, end, allPositions, hit):
    return isPossibleBishopMove(start, end, allPositions, hit) or isPossibleTowerMove(start, end, allPositions)


def isPossiblePawnMove(start, end, forward, allPositions):
    return end[0] == start[0] and(int(end[1]) == int(start[1]) + forward or int(end[1]) == int(start[1]) + forward + forward) and hvCollision(start, end, allPositions)[0] == False


def castlingCheck(pos, short, white):
    distance = 3 if short else -4
    for i in range(0, len(pos["R"])):
        if topSignature.find(pos["R"][i][0]) == topSignature.find(pos["K"][0][0]) + distance and pos["R"][i][1] == ("1" if white else "8"):
            return i
    return None


def pawnPosCheck(pawn, move, pos, forward, allPositions, white, hit):
    i = 24
    if pawn == "K":
        return 0
    for i in range(0, len(pos)):
        check, enemy, enemyLetter = isKingsProtector(
            pos[i], white, allPositions, move[len(move)-2:len(move)] if hit else False)
        if check:
            futurePositions = copy.deepcopy(allPositions)
            c, p, j = findPawn(pos[i], allPositions)
            futurePositions[c][pawn][j] = move[len(move)-2:len(move)]
            if not willProtectKing(move[len(move)-2:len(move)], pawn, enemy, enemyLetter, white, futurePositions):
                continue
        if len(move) == 2:
            if pawn == "R" and isPossibleTowerMove(pos[i], move, allPositions):
                return i
            elif pawn == "Q" and isPossibleQueenMove(pos[i], move, allPositions, hit):
                return i
            elif pawn == "N" and isPossibleKnightMove(pos[i], move):
                return i
            elif pawn == "P" and isPossiblePawnMove(pos[i], move, forward, allPositions):
                return i
            elif pawn == "B" and isPossibleBishopMove(pos[i], move, allPositions, hit):
                return i
        else:
            if topSignature.find(move[0]) != -1:  # bc1 b6c1
                if pawn == "P":
                    if move[0] == pos[i][0] and int(move[len(move)-1]) == int(pos[i][1]) + forward:
                        return i
                elif move[0:len(move)-2] == pos[i][0:len(move)-2]:  # bc1
                    return i
            else:  # 5c1
                if move[0] == pos[i][1]:
                    return i

    return None
