import pandas_datareader.data as web
import datetime
import random
import sqlite3
import time
import numpy as np
import io
import pickle
import talib
import pandas
import math
backtrace=-30
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
            data.to_pickle('./stockhist/'+symbol+'.pkl')
        except:
            pass
def GetNextDay(date, data):
    nextday=date;
    for i in range(10):
        nextday=nextday+datetime.timedelta(days=1)
        if nextday in data['Open']:
            return nextday

def GenOneSample(symbols,conn):
    index = random.randint(0, len(symbols) - 1)
    target = symbols[index]
    date = strTimeProp("1/1/2007", "06/07/2017", '%m/%d/%Y', random.random())
    checkday = datetime.datetime.strptime(date, '%m/%d/%Y')
    olddata = pandas.read_pickle("./stockhist/" + target + ".pkl")
    olddata =(olddata-olddata.min())/(olddata.max()-olddata.min())
    data = olddata[:checkday]
    matrix=[]
    #bollinger band area
    upperband, middleband, lowerband = talib.BBANDS(data['Close'].values)

    matrix.append(upperband[backtrace:-1])
    matrix.append(middleband[backtrace:-1])
    matrix.append(lowerband[backtrace:-1])
    #DEMA
    matrix.append(talib.DEMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #EMA
    matrix.append(talib.EMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #KAMA
    matrix.append(talib.KAMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #SMA
    matrix.append(talib.SMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #MAMA
    mama, fama= talib.MAMA(data['Close'].values)
    matrix.append(mama[backtrace:-1])
    matrix.append(fama[backtrace:-1])
    #TEMA
    matrix.append(talib.TEMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #TRIMA
    matrix.append(talib.TRIMA(data['Close'].values, timeperiod=21)[backtrace:-1])
    #ADX
    matrix.append(talib.ADX(data['High'].values,data['Low'].values, data['Close'].values, timeperiod=21)[backtrace:-1])
    #ADXR
    matrix.append(talib.ADXR(data['High'].values,data['Low'].values, data['Close'].values, timeperiod=21)[backtrace:-1])
    #APO
    matrix.append(talib.APO(data['Close'].values)[backtrace:-1])
    #BOP
    matrix.append(talib.BOP(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #CCI
    matrix.append(talib.CCI(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #CMO
    matrix.append(talib.CMO(data['Close'].values)[backtrace:-1])
    #DX
    matrix.append(talib.DX(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #MACD
    macd, macdsignal, macdhist = talib.MACD(data['Close'].values)
    matrix.append(macd[backtrace:-1])
    matrix.append(macdsignal[backtrace:-1])
    matrix.append(macdhist[backtrace:-1])
    #MFI
    matrix.append(talib.MFI(data['High'].values,data['Low'].values,data['Close'].values,data['Volume'].values.astype(float))[backtrace:-1])
    #MINUS_DI
    matrix.append(talib.MINUS_DI(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #MINUS_DM
    matrix.append(talib.MINUS_DM(data['High'].values,data['Low'].values)[backtrace:-1])
    #MOM
    matrix.append(talib.MOM(data['Close'].values)[backtrace:-1])
    #PLUS_DI
    matrix.append(talib.PLUS_DI(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #PLUS_DM
    matrix.append(talib.PLUS_DM(data['High'].values,data['Low'].values)[backtrace:-1])
    #PPO
    matrix.append(talib.PPO(data['Close'].values)[backtrace:-1])
    #ROCP
    matrix.append(talib.ROCP(data['Close'].values)[backtrace:-1])
    #ROC
    matrix.append(talib.ROC(data['Close'].values)[backtrace:-1])
    #ROCR
    matrix.append(talib.ROCR(data['Close'].values)[backtrace:-1])
    #RSI
    matrix.append(talib.RSI(data['Close'].values)[backtrace:-1])
    #STOCH
    slowk, slowd = talib.STOCH(data['High'].values,data['Low'].values, data['Close'].values)

    matrix.append(slowk[backtrace:-1])
    matrix.append(slowd[backtrace:-1])
    #STOCHF
    fastk, fastd = talib.STOCHF(data['High'].values,data['Low'].values, data['Close'].values)
    matrix.append(fastk[backtrace:-1])
    matrix.append(fastd[backtrace:-1])
    #WILLR
    matrix.append(talib.WILLR(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #AD
    matrix.append(talib.AD(data['High'].values,data['Low'].values,data['Close'].values,data['Volume'].values.astype(float))[backtrace:-1])
    #ADOSC
    matrix.append(talib.ADOSC(data['High'].values,data['Low'].values,data['Close'].values,data['Volume'].values.astype(float))[backtrace:-1])
    #OBV
    matrix.append(talib.OBV(data['Close'].values,data['Volume'].values.astype(float))[backtrace:-1])
    #ATR
    matrix.append(talib.ATR(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #TRANGE
    matrix.append(talib.TRANGE(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])
    #NATR
    matrix.append(talib.NATR(data['High'].values,data['Low'].values,data['Close'].values)[backtrace:-1])

    matrix=np.array(matrix)
    if checkday not in olddata['Open']:
        checkday=GetNextDay(checkday,olddata)
    baseline=olddata['Open'][checkday]
    tag=0
    day=checkday
    flag=True;
    for i in range(5):
        if olddata['High'][day]> 1.02*baseline:
            tag=3
            flag=False
            break
        if olddata['Low'][day]< 0.98*baseline:
            tag=0
            flag=False
            break
        day = GetNextDay(day, olddata)
    if flag:
        if olddata['Close'][day] > baseline:
            tag=2
        if olddata['Close'][day] < baseline:
            tag=1
    if not math.isnan(np.sum(matrix)):
        print (np.sum(matrix))
        blob=pickle.dumps(matrix)
        conn.execute("INSERT INTO StockTable (tag, data) values (?,?)", (tag, blob))
        conn.commit()

#upperband, middleband, lowerband = talib.BBANDS(FBdata['Close'].values)
#print(upperband)
conn=sqlite3.connect("./Collected.db")
conn.execute("CREATE TABLE IF NOT EXISTS StockTable (tag integer, data blob)")
list=loadSymboles()
GenOneSample(list, conn)

#Download(list)
for i in range(100):
    try:
        GenOneSample(list,conn)
    except:
        pass
conn.close()