import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Searching example for the route below: /api/v1.0/20100823 <= This is an Example!!!<br/>"
        f"/api/v1.0/<start><br/>"
        f"Searching example for the route below: /api/v1.0/20100823/20110504 <= This is an Example!!!<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_data = []
    for prcp in results:
        data_dict = {}
        data_dict["Date"] = prcp
        all_data.append(data_dict)

    return jsonify(all_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude,
                            Station.longitude,Station.elevation).all()
    session.close()

    # Create a dictionary from the row data and append to a list of  all_station
    all_station = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        all_station.append(station_dict)

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
            .filter(Measurement.date <= dt.date(2017, 8, 23),Measurement.date >= dt.date(2016, 8, 23))\
            .filter(Measurement.station == 'USC00519281')\
            .all()

    session.close()

     # Create a dictionary from the row data and append to a list of  all_station
    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["Station"] = station
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def search(start=None, end = None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all variables
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    return jsonify(results)
    
@app.route("/api/v1.0/<start>/<end>")
def search_2(start=None, end = None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all variables
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    results_2 = session.query(*sel).filter(Measurement.date >= start, Measurement.date <= end).all()
    
    session.close()
    
    return jsonify(results_2)

if __name__ == "__main__":
    app.run(debug=True)