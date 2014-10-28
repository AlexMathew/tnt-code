
# coding: utf-8

# In[1]:

import plotly.plotly as py
from plotly.graph_objs import *


# In[5]:

import pymongo
connection = pymongo.MongoClient('mongodb://localhost')
db = connection.tnt


# In[7]:

import operator


# In[8]:

import numpy as np


# In[27]:

batAvg = operator.itemgetter('BattingAverage')
battingAverages = [batAvg(player) for player in db.statistics.find()]
batAverages = np.array(battingAverages)
dataBatAvg = Data([
    Histogram(
        x = batAverages
    )
])


# In[28]:

batSR = operator.itemgetter('BattingSR')
battingStrRate = [batSR(player) for player in db.statistics.find()]
batStrRate = np.array(battingStrRate)
dataBatSR = Data([
    Histogram(
        x = batStrRate
    )
])


# In[29]:

batPH = operator.itemgetter('BattingPinchHitting')
battingPinch = [batPH(player) for player in db.statistics.find()]
batPinch = np.array(battingPinch)
dataBatPinch = Data([
    Histogram(
        x = batPinch
    )
])


# In[30]:

bowlO100R = operator.itemgetter('BowlingOvers100Runs')
bowlingO100R = [bowlO100R(player) for player in db.statistics.find()]
bowlOR = np.array(bowlingO100R)
dataBowlO100R = Data([
    Histogram(
        x = bowlOR
    )
])


# In[31]:

bowlW10O = operator.itemgetter('BowlingWicketsPer10')
bowlingW10O = [bowlW10O(player) for player in db.statistics.find()]
bowlWO = np.array(bowlingW10O)
dataBowlW10O = Data([
    Histogram(
        x = bowlWO
    )
])


# In[32]:

bowlO10B = operator.itemgetter('BowlingOvers10Boundaries')
bowlingO10B = [bowlO10B(player) for player in db.statistics.find()]
bowlOB = np.array(bowlingO10B)
dataBowlO10B = Data([
    Histogram(
        x = bowlOB
    )
])


# In[33]:

bowlOExtras = operator.itemgetter('BowlingOversExtras')
bowlingOE = [bowlOExtras(player) for player in db.statistics.find()]
bowlOE = np.array(bowlingOE)
dataBowlOE = Data([
    Histogram(
        x = bowlOE
    )
])


# In[24]:

py.sign_in("AlexMathew", "e82zl7fmcu")


# In[34]:

plot_url_BatAvg = py.plot(dataBatAvg, filename='battingAverage-histogram')
plot_url_BatSR = py.plot(dataBatSR, filename='battingStrikeRate-histogram')
plot_url_BatPinch = py.plot(dataBatPinch, filename='battingPinchHitting-histogram')
plot_url_BowlOR = py.plot(dataBowlO100R, filename='bowlingOvers100Runs-histogram')
plot_url_BowlWO = py.plot(dataBowlW10O, filename='bowlingWicket10Overs-histogram')
plot_url_BowlOB = py.plot(dataBowlO10B, filename='bowlingOver10Boundaries-histogram')
plot_url_BowlOE = py.plot(dataBowlOE, filename='bowlingOversExtras-histogram')


# In[ ]:



