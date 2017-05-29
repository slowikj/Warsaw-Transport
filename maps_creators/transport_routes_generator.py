# -*- coding: utf-8 -*-
"""
Created on Mon May 29 08:28:29 2017

@author: slowik
"""

from static_image_creator import *
import sys
import sqlite3

if len(sys.argv) != 3:
    print("arguments:")
    print("db path")
    print("background image path")
else:
    db_path, background_image_path = sys.argv[1:]
    lines_routes_dict = create_static_line_images_from_db(sqlite3.connect(db_path),
                                                          background_image_path,
                                                          1280, 810)
     
    print(len(lines_routes_dict))                                                     
    for line_name, image_tuple in lines_routes_dict.items():
        try:
            print(line_name + " START")
            image_tuple[1].save("./line_routes/" + line_name + ".png")
            print(line_name + " DONE")
        except:
            print("an error during saving " + line_name)
