import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# View all of the classes that automap found
Base.classes.keys()

# Assign the measurement class to a variable called `Measurement`
Measurement = Base.classes.measurement

# Assign the station class to a variable called `Station`
Station = Base.classes.station

# Create a session
session = Session(engine)

#1. Dictionary of preciptation
preciptation = [
   { "2016-08-24": "0.08"},
   { "2016-08-24": "2.15"},
   { "2016-08-24": "2.28"},
   { "2016-08-24": "1.22"},
   { "2017-08-22": "0.50"},
   { "2017-08-23": "0.08"},
   { "2017-08-23": "0.45"}
]


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():

    """List all available api routes."""
    return (
        f"Welcome to the Home Page below is a list of Available Routes:<br/>"
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end"
    )



# 4. Define what to do when a user hits the /api/v1.0/preciptation
@app.route("/api/v1.0/preciptation")
def preciptation():

     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query preciptation
    results_prcp = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    prcp_dates = []
    for date, prcp in results_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_dates.append(prcp_dict)
    """Return data as json"""

    return jsonify(prcp_dates)

# 5. Define what to do when a user hits the /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
       # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query station
    results_station = session.query(Measurement.station).all()
    session.close()

      # Convert list of tuples into normal list
    all_stations = list(np.ravel(results_station))


    return jsonify(all_stations)

# 6. Define what to do when a user hits the /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
   results_tobs = session.query(Measurement.date, Measurement.tobs).all()
   session.close()
      # Convert list of tuples into normal list
   all_tobs = list(np.ravel(results_tobs))

   
   return jsonify(all_tobs)

# 7. Define what to do when a user hits the /api/v1.0/<start>
@app.route("/api/v1.0/start")
def start():
   results_start = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >'2010-01-01').\
   order_by(Measurement.date).all()
   session.close()
      # Convert list of tuples into normal list
   all_start = list(np.ravel(results_start))

   return jsonify(all_start)

# 8. Define what to do when a user hits the /api/v1.0/<start>
@app.route("/api/v1.0/end")
def end():
   results_end = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date <'2017-08-23').\
order_by(Measurement.date).all()
   session.close()
      # Convert list of tuples into normal list
   all_end = list(np.ravel(results_end))

   return jsonify(all_end)


if __name__ == "__main__":
    app.run(debug=True)
