import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

  
    # Query all results
    results = session.query(Measurement).\
    filter(Measurement.date >= '2016-08-24', Measurement.date <= '2017-08-23')

    session.close()
   
    # Create a dictionary from the row data and append to a list of all_passengers
    
    all_prcp = []
    for rain in results:
        prcp_dict = {}
        prcp_dict[rain.date] = rain.prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def station():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def temp():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query dates and temp results for past year
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-24', Measurement.date <= '2017-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/start")
def start():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query dates and temp results for past year in JSON
    return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-24').all())

@app.route("/api/v1.0/start/end")
def end():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query dates and temp results for past year in JSON
    return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-24', Measurement.date <= '2017-08-23').all())

if __name__ == '__main__':
    app.run(debug=True)
