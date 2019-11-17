import pacan2
import boardOps as bo
import copy
alerts = []
positions = copy.deepcopy(bo.startingPos)
historyPositions = []
historyKills = {"white": [], "black": []}
kills = {"white": [], "black": []}
twoSquares = False


def clear():
    print("\n"*100)


def alert(a):
    alerts.append(a)


def space(a=1):
    return " "*a


def block(a=1):
    return u"\u2588"*a


def playerTurn(color, ai):
    global positions, twoSquares
    valid = False
    target = " "
    sMove = ""
    p = copy.deepcopy(positions)
    if not ai:
        while not valid:
            sMove = input("Gracz: " if color == "white" else "Pacan2: ")
            if len(sMove) < 2:
                while len(sMove) < 2:
                    sMove = input("Gracz: " if color ==
                                  "white" else "Pacan2: ")
            valid, positions, target, check, mate, twoSquares = bo.liMove(
                sMove, positions, True if color == "white" else False, twoSquares)
    alert("Gracz: " + sMove) if color == "white" else alert("Pacan2: " + sMove)
    historyPositions.append(p)
    historyKills[color].append(kills[color])
    if target != " ":
        kills[color].append(target)


def manage():
    global positions
    command = ""
    command = input("Komenda: ")
    if command == "back":
        positions = historyPositions.pop()
        blackKills = historyBlackKills.pop()
        whiteKills = historyWhiteKills.pop()
        return 1
    else:
        return 2


state = 0
turn = 0
while(True):
    clear()
    for a in alerts:
        print(a)
    print("\n")
    bo.draw(positions, 3, turn, kills["white"], kills["black"])
    if state == 0:
        turn += 1
        playerTurn("white", False)
        state += 1
    elif state == 1:
        state = manage()
    elif state == 2:
        playerTurn("black", False)
        state = 0
