# -*- coding: utf-8 -*-
"""
Created on Sat May 27 16:03:22 2017

@author: RAPTOR
"""
import PIL.Image
#from PIL import ImageTk
from PIL import ImageDraw, Image
from tkinter import *
import time
import json
import sqlite3
import pandas as pd
import numpy as np
import requests
import json

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

def get_dataframe_from_db(db_name, table_name, json_column_names,
                          start_req_ind, end_req_ind):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table_name)
        all_rows = cur.fetchall();

        df = pd.DataFrame(columns=json_column_names)

        for (cnt, results_string) in all_rows:
            print(cnt)
            if cnt < start_req_ind or cnt % 2 == 0:
                continue

            if cnt > end_req_ind:
                break                
            
            results_json = json.loads(results_string)
            json_array = results_json["result"]

            for json_item in json_array:
                df.loc[len(df)] = json_item

    return df
    
def create_animated_image_from_db(bus_con, tram_con,
                                  background_image_path,
                                  target_file_name,
                                  image_width, image_height):
    (root, canvas, photo) = get_online_drawing_data(background_image_path,
                                            image_width, image_height, target_file_name)
    cm = converterMap(image_width, image_height)

    bus_iter = iter(bus_con.cursor().execute("SELECT * FROM " + "data").fetchall())
    tram_iter = iter(tram_con.cursor().execute("SELECT * FROM " + "data").fetchall())
    
    while True:
        try:
            bus_row = next(bus_iter)
            tram_row = next(tram_iter)
            
            bus_json_array = json.loads(bus_row[1])["result"]
            tram_json_array = json.loads(tram_row[1])["result"]
            
            canvas.create_image(image_width / 2, image_height / 2, image=photo)
            set_points_online(cm, bus_json_array, canvas, root, "blue")
            set_points_online(cm, tram_json_array, canvas, root, "red")

            time.sleep(0.01)
            
            root.update()
            canvas.delete("all")            
        except KeyboardInterrupt:
            break
        except StopIteration:
            print("stopIter")
            break
    
    root.mainloop()        
        

def create_online_image(bus_request_url, tram_request_url,
                        target_file_name,
                        background_image_path,
                        image_width, image_height):
    (root, canvas, photo) = get_online_drawing_data(background_image_path,
                                            image_width, image_height, target_file_name)
    cm = converterMap(image_width, image_height)
    
    while True:
        try:
            bus_json_array = get_json_array(bus_request_url)
            tram_json_array = get_json_array(tram_request_url)
            
            canvas.create_image(image_width / 2, image_height / 2, image=photo)
            set_points_online(cm, bus_json_array, canvas, root, "blue")
            set_points_online(cm, tram_json_array, canvas, root, "red")
            
            time.sleep(10)
            
            root.update()
            canvas.delete("all")            
        except KeyboardInterrupt:
            break
        
    root.mainloop()
    
def create_offline_image_from_data_frame(target_file_name, data_frame,
                                        background_image_path,
                                        image_width, image_height):
    (draw, image) = get_offline_drawing_data(background_image_path)
    cm = converterMap(image_width, image_height)
    set_points_offline(cm, data_frame, draw, image, "blue", target_file_name)
    

def get_json_array(request_url):
    return json.loads(str(requests.get(request_url).text))["result"]

def set_points_online(cm, json_array, canvas, root, fill_color):
    for row in json_array:
        try:
            longitude = float(row["Lon"])
            latitude = float(row["Lat"])
        
            if cm.isOnMap(longitude, latitude):
                p = cm.getPosition(longitude, latitude)
                canvas.create_circle(p[0], p[1], 2, fill=fill_color, width=1)
        except Exception:
            pass
        
    root.update()

def set_points_offline(cm, data_frame, draw, image, point_color, new_file_name):
    point_size = 3
    for row in data_frame.iterrows():
        row_series = row[1]
        lineNumber = (row_series["Lines"].strip())
        longitude = float(row_series["Lon"])
        latitude = float(row_series["Lat"])
        
        if cm.isOnMap(longitude, latitude):
            p = cm.getPosition(longitude, latitude)
            
            draw.ellipse([p[0] - point_size,
                          p[1] - point_size,
                        p[0] + point_size,
                        p[1] + point_size], fill=point_color)
    
    image.save(new_file_name)
        

def get_online_drawing_data(background_image_path, image_width, image_height, target_file_name):
    root = Tk()
    canvas_width = get_canvas_width(image_width)
    canvas_height = get_canvas_height(image_height)
    root.geometry(str(canvas_width) + "x" + str(canvas_height))
    
    Canvas.create_circle = _create_circle
    canvas = Canvas(root,width=canvas_width,height=canvas_height)
    canvas.pack()
    
    temp=PIL.Image.open(background_image_path)
    temp = temp.save(target_file_name + ".ppm","ppm")
    photo = PhotoImage(file = target_file_name + ".ppm")
    
    return (root, canvas, photo)
    
def get_offline_drawing_data(background_image_path):
    image = Image.open(background_image_path)
    draw = ImageDraw.Draw(image)
    
    return (draw, image)
    

def get_canvas_width(image_width):
    return image_width + 10

def get_canvas_height(image_height):
    return image_height + 10

# getting unique lines
def make_images(df):
    unique_lines = df.loc[:, "Lines"].unique()
    
    for line in unique_lines:
        print("try to process line: " + line)
        
        line_df = df.loc[df.Lines == line, :]
        if len(line_df) > 5:
            create_offline_image_from_data_frame(line + ".png", line_df,
                                                 "mapa_warszawy.jpg",
                                                 1280, 810)
            print(line + " done")

###################################################################################
#df = get_dataframe_from_db("autobusySobota", "data",
#                           ["Lat", "Lon", "Time", "Lines", "Brigade"],
#                            1900, 1930)
#make_images(df)
#bus_request_url = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=a94779ec-47e0-4545-baa1-62206517940e&type=1'
#tram_request_url = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=a94779ec-47e0-4545-baa1-62206517940e&type=2'
#create_online_image(bus_request_url, tram_request_url,
#                    "photo",
#                    "mapa_warszawy.jpg",
#                    1280, 810)
                    
create_animated_image_from_db(sqlite3.connect("autobusySobota"), sqlite3.connect("tramwajeSobota"),
                                  "mapa_warszawy.jpg",
                                  "photo",
                                  1280, 810)