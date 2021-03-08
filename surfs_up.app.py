import numpy as np
import pandas as pd 
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemyimport create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resource/hawaii.sqlite")

#Reflect Existing Database into a New Model
Base = automap_base()
#Reflect the Tables
Base.prepare(engine, reflect=True)

#Save References to each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create Session (link) from Python to the DB
session = Session(engine)

#Flask Setup
app = Flask(_name_)

#Flask Routes
@app.route("/")
def welcome():
    ""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs"
    )
   
#Percipitation Route
@app.route("api/v1.0/percipitation")
def percipitation():
    #Convert the Query Results to a Dictionary Using "date" as the Key and "prcp" as the Value
    #Calcualte the Date 1 Year Ago from the Last Data Point in the Database
    one_year_ago = dt.date(2017, 7, 10) - dt.timedelta(days=365)
    #Create a Query to Retireive the Last 12 Months of Preciptiation Data Selection Onlthe the "date" and "prcp" as the Value
    prcp_data = session.query(Measurement.date, Measurement.prcp).
        filter(Measurement.date >= one_year_ago).
        order_by(Measurement.date).all()
    #Convert List of Tules into a Dictionary
    prcp_data_list = dict(prcp_data)
    #Return JSON Representation of Dictionary
    return  jsonify(prcp_data_list)

#Station Route
@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON List of Stations from the Dataset
    stations_all = session.query(Station.station, Station.name).all()
    #Convert List of Tuples into Normal List
    station_list = list(stations_all)
    #Return JSON list of stations from the Dataset
    return jsonify(station_list)
    
#TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    #Query for the Dates and Temperature Observations from a Year from the Last Data Point
    one_year_ago = dt.date(2017, 7, 10) - dt.timedelta(days=365)
    #Create a Query to Retrieve the Last 12 months of Precipitation DAta Selecting only the 'date" and 'precp' Values
    tobs_data = session.query(Measurement.date, Measurement.tobs).
        filter(Measurement.date >= one_year_ago).
        order_by(Measurement.date).all()
    #Convert List of Tuples into Normal list
    tobs_data_list = list(tobs_data)
    #Return JSON List of Temperature Observations (tobs) for the Previous Year
    return jsonify(tobs_day_list)
    
#Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).
            group_by(Measurement.date).all()
        #Convert List of Tuples into Normal List
        start_day_list = list(start_day)
        #Return JSON List of Min, Avg, and Max Temps for a Given Start Range
        return jsonify(start_day_list)

#Start-End Day Route    
@app.route("/api/v1.0/<start>/<end>")
def start_end_day = (start, end):
    start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).
            filter(Measurement.date <= end).
            group_by(Measurement.date).all()
    #Convert List of Tuples Into Normal List
    start_end_day_list = list(start_end_day)
    return jsonify(start_end_day_list)

if _name_ == '_main_':
    app.run(debug=True)