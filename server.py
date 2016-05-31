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
    result = "<strong>" , lat , "," , lon, "," , zoom , "</strong>"
    # return result
    return result

@app.route("/send_collected_data", methods=['PUT'])
def send_data():
    return "<strong>send_collected_data</strong>"

@app.route("/get_position", methods=['GET'])
def get_pos():
    data = request.json
    separator = ','

    # get data
    try:
        values = np.fromstring(data.get("values"), sep=separator)[0]
        lat    = np.fromstring(data.get("lat"),    sep=separator)[0]
        lon    = np.fromstring(data.get("lon"),    sep=separator)[0]
        speed  = np.fromstring(data.get("speed"),  sep=separator)[0]
        acc_data = np.fromstring(data.get("acc_data"), sep=separator)
        com_data = np.fromstring(data.get("com_data"), sep=separator)
        tim_data = np.fromstring(data.get("tim_data"), sep=separator)
    except Exception as e:
        print bcolors.FAIL + "get_position: there are an exception! Pls, check data!" + bcolors.ENDC
        abort(400)

    # TODO: check data 
    # sizeof acc_data, com_data and tim_data should be the same

    # prepare data for calculation
    directions = cmn.aver_std_array(com_data, values)
    times = cmn.label_array(tim_data, values)
    acc_data = cmn.aver_std_array(acc_data, values)
    acc_data = acc_data.reshape(len(acc_data)/2, 2)
    speeds = sp.calculate_speed(acc_data, sp.predicted(acc_data), times, speed)

    coordinates = pos.calculate_position(speeds, tim_data, directions, lat, lon) #, speed)

    result = "\n<strong>lat:" + str(coordinates[0]) + ";lon:" + str(coordinates[1]) + ";speed:" + str(speeds[-1]) + "</strong>\n"
    print bcolors.OKGREEN, result, bcolors.ENDC
    return result


if __name__ == '__main__':
    # initialize modules for classification
    print bcolors.HEADER + "Initialize modules" + bcolors.ENDC
    init_server.init_speed_module   ("train_data/speed_acc_data.output",   10, 10)
    init_server.init_turns_module   ("train_data/turns_com_data.output",    5, 10)
    init_server.init_defects_module ("train_data/speed_acc_data.output",   10, 10)
    init_server.init_behavior_defects_module("train_data/behavior_defects_data.output", 1, 10)
    init_server.init_road_quality_module("train_data/road_quality_data.output", 1, 10)
    print bcolors.OKGREEN + "Done! " + bcolors.ENDC
    # run app
    app.run()
