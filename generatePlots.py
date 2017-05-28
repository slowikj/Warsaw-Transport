# -*- coding: utf-8 -*-
"""
Created on Sun May 28 19:30:48 2017

@author: RAPTOR
"""

from script import *

conn = sqlite3.connect("autobusySobota")
conn2 = sqlite3.connect("tramwajeSobota")

date = datetime(2017, 5, 27)
calculateAvg(conn, conn2, date, 62, allPoints, allPoints, "Autobusy", "Tramwaje", "plots/2_1_1a")
calculateAvg(conn, conn2, date, 62, myCentrum, myCentrum, "Autobusy", "Tramwaje", "plots/2_1_1b")
calculateAvg(conn, conn2, date, 62, notMyCentrum, notMyCentrum, "Autobusy", "Tramwaje", "plots/2_1_1c")

calculateAvg(conn, conn2, date, 62, wola, wola, "Autobusy", "Tramwaje", "plots/2_1_2a")
calculateAvg(conn, conn2, date, 62, mokotow, mokotow, "Autobusy", "Tramwaje", "plots/2_1_2b")
calculateAvg(conn, conn2, date, 62, ursynow, ursynow, "Autobusy", "Tramwaje", "plots/2_1_2c")
calculateAvg(conn, conn2, date, 62, bialoleka, bialoleka, "Autobusy", "Tramwaje", "plots/2_1_2d")
calculateAvg4(conn, date, 62, wola, mokotow, ursynow, bialoleka, "wola", "mokotow", "ursynow", "bialoleka", "plots/2_1_2e")
calculateAvg4(conn2, date, 62, wola, mokotow, ursynow, bialoleka, "wola", "mokotow", "ursynow", "bialoleka", "plots/2_1_2f")


calculateNumber(conn, conn2, date, 31, allPoints, allPoints, "Autobusy", "Tramwaje", "plots/2_2_1a")
calculateNumber(conn, conn2, date, 31, myCentrum, myCentrum, "Autobusy", "Tramwaje", "plots/2_2_1b")
calculateNumber(conn, conn2, date, 31, notMyCentrum, notMyCentrum, "Autobusy", "Tramwaje", "plots/2_2_1c")

calculateNumber(conn, conn2, date, 31, wola, wola, "Autobusy", "Tramwaje", "plots/2_2_2a")
calculateNumber(conn, conn2, date, 31, mokotow, mokotow, "Autobusy", "Tramwaje", "plots/2_2_2b")
calculateNumber(conn, conn2, date, 31, ursynow, ursynow, "Autobusy", "Tramwaje", "plots/2_2_2c")
calculateNumber(conn, conn2, date, 31, bialoleka, bialoleka, "Autobusy", "Tramwaje", "plots/2_2_2d")
calculateNumber4(conn, date, 31, wola, mokotow, ursynow, bialoleka, "wola", "mokotow", "ursynow", "bialoleka", "plots/2_2_2e")
calculateNumber4(conn2, date, 31, wola, mokotow, ursynow, bialoleka, "wola", "mokotow", "ursynow", "bialoleka", "plots/2_2_2f")