# -*- coding: utf-8 -*-
"""
Created on Mon May 29 09:58:48 2017

@author: slowik
"""

import sqlite3
import sys
import static_image_creator as ic

db_name, background_image_path = sys.argv
lines_images_dict = ic.create_static_line_images_from_db(sqlite3.connect(db_name),
                                                      background_image_path,
                                                      1280, 810)