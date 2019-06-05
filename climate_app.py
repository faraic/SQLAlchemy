import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes</br>"
        "/api.v1.0/precipitation</br>"
        "/api/v1.0/stations</br>"
        "/api/v1.0/tobs</br>"
        "/api/v1.0/<start></br>"
        "/api/v1.0/<start>/<end></br>"
        
    )

@app.route("/api.v1.0/precipitation")
def precipitation():
    
    query = session.query(Measurement.date, func.max(Measurement.prcp)).\
        group_by(Measurement.date).order_by(Measurement.date.desc()).limit(365).all()

 # Create a dictionary from the row data and append
    precipitation = []
    for date, prcp in query:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    query2=session.query(Station.id, Station.station,Station.name,Station.latitude,\
        Station.longitude,Station.elevation).all()
        
    stations = []
    for id, station, name,latitude,longitude,elevation in query2:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        stations.append(stations_dict)   

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    query3 = session.query(Measurement.date,Measurement.tobs).order_by(Measurement.date.desc()).\
        filter(Measurement.station == 'USC00519281').limit(365).all()
       
# Create a dictionary from the row data and append
    days = []
    for temps in query3:
        temps_dict = {}
        temps_dict["date"] = temps.date
        temps_dict["tobs"] = temps.tobs
        days.append(temps_dict)
        
    return jsonify(days)


@app.route('/api/v1.0/<start>', defaults={'date': None})
@app.route('/<start>/<date>')
def show(start,date):
    Temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                         func.avg(Measurement.tobs)).filter(Measurement.date >=start).all()
                         
    Temps_all=list(np.ravel(Temps))
    Temp_keys=['Minimum temp', 'Maximum temp','Average temp']
    Temps_all_dict=dict(zip(Temp_keys,Temps_all))

    
    return jsonify(Temps_all_dict)

    
@app.route("/api/v1.0/<start>/<end>")
def temps(start, end):

    Temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                         func.avg(Measurement.tobs)).filter(Measurement.date >=start)\
                             .filter(Measurement.date >=start).all()
                         
    Temps_all=list(np.ravel(Temps))
    Temp_keys=['Minimum temp', 'Maximum temp','Average temp']
    Temps_all_dict=dict(zip(Temp_keys,Temps_all))

    
    return jsonify(Temps_all_dict)

if __name__ == '__main__':
    app.run(debug=True)