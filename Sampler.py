import pandas_datareader.data as web
import datetime
import random
import sqlite3
import time
import numpy as np
import io
import pickle
import talib
def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y', prop)

def loadSymboles():
    list = []
    with open('constituents.csv', "r") as csvfile:
        for row in csvfile:
            symbol=row.split(",")[0]
            if symbol != 'Symbol':
                list.append(symbol)
    return list
def Download(list):
    start=datetime.datetime.strptime("1/1/2006",'%m/%d/%Y');
    end=datetime.datetime.strptime("06/07/2017",'%m/%d/%Y');
    for symbol in list:
        try:
            data = web.DataReader(symbol, 'google', start, end)
            data.to_csv('./stockhist/'+symbol+'.h5')
        except:
            pass

FBdata=web.DataReader('FB', 'google', "06/07/2016", "06/19/2017")
tencentdata=web.DataReader('TCEHY', 'google', "06/07/2016",  "06/19/2017")
def GetNextDay(data, date):
    for i in range(10):
        nextday=date+datetime.timedelta(days=1)
        if nextday in data['Open']:
            return nextday
def GenOneSample():

    date=strTimeProp("1/1/2006","06/07/2017",'%m/%d/%Y',random.random())
    checkday = datetime.datetime.strptime(date, '%m/%d/%Y')

    traning=[]
    yesterday=checkday-datetime.timedelta(days=1)
    if (tencentdata['Open'][checkday] > 1.01*tencentdata['Close'][yesterday]):
        if FBdata['Close'][checkday] > FBdata['Open'][checkday]:
            return 1
        else:
            return -1
    if (tencentdata['Open'][checkday] < 0.99*tencentdata['Close'][yesterday]):
        if FBdata['Close'][checkday] < FBdata['Open'][checkday]:
            return 1;
        else:
            return -1
    return 0
    #print(data['Open'][date])
#start = datetime.datetime(2010, 1, 1)
#end = datetime.datetime(2013, 1, 27)
#f = web.DataReader("F", 'google', start, end)
#print(f)
#conn = sqlite3.connect('Data.db')
#conn.execute("CREATE TABLE IF NOT EXISTS Stockdata (tag INTEGER, data Blob);")
#for i in range(10):
#    try:
#        print(GenOneSample())
#        pass
#for i in range(1000):
#    try:
#        GenOneSample(list,conn)
#    except:
#        pass
#conn.close()
upperband, middleband, lowerband = talib.BBANDS(FBdata['Close'].values)
print(upperband)