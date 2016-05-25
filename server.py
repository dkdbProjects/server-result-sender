#!/usr/bin/python
#from flask import abort
#!flask/bin/python

import speed
from threading import Timer
from flask import Flask, jsonify, abort, request
import position


last_speed = []
last_coordinate = []
i = 0
tasks = 0
time_for_acc = []

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

tasks = [
    {
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/taskspost', methods=['POST'])
def create_task():
    #print(request.json['title'])
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': "description",
        'done': True
    }
    print(request.json['title'])
    request_split(request.json['title'])
    print(x_coordinate)
    string = "gps;" + x_coordinate + "," + y_coordinate + ";" + "speed;" + speed;
    print(string)
    return jsonify({'result': string}), 200

def request_split(requestForSplit):
    temp = requestForSplit.split(';')
    string = []
    timeForAcc = []
    timeForCompas = []
    acc = []
    compas = []
    count = 1
    i = 0
    for element in temp:
        if temp[count] == "last_coordinates":
            break        
        string = temp[count].split(",")
        for element in string:
            if i == 0:
                timeForAcc.append(string[i])
            if i == 1 or i == 2 or i == 3:
                acc.append(string[i])
            if i == 4:
                timeForCompas.append(string[i])
            if i == 5:
                compas.append(string[i])
                i = 0
                continue
            i = i + 1
        count = count + 1
    last_coordinate = temp[count+1].split(",")
    global x_coordinate
    x_coordinate = str(last_coordinate[0])
    global y_coordinate
    y_coordinate = str(last_coordinate[1])
    global speed
    speed = str(temp[count+3])
    print("timeForAcc")
    print(timeForAcc)
    print("acc")
    print(acc)
    print("timeForCompas")
    print(timeForCompas)
    print("compas")
    print(compas)
    print("x_coordinate")
    print(x_coordinate)
    print("y_coordinate")
    print(y_coordinate)
	
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"



if __name__ == '__main__':
    speed.init()
    #app.run()
    list_of_speed = speed.start_speed()
    print(len(list_of_speed))
    time_for_acc = 2
    angle = [45, 90, 10, 15, 90, 90, 90, 90]
    x_coordinate = 10
    y_coordinate = 20
    coordinates = position.calculate_position(list_of_speed,time_for_acc,angle,x_coordinate,y_coordinate)
    x_coordinate = coordinates[0]
    y_coordinate = coordinates[1]
    print("x")
    print(x_coordinate)
    print("y")
    print(y_coordinate)

