# Import datetime, NumPy and Pandas dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependencies 
from flask import Flask, jsonify
# Set up the database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes 
Base = automap_base()

# Reflect the schema 
Base.prepare(engine, reflect=True)

# Create variables for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the SQLite database
session = Session(engine)

# Define a Flask app 
app = Flask(__name__)

# Define the root of the routes (which will be "welcome")
@app.route("/")

# Create a function "welcome()" with a return statement 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Define the precipitation route 
@app.route("/api/v1.0/precipitation")

# Define a precipitation function that will return precipitation data
# for all dates within the previous year as a JSON file 
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
# Define the stations route 
@app.route("/api/v1.0/stations")

# Define a stations function that will return all of the stations 
# first as an array but finally as a JSON file 
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define the temperatures route 
@app.route("/api/v1.0/tobs")

# Define a temperatures function that will query the primary station 
# for all of the temps within the past year, adn return it first as a 
# list but finally as a JSON file 
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Define the statistics route with a starting and end date 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Define a statistics function that will find stats for the start and end
# date, and return it first as a list but finally as a JSON file 
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)