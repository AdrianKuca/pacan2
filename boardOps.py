import copy
import boardOpsInside as boi
topSignature = "abcdefgh"
topSignatureV = "A B C D E F G H"
leftSignature = "87654321"
startingPos = {"white": {"R": ["a1", "h1"], "N": [
    "b1", "g1"], "B": ["c1", "f1"], "Q": ["d1"], "K": ["e1"], "P": ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]},
    "black": {"R": ["a8", "h8"], "N": [
        "b8", "g8"], "B": ["c8", "f8"], "Q": ["d8"], "K": ["e8"], "P": ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]}}


def getEmptyBoard():
    board = []
    for y in range(0, 8):
        board.append([])
        for x in range(0, 8):
            board[y].append(" ")
    return board


def getBoard(positions):
    board = getEmptyBoard()
    for color in ["white", "black"]:
        for pawn in positions[color]:
            for square in positions[color][pawn]:
                if color == "black":
                    board[leftSignature.find(
                        square[1])][topSignature.find(square[0])] = pawn
                else:
                    board[leftSignature.find(square[1])][topSignature.find(
                        square[0])] = pawn.lower()
    return board


def liMove(move, positions, white, possiblePassant):
    start = ""
    end = ""
    sColor = "white" if white else "black"
    opposite = "white" if not white else "black"
    forward = 1 if white else -1
    advance = " "
    check = False
    mate = False
    twoSquares = False
    a = move.replace("+", "")
    if a != move:
        move = a
        check = True
    a = move.replace("#", "")
    if a != move:
        move = a
        mate = True
    a = move.replace("=", "")
    if a != move:
        move = a[0:len(a)-1]
        advance = a[len(a)-1: len(a)]
    if move == "O-O-O":  # roszada królowa long
        i = boi.castlingCheck(positions[sColor], False, white)
        if i is None:
            return False, positions, " ", check, mate, twoSquares
        start = positions[sColor]["R"][i]
        positions[sColor]["R"][i] = topSignature[topSignature.find(
            positions[sColor]["R"][i][0])+3]+positions[sColor]["R"][i][1]
        end = positions[sColor]["R"][i]

        start = positions[sColor]["K"][0]
        positions[sColor]["K"][0] = topSignature[topSignature.find(
            positions[sColor]["K"][0][0])-2]+positions[sColor]["K"][0][1]
        end = positions[sColor]["K"][0]
        return True, positions, " ", check, mate, twoSquares, start, end
    elif move == "O-O":  # ROSZADA KRÓL short
        i = boi.castlingCheck(positions[sColor], True, white)
        if i is None:
            return False, positions, " ", check, mate, twoSquares
        start = positions[sColor]["R"][i]
        positions[sColor]["R"][i] = topSignature[topSignature.find(
            positions[sColor]["R"][i][0])-2]+positions[sColor]["R"][i][1]
        end = positions[sColor]["R"][i]

        start = positions[sColor]["K"][0]
        positions[sColor]["K"][0] = topSignature[topSignature.find(
            positions[sColor]["K"][0][0])+2]+positions[sColor]["K"][0][1]
        end = positions[sColor]["K"][0]
        return True, positions, " ", check, mate, twoSquares, start, end
    else:  # nie pachoł Rd4 Rdd3 R6a5 Rxd4 Rfxd8 R6xd8
        hit = False
        a = move.replace("x", "")
        if a != move:
            move = a
            hit = True
        pawn = "P" if "RNKQB".find(move[0]) == -1 else move[0]  # R
        move = move if pawn == "P" else move[1:len(move)]  # d4
        i = boi.pawnPosCheck(
            pawn, move, positions[sColor][pawn], forward, positions, white, hit)
        if i is None:
            return False, positions, " ", check, mate, twoSquares
        start = positions[sColor][pawn][i]
        end = move[len(move)-2: len(move)]
        target = boi.getPawn(end, positions)
        positions[sColor][pawn][i] = end
        if hit:
            if possiblePassant != False:
                if pawn == "P" and possiblePassant[1] == start[1] and possiblePassant[0] == end[0]:
                    s, s, j = boi.findPawn(possiblePassant, positions)
                    positions[opposite]["P"].pop(j)
            for letter in "PRNKQB":
                j = 0
                for p in positions[opposite][letter]:
                    if p == end:
                        positions[opposite][letter].pop(j)
                        break
                    j += 1

    if advance != " ":
        positions[sColor][advance].append(end)
        j = 0
        for p in positions[sColor]["P"]:
            if p == end:
                positions[sColor]["P"].pop(j)
                break
            j += 1
    if pawn == "P" and int(end[1]) == int(start[1]) + forward + forward:
        twoSquares = end
    return True, positions, target, check, mate, twoSquares  # start, end


def unrollBoard(board):
    newBoard = []
    for line in board:
        for square in line:
            if square == "R":
                newBoard.append(0.5)
            elif square == "N":
                newBoard.append(0.3)
            elif square == "B":
                newBoard.append(0.4)
            elif square == "Q":
                newBoard.append(0.9)
            elif square == "K":
                newBoard.append(0.2)
            elif square == "P":
                newBoard.append(-0.1)
            elif square == "r":
                newBoard.append(-0.5)
            elif square == "n":
                newBoard.append(-0.3)
            elif square == "b":
                newBoard.append(-0.4)
            elif square == "q":
                newBoard.append(-0.9)
            elif square == "k":
                newBoard.append(-0.2)
            elif square == "p":
                newBoard.append(-0.1)
            else:
                newBoard.append(0)
    return newBoard


def space(a=1):
    return " "*a


def getPossibleMoves(positions, white):
    possibleMoves = []
    if white == True:
        for pawnType in positions["white"].items():
            if len(pawnType):
                for pawnPosition in pawnType:
                    moves = boi.getAnArrayOfPossibleFigureMoves(
                        pawnPosition, pawnType)
                    possibleMoves.extend(moves)


def draw(positions, frame=3, turn=0, whiteKills="", blackKills=""):
    print("{:0>3}".format(turn)+" "+topSignatureV + "\n")
    i = 0
    board = getBoard(positions)
    for line in board:
        if i == 0:
            print(leftSignature[i] + space(frame) +
                  " ".join(line) + "  " + "Czarne " + " ".join(blackKills))
        elif i == len(board)-1:
            print(leftSignature[i] + space(frame) +
                  " ".join(line) + "  " + "Białe " + " ".join(whiteKills))
        else:
            print(leftSignature[i] + space(frame) + " ".join(line))
        i += 1
