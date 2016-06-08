#!/usr/bin/python
#from flask import abort
#!flask/bin/python

from flask import Flask, jsonify, abort, request
from threading import Timer
from flask_restful import reqparse
from flask.ext.mysqldb import MySQL

import os
import json
import numpy    as np
import common   as cmn
import defects  as df
import speed    as sp
import turns    as tr
import position as pos
import behavior_defects as bd
import road_quality as rq
import init_server

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
@app.route("/update_map", methods=['GET'])
def update_map():
    # foreach road section from road_section_table
        # get defect list from defects_table and count defects by type
        # normalize counts (<1) 
        # predict road quality
        # write predicted result in road_section_table
    cursor   = mysql.connection.cursor()
    query = """
UPDATE   
  dkdbprojects.road_sections, 
  (SELECT section_id, defect_type FROM 
      (SELECT section_id, defect_type, COUNT(1) AS num FROM dkdbprojects.defects GROUP BY section_id ORDER BY num DESC) 
  x GROUP BY section_id) a  
SET dkdbprojects.road_sections.section_type = a.defect_type 
WHERE dkdbprojects.road_sections.section_id = a.section_id;
"""
    print bcolors.HEADER +"Exectute: \n" + bcolors.ENDC, query
    cursor.execute(query)
    return "<strong>Updated!</strong>"

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
#@app.route("/get_defect_map/<float:lat>/<float:lon>/<int:zoom>", methods=['GET'])
#def get_map(lat, lon, zoom):
@app.route("/get_defect_map", methods=['GET'])
def get_map():
    update_map()
    _lines = get_road_sections()
    return jsonify(lines=_lines)

