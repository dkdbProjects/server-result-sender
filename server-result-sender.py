#from flask import abort
#!flask/bin/python
from threading import Timer
from flask import Flask, jsonify, abort

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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

def read_file():
    p = 1
    #fo = open("C:\Users\Dasha\Desktop\cordova-acc.txt", "r")
    with open("C:\Users\Dasha\Desktop\cordova-acc.txt") as f:
        global lines
        lines = f.read().splitlines()
    #with open('C:\Users\Dasha\Desktop\cordova-acc.txt') as fp
    #    for line in fp:
    #        print line
            #t = Timer(10.0, read_file)
            #t.start()

def read_str(i):
    if i < len(lines):
        #print(lines[i])
        #Timer(2.0, read_str(i + 1)).start
        #read_str(i + 1)
        global str
        str = lines[i]
        tasks[1] = str
        print(tasks[1])
        t = Timer(2.0, lambda: read_str(i + 1))
        t.start()
    else:
        print("end")

def timer(i):
    #t.start()
    t = Timer(2.0, read_str(i)).start
    #t.start()

if __name__ == '__main__':
    #i = 0
    read_file()
    read_str(i)
    app.run()
