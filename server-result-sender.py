#from flask import abort
#!flask/bin/python
from threading import Timer
from flask import Flask, jsonify, abort, request

i = 0
tasks = 0

app = Flask(__name__)

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
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': True
    }
    request_split(request.json['title'])
    return jsonify({'done': True}), 200

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

def request_split(requestForSplit):
    temp = requestForSplit.split(',')
    i = 1
    count = 0
    timeForAcc = []
    timeForCompas = []
    acc = []
    compas = []
    for element in temp:
        if i == 1:
            timeForAcc.append(temp[count])
        if i == 2 or i == 3 or i == 4:
            acc.append(temp[count])
        if i == 5:
            timeForCompas.append(temp[count])
        if i == 6:
            compas.append(temp[count])
            i = 0
        i = i + 1
        count = count + 1

def read_str(i):
    if i < len(lines):
        global str
        str = lines[i]
        tasks[1] = str
        print(tasks[1])
        t = Timer(2.0, lambda: read_str(i + 1))
        t.start()
    else:
        print("end")

def timer(i):
    t = Timer(2.0, read_str(i)).start

if __name__ == '__main__':
    app.run(host='0.0.0.0')

