# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create a connection to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///C:/Users/fitse/OneDrive/Desktop/Challenges/sqlalchemy-challenge/Resources/hawaii.sqlite")
#engine = create_engine(r"sqlite:///C:\Users\fitse\OneDrive\Desktop\Challenges\sqlalchemy-challenge\Resources\hawaii.sqlite")
#engine = create_engine("sqlite:///C:/Users/fitse/OneDrive/Desktop/Challenges/sqlalchemy-challenge/Resources/hawaii.sqlite")
#DATABASE_PATH = "../Resources/hawaii.sqlite"
#engine = create_engine(f"sqlite:///{DATABASE_PATH}")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables from the database
Base.prepare(autoload_with=engine)

# Map the Measurement and Station tables to classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Initialize the Flask application
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Welcome():
    """List all available API routes."""
    return(
        f"Welcome to the  Hawii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0//temp/start/end<br/>"
       f"<p>'start' and 'end' date should be in the format MMDDYYYY.<p>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data from last year"""
    # Calculate the date one year before the last data point in the dataset
    a_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= a_year_before).all()

    # Close the session
    session.close()

    # Create a dictionary with date as the key and precipitation as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return the list of stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Close the session
    session.close()
    
    # Convert the query results into a list
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observation for previous year"""
    # Calculate the date one year before the last data point in the dataset
    a_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query temperature observations for the most active station over the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= a_year_before).all()

    # Close the session
    session.close()

    # Unravel results into an ID array and convert into a list
    temps = list(np.ravel(results))
    
    # Convert list of tuples into normal list
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None): 
    "Return temp min, temp max and temp avg"
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)] 

    # If no end date is provided
    if not end:
        # Convert the start date string to a datetime object
        start = dt.datetime.strptime(start, "%m%d%Y")
        # Query for the temperature statistics from the start date onwards
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        # Close the session
        session.close()

        # Unravel results into an ID array and convert into a list
        temps = list(np.ravel(results)) 
        return jsonify(temps)

    # If end date is provided # Convert the start and end date strings to datetime objects
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    # Query for the temperature statistics between the start and end dates
    results = session.query(*sel).\
            filter(Measurement.date >= start).all().\
                 filter(Measurement.date <= end).all()
    
    # Close the session
    session.close()

     # Unravel results into an ID array and convert into a list
    temps = list(np.ravel(results)) 
    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)
