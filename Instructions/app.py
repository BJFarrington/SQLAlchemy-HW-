import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resource/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Welcome():
    return (
       f"Welcome to the Climate API!<br/><br/>"
       f"Available Routes:<br/><br/>"
       f"/api/precipitation<br/><br/>"
       f"/api/stations<br/><br/>"
       f"/api/temperature<br/><br/>"
       f"/api/start<br/><br/>"
       f"/api/start/end"
   )


#@app.route("/api/v1.0/names")
#def names():
#    """Return a list of all passenger names"""
#    # Query all passengers
#    results = session.query(Passenger.name).all()

    # Convert list of tuples into normal list
#    all_names = list(np.ravel(results))

 #   return jsonify(all_names)


@app.route("/api/precipitation")
def precipitation():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_data  = []
    for date, prcp in results:
        all_data_dict = {}
        all_data_dict["date"] = date
        all_data_dict["prcp"] = prcp
        
        all_data.append(all_data_dict)

  
    return jsonify(all_data)



@app.route("/api/stations")
def stations():

  results = session.query(Measurement.station, Station.name).filter(Measurement.station == Station.station).group_by(Station.name).all()
# a = session.query(Measurement.station ).\
#group_by(Measurement.station).\
#order_by((Measurement.station).asc()).all()

  all_stations = list(np.ravel(results))
  return jsonify(all_stations)




@app.route("/api/temperature")
def temperature():

  #query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
  tempobs_last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-24', '2017-08-23')).order_by((Measurement.date).desc()).all()
  
  return jsonify(tempobs_last_year)



@app.route("/api/<start>")
def start(start):
    
    #start = '2016-08-24'
    end = '2017-08-23'
    temp_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).order_by((Measurement.date).desc()).all()
     
    
    return jsonify(temp_start)   

@app.route("/api/<start>/<end>")
def start_end(start, end):
 
    temp_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).order_by((Measurement.date).desc()).all()
    
    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)