import pickle
import sqlite3
import numpy as np

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
import keras

conn = sqlite3.connect('Collected.db')
cur = conn.cursor()

cur.execute("select data, tag from StockTable")
training=[]
tags=[]
for row in cur:
    data=pickle.loads(row[0])
    tag=row[1]
    tags.append(tag)
    matrix=np.array(data)
    matrix=np.reshape(matrix,43*29)
    training.append(matrix)

X=np.array(training)
Y = np_utils.to_categorical(tags,4)

model = Sequential()
model.add(Dense(300, input_dim=43*29, activation='tanh'))
model.add(Dense(100, activation='tanh'))

model.add(Dense(4, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y,
          batch_size=64,
          nb_epoch=200,
          verbose=1,
          validation_split=0.1
          )