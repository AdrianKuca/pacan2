
import numpy
import encodings
import json
import copy
import boardOps as bo
import pandas as pd
import tensorflow as tf


def toClasses(a):
    sixteen = [0]*16
    for i in range(0, 16):
        if i == a[0] or i == a[1]+8:
            sixteen[i] = 1
    return sixteen


frame = pd.read_csv("games.csv", usecols=[4, 6, 12])
frame = frame.to_dict(orient="records")
myFrame = numpy.empty((20058, 2), dtype=object)

inputValues = []
outputValues = []
n = 0
for example in frame:
    positions = copy.deepcopy(bo.startingPos)
    moves = example["moves"].split(" ")
    white = True
    turn = 1
    twoSquares = False
    oneGameInput = []
    if n % 1000 == 0:
        print(n, turn, white)
    m = 0
    while m < len(moves):
        oneGameInput.append(bo.unrollBoard(bo.getBoard(positions)))
        valid, positions, target, check, mate, twoSquares, start, end = bo.liMove(
            moves[m], positions, white, twoSquares)
        # outputValues.append(toClasses([bo.topSignature.find(start[0]), int(start[1])]) + toClasses([
        #    bo.topSignature.find(end[0]), int(end[1])]))
        white = not white
        if white:
            turn += 1
        m += 1
        inputValues.append(copy.deepcopy(oneGameInput))
    n += 1
inputValues = numpy.array(inputValues)
outputValues = numpy.array(outputValues)
numpy.save("inputSequences.npy", inputValues, True)
#numpy.save("output.npy", outputValues, True)
# deepcopy do input values!
# tylko na WIĘCEJ MOCY
# output ten sam
