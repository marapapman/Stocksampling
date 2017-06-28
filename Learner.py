import pickle
import sqlite3
import numpy as np


conn = sqlite3.connect('Collected.db')
cur = conn.cursor()

cur.execute("select data from StockTable")
for row in cur:
    data=pickle.loads(row[0])
    matrix=np.array(data)
    print(np.sum(matrix))

