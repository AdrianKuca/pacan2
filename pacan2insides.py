import json

import numpy as np
import tensorflow as tf
import boardOps
# tf.enable_eager_execution()
# sequenceLength - długość poszczególnej gry


def fromClasses(tensor):
    tensor = tensor.numpy()[0]
    start = boardOps.topSignature[np.argmax(
        tensor[0:8])] + boardOps.leftSignature[np.argmax(tensor[8:16])]
    end = boardOps.topSignature[np.argmax(
        tensor[16:24])] + boardOps.leftSignature[np.argmax(tensor[24:32])]
    return start + " " + end


def buildModel(rnnUnits, batchSize, inputSize=64, outputSize=32):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(inputSize))
    model.add(tf.keras.layers.Dense(rnnUnits))
    model.add(tf.keras.layers.Dense(rnnUnits))
    model.add(tf.keras.layers.Dense(outputSize))
    return model


inputSet = np.load("input.npy", allow_pickle=True)
outputSet = np.load("output.npy", allow_pickle=True)
dataset = tf.data.Dataset.from_tensor_slices((inputSet, outputSet))


def loss(labels, outputs):
    return tf.keras.losses.categorical_crossentropy(labels, outputs)


examplesPerEpoch = 3000
EPOCHS = 10
batchSize = 10
units = 1024

predictionModel = buildModel(units, 1)
model = buildModel(units, batchSize)
model.compile(tf.optimizers.Adam(), loss)
checkpointDir = "./czk"
checkpointCallback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpointDir+"/checkpoint{epoch}", save_weights_only=True)

if tf.train.latest_checkpoint(checkpointDir) != None:
    if input(tf.train.latest_checkpoint(checkpointDir)+" load? y/n: ") == "y":
        model.load_weights(tf.train.latest_checkpoint(checkpointDir))

datasetBatch = dataset.shuffle(10000).batch(batchSize, drop_remainder=True)
history = model.fit(datasetBatch.repeat(), epochs=EPOCHS,
                    steps_per_epoch=examplesPerEpoch, callbacks=[checkpointCallback])
print(history.history["loss"])
# model.set_weights(model.get_weights())
starting = boardOps.unrollBoard(
    boardOps.getBoard(boardOps.startingPos))
starting = tf.expand_dims(starting, 0)
output = model(starting)
boardOps.draw(boardOps.startingPos)
print(fromClasses(output))
