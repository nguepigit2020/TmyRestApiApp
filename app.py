from flask import Flask, render_template, request, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import yaml

app = Flask(__name__)
CORS(app) # Allow CORS for all routes
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)


### This is the model of our app and also the way that we are going to store the data in the database
class TmyCong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Integer, nullable=False)
    technology = db.Column(db.String(50), nullable=False)
    pv_description = db.Column(db.String(255))
    tilt = db.Column(db.Float)
    azimuth = db.Column(db.Float)
    tracker_description = db.Column(db.String(255))
    gcr = db.Column(db.Float)
    axis_azimuth = db.Column(db.Float)
    max_angle = db.Column(db.Float)

    request_id = db.Column(db.String(255))
    p50 = db.Column(db.Boolean, nullable=False)
    p75 = db.Column(db.Boolean, nullable=False)
    p90 = db.Column(db.Boolean, nullable=False)
    p10 = db.Column(db.Boolean, nullable=False)
    p99 = db.Column(db.Boolean, nullable=False)
    ambient_temperature = db.Column(db.Boolean, nullable=False)
    pm_2_5 = db.Column(db.Boolean, nullable=False)
    pm_10 = db.Column(db.Boolean, nullable=False)
    relative_humidity = db.Column(db.Boolean, nullable=False)
    precipitable_water = db.Column(db.Boolean, nullable=False)
    wind_direction = db.Column(db.Boolean, nullable=False)
    granularity = db.Column(db.String(50), nullable=False)

    def __init__(self, project_name, latitude, longitude, altitude, technology,
                 pv_description, tilt, azimuth, tracker_description, gcr,
                 axis_azimuth, max_angle, request_id, p50, p75, p90, p10, p99,
                 ambient_temperature, pm_2_5, pm_10, relative_humidity,
                 precipitable_water, wind_direction, granularity):
        self.project_name = project_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.technology = technology
        self.pv_description = pv_description
        self.tilt = tilt
        self.azimuth = azimuth
        self.tracker_description = tracker_description
        self.gcr = gcr
        self.axis_azimuth = axis_azimuth
        self.max_angle = max_angle
        self.request_id = request_id
        self.p50 = stringToBoolean(p50)
        self.p75 = stringToBoolean(p75)
        self.p90 = stringToBoolean(p90)
        self.p10 = stringToBoolean(p10)
        self.p99 = stringToBoolean(p99)
        self.ambient_temperature = stringToBoolean(ambient_temperature)
        self.pm_2_5 = stringToBoolean(pm_2_5)
        self.pm_10 = stringToBoolean(pm_10)
        self.relative_humidity = stringToBoolean(relative_humidity)
        self.precipitable_water = stringToBoolean(precipitable_water)
        self.wind_direction = stringToBoolean(wind_direction)
        self.granularity = granularity

# Create the database tables
#db.create_all()


### This fuction allow us to put the data into the same structure as expected in the tmy.yml file 
def format_data(data):
    with open('tmy.yml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    config['id'] = data.id
    config['project_name'] = data.project_name 

    config['location']['latitude'] = data.latitude
    config['location']['latitude'] = data.longitude
    config['location']['altitude'] = data.altitude

    config['pv_system']['technology'] = data.technology
    config['pv_system']['pv']['description'] = data.pv_description
    config['pv_system']['pv']['tilt'] = data.tilt
    config['pv_system']['pv']['azimuth'] = data.azimuth 

    config['pv_system']['tracker']['description'] = data.tracker_description
    config['pv_system']['tracker']['gcr'] = data.gcr
    config['pv_system']['tracker']['axis_azimuth'] = data.axis_azimuth
    config['pv_system']['tracker']['max_angle'] = data.max_angle

    config['analysis']['request_id'] = data.request_id

    config['analysis']['probabilities']['P50'] = data.p50
    config['analysis']['probabilities']['P75'] = data.p75
    config['analysis']['probabilities']['P90'] = data.p90
    config['analysis']['probabilities']['P10'] = data.p10
    config['analysis']['probabilities']['P99'] = data.p99

    config['analysis']['meteo_data']['ambient_temperature'] = data.ambient_temperature
    config['analysis']['meteo_data']['pm_2_5'] = data.pm_2_5
    config['analysis']['meteo_data']['pm_10'] = data.pm_10
    config['analysis']['meteo_data']['relative_humidity'] = data.relative_humidity
    config['analysis']['meteo_data']['precipitable_water'] = data.precipitable_water
    config['analysis']['meteo_data']['wind_direction'] = data.wind_direction

    config['analysis']['granularity'] = data.granularity

    return config

##### This is use to get acces to all the configurations record
@app.route('/getall/configurations', methods=['GET'])
def get_tmy_conf():
    configurations = TmyCong.query.all()
    config_list = []

    for config in configurations:
        config_dict = format_data(config)
        config_list.append(config_dict)

    return jsonify(config_list)


### this is use to get acces to a single configuration record
@app.route('/getsingle/configuration/<int:id>', methods=['GET'])
def get_configuration(id):
    config = TmyCong.query.get(id)
    if config:
        config_dict = format_data(config)
        return jsonify(config_dict)
    else:
        return jsonify({'message': 'Configuration not found'}), 404


### This is use to create the new configuration record
@app.route('/create/configuration', methods=['POST'])
def create_configuration():
    data = request.json
    config = TmyCong(**data)
    print(config)

    db.session.add(config)
    db.session.commit()

    return jsonify({'message': 'Configuration created successfully'}), 201

### This is use to update a single configuration
@app.route('/update/configuration/<int:id>', methods=['POST'])
def update_configuration(id):
    data = request.json
    config = TmyCong.query.get(id)

    if config:
        for key, value in data.items():
            setattr(config, key, value)

        db.session.commit()
        return jsonify({'message': 'Configuration updated successfully'})
    else:
        return jsonify({'message': 'Configuration not found'}), 404

#### This methode is use to delete the configuration
@app.route('/delete/configuration/<int:id>', methods=['DELETE'])
def delete_configuration(id):
    config = TmyCong.query.get(id)

    if config:
        db.session.delete(config)
        db.session.commit()
        return jsonify({'message': 'Configuration deleted successfully'})
    else:
        return jsonify({'message': 'Configuration not found'}), 404        

### This is use to generate the yaml file
@app.route('/download_yaml/configuration/<int:id>', methods=['GET'])
def download_yaml(id):
    config = TmyCong.query.get(id)
    if config:
        config_dict = format_data(config)
        del config_dict['id']
        # Create a YAML representation of the config_dict
        yaml_data = yaml.dump(config_dict, default_flow_style=False, sort_keys=False)

        # Create a response containing the YAML data
        response = Response(yaml_data, content_type='application/x-yaml')
        response.headers["Content-Disposition"] = "attachment; filename=generated_config_{id}.yml"
        return response
    else:
        return "Configuration not found", 404  

#### This function allow us to convert string to python boolean
def stringToBoolean(s:str):
    if s == 'true':
        return True          
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)