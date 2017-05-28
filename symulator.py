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
import pandas as pd

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    
class converterMap:
    x1 = 20.788000
    y1 = 52.160088
    x2 = 21.227348
    y2 = 52.330103
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def isOnMap(self, lon, lat):
        if(self.x1 < lon < self.x2 and self.y1 < lat < self.y2):
            return True
        else:
            return False
    
    def getPosition(self, lon, lat):
        x = (lon - self.x1) / (self.x2 - self.x1) * self.width
        y = self.height - (lat - self.y1) / (self.y2 - self.y1) * self.height
        return (x,y)

def get_dataframe_from_db(db_name, table_name, json_column_names):
	with sqlite3.connect(db_name) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM " + table_name)
		all_rows = cur.fetchall()

		df = pd.DataFrame(columns=json_column_names)

		for (cnt, results_string) in all_rows:
			results_json = json.loads(results_string)
			json_array = results_json["result"]

			for json_item in json_array:
				df.loc[len(df)] = json_item

	return df

def create_image_from_data_frame(data_frame,
                                 background_image_path, image_width, image_height):
    (root, canvas, photo) = get_drawing_data(background_image_path, image_width, image_height)
    
    cm = converterMap(image_width, image_height)   
    
    for row in data_frame.iterrows():
        row_series = row[1]
        lineNumber = (row_series["Lines"].strip())
        longitude = float(row_series["Lon"])
        latitude = float(row_series["Lat"])
        
        if cm.isOnMap(longitude, latitude):
            p = cm.getPosition(longitude, latitude)
            canvas.create_circle(p[0], p[1], 2, fill="blue", width=1)
        

    root.update()
    root.mainloop()
            

def get_drawing_data(background_image_path, image_width, image_height):
    root = Tk()
    canvas_width = get_canvas_width(image_width)
    canvas_height = get_canvas_height(image_height)
    root.geometry(str(canvas_width) + "x" + str(canvas_height))
    
    Canvas.create_circle = _create_circle
    canvas = Canvas(root,width=canvas_width,height=canvas_height)
    canvas.pack()
    
    temp=PIL.Image.open(background_image_path)
    temp = temp.save("photo.ppm","ppm")
    photo = PhotoImage(file = "photo.ppm")
    
    canvas.create_image(image_width / 2, image_height / 2, image=photo)
    
    return (root, canvas, photo)
    

def get_canvas_width(image_width):
    return image_width + 10

def get_canvas_height(image_height):
    return image_height + 10

df = get_dataframe_from_db("autobusyPiatek", "data", ["Lat", "Lon", "Time", "Lines", "Brigade"])

df_523 = df.loc[df.Lines == "523",:]

create_image_from_data_frame(df_523,
                             "mapa_warszawy.jpg",
                             1280, 810)





