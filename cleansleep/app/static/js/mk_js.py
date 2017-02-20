from flask import render_template,request
from app import app
import pymysql as mdb
from a_Model import ModelIt
import pickle
import json

def input():
    # return render_template("input.html")                                                                                                                        
    hotels = []
    marker_lon = []
    marker_lat = []
#     marker_gps = []                                                                                                                                             
    marker_ID = []
    marker_name=[]
    marker_rating= []
    with db:
        cur = db.cursor()
        cur.execute("SELECT HotelID, HotelName, City, Ratepng, HotelRate, Hotel_lat , Hotel_len FROM ddScore;")
        query_results = cur.fetchall()

    for result in query_results:
        hotels.append(dict(ID=result[0], name=result[1], city=result[2], png=result[3],rate=result[4], lat=result[5], len=result[6]))
#         t= [result[5],result[6]]                                                                                                                                
        marker_lat.append(result[5])
        marker_lon.append(result[6])
      #   marker_gps.append(t)                                                                                                                                    
        marker_ID.append(result[0])
        marker_name.append(result[1])
        marker_rating.append(result[4])
    with open("/Users/hkim/Desktop/Insight_Project/CleanSleep/Flask/app/static/js/data", "w") as outfile:
        json.dump({ID=result[0], name=result[1], city=result[2], png=result[3],rate=result[4], lat=result[5], len=result[6]}, outfile, indent=4)
    return render_template("input.html", hotels=hotels, marker_lon=marker_lon, marker_lat=marker_lat ,marker_ID=marker_ID,marker_name=marker_name,marker_rating=marker_rating)
