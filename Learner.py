import pickle
import sqlite3


conn = sqlite3.connect('Data.db')
cur = conn.cursor()

cur.execute("select data from Stockdata")
for row in cur:
    print(pickle.loads(row[0]))

