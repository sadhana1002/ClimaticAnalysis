from flask import Flask,jsonify,send_file
import climatic_analysis as helper
from datetime import datetime
import json

app = Flask(__name__)

def currentday():
    today = datetime.now()
    return today.strftime('%m-%d')

@app.route("/")
def home():
    return (
        f"<bold>Welcome to the Hawaiian Climate API!<br/><br/></bold>"
        f"<bold>Available Routes:<br/><br/></bold>"
        f"<bold>General data:<br/><br/></bold>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"<bold>Specific trip data:<br/><br/></bold>"
        f"/api/v1.0/trip/\"startdate as mm-dd\"<br/>"
        f"/api/v1.0/trip/\"startdate as mm-dd\"/\"enddate as mm-dd\"<br/><br/>"
        f"<bold>Visualizations:<br/><br/></bold>"
        f"/api/v1.0/viz/tobs<br/>"
        f"/api/v1.0/viz/precipitation<br/>"
        f"/api/v1.0/viz/trip_average<br/>"
        f"/api/v1.0/viz/daily_normals<br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def getprecipitationinfo():
    precipitation_df = helper.precipitation_data()
    precipitation_list = precipitation_df.to_dict(orient='index')
    result = jsonify(precipitation_list)
    return result

@app.route("/api/v1.0/stations")
def getstationsinfo():
    stations_df = helper.getallstations()
    station_list = stations_df.to_dict()
    result = jsonify(station_list)
    return result

@app.route("/api/v1.0/tobs")
def gettemperaturesinfo():
    temperatures_df = helper.get_temperature_obs()
    temperatures_list = temperatures_df.to_json()
    # result = jsonify(temperatures_list)
    return temperatures_list

@app.route("/api/v1.0/trip/<start>")
@app.route("/api/v1.0/trip/<start>/<end>")
def gettripprediction(start,end=currentday()):
    dailynormals_df = helper.dailynormals(start,end)
    dailynormals_list = dailynormals_df.to_dict(orient='index')
    result = jsonify(dailynormals_list)
    return result

@app.route("/api/v1.0/viz/<feature>")
def visual_temperature(feature):
    if(feature == 'tobs'):
        return send_file('figures/TemperatureAnalysis_Hawaii.png',mimetype='image/png')
    elif(feature == 'precipitation'):
        return send_file('figures/PrecipitationAnalysis_Hawaii.png',mimetype='image/png')
    elif(feature == 'trip_average'):
        return send_file('figures/Tripavg.png',mimetype='image/png')
    elif(feature == 'daily_normals'):
        return send_file('figures/trip_dailynormals.png',mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)