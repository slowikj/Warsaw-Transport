# -*- coding: utf-8 -*-
"""
Created on Mon May 29 08:28:29 2017

@author: slowik
"""

from static_image_creator import *

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
