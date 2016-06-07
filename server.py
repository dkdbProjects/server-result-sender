#!/usr/bin/python
#from flask import abort
#!flask/bin/python

from flask import Flask, jsonify, abort, request
from threading import Timer
from flask_restful import reqparse
from flask.ext.mysqldb import MySQL

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
mysql = MySQL(app)
app.config.from_pyfile('server.cfg')

@app.route("/get_defect_map/<float:lat>/<float:lon>/<int:zoom>", methods=['GET'])
def get_map(lat, lon, zoom):
    # get polylines from db in nearest area of user position

    # create reply
    result = "<strong>" + str(lat) + "," + str(lon) + "," + str(zoom) + "</strong>"
    # return result
    return result

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
    print "com_data is ", com_data
    predicted_turns = tr.predicted(com_data)
    print predicted_turns
 
    acc_data = cmn.aver_std_array(acc_data, values)
    acc_data = acc_data.reshape(1, 2)
    print "acc_data is ", acc_data
    predicted_speed = sp.predicted(acc_data)
    print predicted_speed

    def_data = cmn.aver_std_array(def_data, values)
    def_data = def_data.reshape(1, 2)
    print "def_data is ", def_data
    predicted_defects = df.predicted(def_data)
    print predicted_defects

    test_data  = np.hstack((predicted_speed.item(0), predicted_turns.item(0), predicted_defects.item(0)))
    test_data  = test_data.reshape(1, 3)
    print test_data
    _status = bd.predicted(test_data).item(0) 

    return jsonify(status=_status, lat=_lat, lon=_lon)

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

@app.route("/", methods=['GET']) 
def init(): 
# initialize modules for classification 
    print bcolors.HEADER + "Initialize modules" + bcolors.ENDC 
    init_server.init_speed_module ("train_data/speed_acc_data.output", 10, 15) 
    init_server.init_turns_module ("train_data/turns_com_data.output", 5, 10) 
    init_server.init_defects_module ("train_data/defects_acc_data.output", 5, 15) 
    init_server.init_behavior_defects_module("train_data/behavior_defects_data.output", 1, 10) 
    init_server.init_road_quality_module("train_data/road_quality_data.output", 1, 10) 
    print bcolors.OKGREEN + "Done! " + bcolors.ENDC 
    return "<strong>Initialization done!</strong>" 
    # run app 

if __name__ == '__main__': 
    init() 
    # run app 
    app.run()
