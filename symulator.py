# -*- coding: utf-8 -*-
"""
Created on Sat May 27 16:03:22 2017

@author: RAPTOR
"""
import PIL.Image
from PIL import ImageTk
from tkinter import *
import time
import json
import sqlite3


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    
class converterMap:
    x1 = 20.788000
    y1 = 52.160088
    x2 = 21.227348
    y2 = 52.330103
    length = 1280
    width = 810
    
    def isOnMap(self, lon, lat):
        if(self.x1 < lon < self.x2 and self.y1 < lat < self.y2):
            return True
        else:
            return False
    
    def getPosition(self, lon, lat):
        x = (lon - self.x1) / (self.x2 - self.x1) * self.length
        y = self.width - (lat - self.y1) / (self.y2 - self.y1) * self.width
        return (x,y)

root = Tk()
root.geometry('2480x1240')
Canvas.create_circle = _create_circle
canvas = Canvas(root,width=2480,height=1240)
canvas.pack()
temp=PIL.Image.open("mapa_warszawy.jpg")
temp = temp.save("photo.ppm","ppm")
photo = PhotoImage(file = "photo.ppm")
cm = converterMap()
conn = sqlite3.connect("autobusyPiatek")
conn2 = sqlite3.connect("tramwajePiatek")
for row in conn2.execute("SELECT * FROM data"):
    canvas.create_image(640, 405, image=photo)
    data = json.loads(row[1])
    currList = data['result']
    for currItem in currList:
        if(cm.isOnMap(float(currItem['Lon']), float(currItem['Lat']))):
            p = cm.getPosition(float(currItem['Lon']), float(currItem['Lat']))
            canvas.create_circle(p[0], p[1], 2, fill="blue", width=1)
    root.update()
    time.sleep(0.5)
    canvas.delete("all")

root.mainloop()