def get_road_sections():
    cursor   = mysql.connection.cursor()
    query = """SELECT startpoint.lat, startpoint.lon, endpoint.lat, endpoint.lon, section_type FROM  dkdbprojects.road_sections 
JOIN  dkdbprojects.section_points AS startpoint ON dkdbprojects.road_sections.start_point = startpoint.point_id 
JOIN  dkdbprojects.section_points AS endpoint   ON dkdbprojects.road_sections.end_point   = endpoint.point_id ;"""
    print bcolors.HEADER +"Exectute: \n" + bcolors.ENDC, query
    cursor.execute(query)
    data = cursor.fetchall()
    _lines = []
    # get list of road sections near the user position
    for row in data:
        line = {"start_lat": row[0], "start_lon": row[1], "end_lat": row[2], "end_lon": row[3], "color": row[4]}
        _lines.append(line)
    return _lines

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
@app.route("/send_collected_data", methods=['POST'])
def send_data():
    # get data
    print bcolors.OKBLUE + "/send_collected, POST" + bcolors.ENDC
    try:
        print bcolors.HEADER + "Try get data..." + bcolors.ENDC
        separator = ','
        data     = request.json
        _values  = np.fromstring(data.get("values"), sep=separator)[0]
        _lat     = np.fromstring(data.get("lat"),    sep=separator)[0]
        _lon     = np.fromstring(data.get("lon"),    sep=separator)[0]
        acc_data = np.fromstring(data.get("acc_data"), sep=separator)
        def_data = np.fromstring(data.get("def_data"), sep=separator)
        com_data = np.fromstring(data.get("com_data"), sep=separator)
        tim_data = np.fromstring(data.get("tim_data"), sep=separator)
        print bcolors.OKGREEN + "Done!" + bcolors.ENDC
    except Exception as e:
        print bcolors.FAIL + "get_position: there are an exception! Pls, check data!" + bcolors.ENDC
        abort(400)

    # TODO: check data 
    # sizeof acc_data, com_data and tim_data should be the same

    # prepare data for calculation
    # TODO: should be changed, currently we need to send request frequently
    print bcolors.WARNING + "Ignore values from request..." + bcolors.ENDC
    values = len(com_data)

    com_data = cmn.get_diff_array(com_data)
    com_data = cmn.aver_std_array(com_data, values)
    com_data = com_data.reshape(1, 2)
    predicted_turns = tr.predicted(com_data)
 
    acc_data = cmn.aver_std_array(acc_data, values)
    acc_data = acc_data.reshape(1, 2)
    predicted_speed = sp.predicted(acc_data)

    def_data = cmn.aver_std_array(def_data, values)
    def_data = def_data.reshape(1, 2)
    predicted_defects = df.predicted(def_data)

    test_data  = np.hstack((predicted_speed.item(0), predicted_turns.item(0), predicted_defects.item(0)))
    test_data  = test_data.reshape(1, 3)
    print test_data
    _status = bd.predicted(test_data).item(0)
    print "Status is ", _status 
    if _status == 0:
        return jsonify(status=_status, lat=_lat, lon=_lon)
    # write defect to defect_table (facepalm version...)
    cursor   = mysql.connection.cursor()
    direction = predicted_turns.item(0) # TODO should be 0 or 1:

    query = """SELECT section_id FROM  dkdbprojects.road_sections 
JOIN  dkdbprojects.section_points AS startpoint ON dkdbprojects.road_sections.start_point = startpoint.point_id 
JOIN  dkdbprojects.section_points AS endpoint   ON dkdbprojects.road_sections.end_point   = endpoint.point_id 
WHERE 
(
    (startpoint.lat < """ + str(_lat) + """ AND endpoint.lat > """ + str(_lat) + """ )
    OR 
    (startpoint.lat > """ + str(_lat) + """ AND endpoint.lat < """ + str(_lat) + """ )
) 
AND 
(
    (startpoint.lon < """ + str(_lon) + """ AND endpoint.lon > """ + str(_lon) + """ )
    OR
    (startpoint.lon > """ + str(_lon) + """ AND endpoint.lon < """ + str(_lon) + """ )
);"""

    print bcolors.HEADER +"Exectute: \n" + bcolors.ENDC, query
    cursor.execute(query)
    data = cursor.fetchall()
    
    if len(data) == 0:
        print bcolors.WARNING + "Result is empty!" + bcolors.ENDC
        values = str(_lat) + ", " + str(_lon) + ", " + str(direction) + ", " + str (_status)
        query = "INSERT INTO dkdbprojects.defects (lat, lon, direction, defect_type) VALUES (" + values + ");"
    else:
        print bcolors.OKGREEN + "OK!" + bcolors.ENDC + " result len is " + str (len(data))
        result = (data[0])[0]
        print result
        values = str(_lat) + ", " + str(_lon) + ", " + str(direction) + ", " + str (_status) + ", " +  str(result)
        query = "INSERT INTO dkdbprojects.defects (lat, lon, direction, defect_type, section_id) VALUES (" + values + ");"

    print bcolors.HEADER +"Exectute: \n" + bcolors.ENDC, query
    cursor.execute(query)
    mysql.connection.commit()
    
    print bcolors.OKGREEN +"OK! Exit..." + bcolors.ENDC
    return jsonify(status=_status, lat=_lat, lon=_lon)

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
@app.route("/get_position", methods=['POST'])
def get_pos():
    # get data
    print bcolors.OKBLUE + "/get_position, POST" + bcolors.ENDC
    try:
        print bcolors.HEADER + "Try get data..." + bcolors.ENDC
        separator = ','
        data = request.json
        values = np.fromstring(data.get("values"), sep=separator)[0]
        lat    = np.fromstring(data.get("lat"),    sep=separator)[0]
        lon    = np.fromstring(data.get("lon"),    sep=separator)[0]
        speed  = np.fromstring(data.get("speed"),  sep=separator)[0]
        print type(speed)
        acc_data = np.fromstring(data.get("acc_data"), sep=separator)
        com_data = np.fromstring(data.get("com_data"), sep=separator)
        tim_data = np.fromstring(data.get("tim_data"), sep=separator)
        print bcolors.OKGREEN + "Done!" + bcolors.ENDC
    except Exception as e:
        print bcolors.FAIL + "get_position: there are an exception! Pls, check data!" + bcolors.ENDC
        abort(400)

    # TODO: check data 
    # sizeof acc_data, com_data and tim_data should be the same

    # prepare data for calculation
    # TODO: should be changed, currently we need to send request frequently
    print bcolors.WARNING + "Ignore values from request..." + bcolors.ENDC
    values = len(com_data)

    # prepare data for calculation
    acc_data  = cmn.aver_std_array(acc_data, values)
    acc_data  = acc_data.reshape(len(acc_data)/2, 2)
    acceleration = acc_data.item(0,0)
    direction = cmn.aver_std_array(com_data, values).item(0)
    time = tim_data.item(-1)/1000 - tim_data.item(0)/1000
    action    = sp.predicted(acc_data)
    speed     = sp.get_speed(speed, time, acceleration, action)

   
    print "speed ", speed, " direct ", direction, " t ", time, " acc ", acceleration
    coordinates = pos.calculate_position(speed, time, direction, lat, lon)

    _lat   = "%.6f" % coordinates[0]
    _lon   = "%.6f" % coordinates[1]
    _speed = speed

    result = "lat: " + str(_lat)  + "; lon: " +str( _lon) + "; speed: " + str(_speed)
    print bcolors.OKGREEN, result, bcolors.ENDC
    return jsonify(lat=_lat, lon=_lon, speed=_speed)

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
init_type="openshift"
@app.route("/", methods=['GET']) 
def init(): 
    # initialize modules for classification 
    print bcolors.HEADER + "Initialize modules" + bcolors.ENDC 
    init_server.init_speed_module ("train_data/speed_acc_data.output", 10, 15) 
    init_server.init_turns_module ("train_data/turns_com_data.output", 5, 10) 
    init_server.init_defects_module ("train_data/defects_acc_data.output", 5, 15) 
    init_server.init_behavior_defects_module("train_data/behavior_defects_data.output", 1, 10) 
    init_server.init_road_quality_module("train_data/road_quality_data.output", 1, 10)
    connect_to_db(init_type)
    print bcolors.OKGREEN + "Done! " + bcolors.ENDC 
    return "<strong>Initialization done!</strong>" 

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################

def connect_to_db(init_type):
    # connect to database
    if init_type == "openshift" :
        app.config['MYSQL_USER']     =  os.environ['OPENSHIFT_MYSQL_DB_USERNAME']
        app.config['MYSQL_PASSWORD'] =  os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
        app.config['MYSQL_DB']       = 'dkdbprojects'
        app.config['MYSQL_HOST']     =  os.environ['OPENSHIFT_MYSQL_DB_HOST']
    else :
        app.config['MYSQL_USER']     = 'root'
        app.config['MYSQL_PASSWORD'] = '6829866'
        app.config['MYSQL_DB']       = 'dkdbprojects'
        app.config['MYSQL_HOST']     = 'localhost'
    global mysql
    mysql = MySQL()
    mysql.init_app(app)
    return

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
if __name__ == '__main__': 
    init_type="local"
    init() 
    # run app 
    app.run()
else :
    init_type="openshift"
    init()
