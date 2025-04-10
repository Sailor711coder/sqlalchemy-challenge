# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text
import pandas as pd

class SQLHelper():

    def __init__(self):
        self.engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        self.Base = None
        self.Measurement = None
        self.Station = None
        self.session = None

        # prepare db
        self.init_database()

    # connects the ORM stuff
    def init_database(self):
        # reflect an existing database into a new model
        self.Base = automap_base()

        # reflect the tables
        self.Base.prepare(autoload_with=self.engine)

        # Save references to each table
        self.Measurement = self.Base.classes.measurement
        self.Station = self.Base.classes.station

        # Create our session (link) from Python to the DB
        self.session = Session(self.engine)

    def get_precipitation_data(self):

        # USE RAW SQL
        # query = """SELECT
        #             date,
        #             station,
        #             prcp
        #         FROM
        #             measurement
        #         WHERE
        #             date >= '2016-08-23';
        #         """
        # df = pd.read_sql(text(query), con=self.engine)

        # OR use ORM
        db_data = self.session.query(self.Measurement.date, self.Measurement.station, self.Measurement.prcp).where(self.Measurement.date >= '2016-08-23').all()
        df = pd.DataFrame(db_data, columns=["date", "station", "prcp"])

        return(df)

    def get_station_data(self):
         # USE RAW SQL
        query = """SELECT
                    *
                FROM
                    station;
                """
        df = pd.read_sql(text(query), con=self.engine)
        return(df)

    def get_tobs_data(self):
        # USE RAW SQL
        query = """SELECT
                    date,
                    station,
                    tobs
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23'
                    AND station = 'USC00519281'
                ORDER BY
                    date asc;
                """

        df = pd.read_sql(text(query), con=self.engine)
        return(df)

    def get_tobs_by_start_date(self, start):
        # USE RAW SQL
        query = f"""SELECT
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                WHERE
                    date >= '{start}';
                """
        df = pd.read_sql(text(query), con=self.engine)
        return(df)

    def get_tobs_by_date_range(self, start, end):
        # USE RAW SQL
        query = f"""SELECT
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                    AND date <= '{end}';
                """
        print(query)

        df = pd.read_sql(text(query), con=self.engine)
        return(df)
