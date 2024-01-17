# Import the dependencies.
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

# ------------------------------------

latest_date = datetime.strptime(session.query(func.max(Base.classes.measurement.date)).scalar(), '%Y-%m-%d')
one_year_ago = latest_date - dt.timedelta(days=365)

precipitation_data = session.query(Base.classes.measurement.date, Base.classes.measurement.prcp).\
    filter(Base.classes.measurement.date >= one_year_ago).all()

prcp_df = pd.DataFrame(precipitation_data, columns=['date', 'prcp'])

prcp_df.set_index('date', inplace=True)

total_dates = len(prcp_df.index)
desired_intervals = 6 

total_months = (latest_date.year - one_year_ago.year) * (12) + (latest_date.month - one_year_ago.month)
step_size = max(total_dates // (desired_intervals - 1), 1)

plt.figure(figsize=(10, 6))
plt.bar(prcp_df.index, prcp_df['prcp'], label='Precipitation', width=3)
plt.xlabel('Date')
plt.ylabel('Precipitation (inches)')
plt.title('Last 12 Months of Precipitation Data')

selected_dates_index = np.arange(0, total_dates, step_size)
selected_dates = prcp_df.index[selected_dates_index]

plt.xticks(selected_dates, rotation=90)

plt.legend()
plt.tight_layout()
plt.savefig("static\Precipitation_data.png")

#----------------------------------------------

most_active_station = session.query(measurement.station, func.count(measurement.station).label('station_count')).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).first()

most_active_station_id = most_active_station.station

latest_date = session.query(func.max(measurement.date)).filter(measurement.station == most_active_station_id).scalar()
latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
one_year_ago = latest_date - timedelta(days=365)

temperature_data = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == most_active_station_id).\
    filter(measurement.date >= one_year_ago).all()

df = pd.DataFrame(temperature_data, columns=['date', 'temperature'])

plt.figure(figsize=(10, 6))
plt.hist(df['temperature'], bins=12, label='Temperature Observations', alpha=0.7)
plt.xlabel('Temperature (°F)')
plt.ylabel('Frequency')
plt.title('Last 12 Months of Temperature Observations')
plt.legend()
plt.tight_layout()
plt.savefig("static\Temp_data.png")



#################################################
# Flask Setup
#################################################

from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(autoload_with=engine)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

@app.route('/api/v1.0/precipitation')
def prcp():
    precipitation_data_dict = prcp_df['prcp'].to_dict()

    return jsonify(precipitation_data_dict)

@app.route('/api/v1.0/stations')
def stations():
    station_results = session.query(station.station, station.name).all()

    stations_data = [{'station': result.station, 'name': result.name} for result in station_results]

    return jsonify(stations_data)

@app.route('/api/v1.0/tobs')
def tobs():
    most_active_station = session.query(measurement.station, func.count(measurement.station).label('station_count')).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()

    most_active_station_id = most_active_station.station
    latest_date = session.query(func.max(measurement.date)).filter(measurement.station == most_active_station_id).scalar()
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    one_year_ago = latest_date - timedelta(days=365)

    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station_id).\
        filter(measurement.date >= one_year_ago).all()
    
    tobs_list = [{'date': result.date, 'tobs': result.tobs} for result in tobs_data]

    return jsonify(tobs_list)


@app.route('/api/v1.0/<start>')
def temp_start(start):
    temp_data_start = session.query(func.min(measurement.tobs).label('TMIN'),
                                     func.avg(measurement.tobs).label('TAVG'),
                                     func.max(measurement.tobs).label('TMAX')).\
        filter(measurement.date >= start).all()

    if temp_data_start:
        temp_start_dict = {'TMIN': temp_data_start[0].TMIN,
                           'TAVG': temp_data_start[0].TAVG,
                           'TMAX': temp_data_start[0].TMAX}

        return jsonify(temp_start_dict)

@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    temp_data_range = session.query(func.min(measurement.tobs).label('TMIN'),
                                    func.avg(measurement.tobs).label('TAVG'),
                                    func.max(measurement.tobs).label('TMAX')).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    temp_range_dict = {'TMIN': temp_data_range[0].TMIN,
                       'TAVG': temp_data_range[0].TAVG,
                       'TMAX': temp_data_range[0].TMAX}

    return jsonify(temp_range_dict)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


#################################################
# Flask Routes
#################################################
