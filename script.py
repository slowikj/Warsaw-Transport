# -*- coding: utf-8 -*-
"""
Created on Thu May 25 22:46:57 2017

@author: sebassud
"""

import requests
import json
import sqlite3
import time
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mplPath
import numpy as np
import pandas as pd

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def quickDistance(lon1, lat1, lon2, lat2):
    R = 6371  # radius of the earth in km
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    x = (lon2 - lon1) * cos( 0.5*(lat2+lat1) )
    y = lat2 - lat1
    d = R * sqrt( x*x + y*y )
    return d

def differenceStringDate(date1, date2):
    """
    return hours
    """
    diffDate = datetime.strptime(date1 , '%Y-%m-%d %H:%M:%S') - datetime.strptime(date2 , '%Y-%m-%d %H:%M:%S')
    
    if(diffDate.seconds == 0):
        return 0
    else:
        return diffDate.seconds / 3600

def minAvgMax(prevList, currList, fun):
    vlist = []
    for currItem in currList:
        if(fun(currItem['Lat'], currItem['Lon']) == False):
            continue
        prevItem = None
        for prev in prevList:
            if(prev['Lines'] == currItem['Lines'] and prev['Brigade'] == currItem['Brigade']):
                prevItem = prev
                break
        if(prevItem is not None):
            diffTime = differenceStringDate(currItem['Time'], prevItem['Time'])
            if(diffTime != 0):
                dist = haversine(currItem['Lon'], currItem['Lat'], prevItem['Lon'], prevItem['Lat'])
                vlist.append(dist / diffTime)
    return (min(vlist), sum(vlist) / len(vlist), max(vlist))

def calculateNumberVehicles(conn, fun):
    scores = []
    for row in conn.execute("SELECT * FROM data"):
        data = json.loads(row[1])
        currList = data['result']
        scores.append(sum(1 for item in currList if(fun(item['Lat'], item['Lon']))))
            
    return scores

def calculateScoresMinAvgMax(conn, fun):
    first = True
    scores = []
    for row in conn.execute("SELECT * FROM data"):
        data = json.loads(row[1])
        if(first):
            first = False
            prevList = data['result']
        else:
            currList = data['result']
            scores.append(minAvgMax(prevList, currList, fun))
            
    return scores

class LineAvgMax:
    def __init__(self, v, line):
        self.count = 1
        self.sum = v
        self.maxV = v
        self.line = line
        
    def addV(self, v):
        self.count += 1
        self.sum += v
        if(v > self.maxV):
            self.maxV = v
        
    def calAvg(self):
        return self.sum / self.count
    
def lineAvgMax(prevList, currList, fun, dictionary):
    for currItem in currList:
        if(fun(currItem['Lat'], currItem['Lon']) == False):
            continue
        prevItem = None
        for prev in prevList:
            if(prev['Lines'] == currItem['Lines'] and prev['Brigade'] == currItem['Brigade']):
                prevItem = prev
                break
        if(prevItem is not None):
            diffTime = differenceStringDate(currItem['Time'], prevItem['Time'])
            if(diffTime != 0):
                dist = haversine(currItem['Lon'], currItem['Lat'], prevItem['Lon'], prevItem['Lat'])
                if(currItem['Lines'] in dictionary):
                    dictionary[currItem['Lines']].addV(dist / diffTime)
                else:
                    dictionary[currItem['Lines']] = LineAvgMax(dist / diffTime, currItem['Lines'])
    
def calculateLineAvgMax(conn, fun):
    first = True
    dictionary = dict()
    for row in conn.execute("SELECT * FROM data"):
        data = json.loads(row[1])
        if(first):
            first = False
            prevList = data['result']
        else:
            currList = data['result']
            lineAvgMax(prevList, currList, fun, dictionary)
            
    return dictionary
            
def calculateLines(conn, conn2, fun, fun2):
    d1 = calculateLineAvgMax(conn, fun)
    lines = []
    [lines.append(el.line) for el in d1.values()]
    ds1 = {'Avg' :  pd.Series([el.calAvg() for el in d1.values()], lines), 
    'Max' :  pd.Series([el.maxV for el in d1.values()], lines)}
    df1 = pd.DataFrame(ds1)
    
    print(df1.sort(['Avg'], ascending=[0]))
    
    return 0

def calculateAvg(conn, conn2, startDate, interval, fun, fun2):
    scores = calculateScoresMinAvgMax(conn, fun)
    
    listAvg1 = []
    [listAvg1.append(i[1]) for i in scores]
    listTime = []
    [listTime.append(startDate + timedelta(0,interval*i)) for i in range(len(listAvg1))]
    
    
    scores = calculateScoresMinAvgMax(conn2, fun2)
    
    listAvg2 = []
    [listAvg2.append(i[1]) for i in scores]
    
    plt.plot(listTime, listAvg1, 'r', listTime, listAvg2, 'b')
    red_patch = mpatches.Patch(color='red', label='Autobusy')
    blue_patch = mpatches.Patch(color='blue', label='Tramwaje')
    plt.legend(handles=[red_patch, blue_patch])
    plt.ylabel('Max v')
    plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(18.5, 10.5)
    #fig.savefig('test2png.png', dpi=120)
    return 0

def calculateNumber(conn, conn2, startDate, interval, fun, fun2):
    scores1 = calculateNumberVehicles(conn, fun)
    
    listTime = []
    [listTime.append(startDate + timedelta(0,interval*i)) for i in range(len(scores1))]
        
    scores2 = calculateNumberVehicles(conn2, fun2)
    
    plt.plot(listTime, scores1, 'r', listTime, scores2, 'b')
    red_patch = mpatches.Patch(color='red', label='Autobusy')
    blue_patch = mpatches.Patch(color='blue', label='Tramwaje')
    plt.legend(handles=[red_patch, blue_patch])
    plt.ylabel('Ilość')
    plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(18.5, 10.5)
    #fig.savefig('test2png.png', dpi=120)
    return 0

def allPoints(lat, lon):
    return True

def myCentrum(lat, lon):
    bbPath = mplPath.Path(np.array([[52.246760, 20.957805],
                     [52.216239, 20.980857],
                     [52.221867, 21.035873],
                     [52.247934, 21.018419],
                     [52.256370, 20.981776]]))
    return bbPath.contains_point((lat, lon))

conn = sqlite3.connect("autobusyPiatek")
conn2 = sqlite3.connect("tramwajePiatek")

#calculateLines(conn, conn2, myCentrum, allPoints)


        