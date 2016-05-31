#!/usr/bin/python

# Import the necessary modules and libraries
import threading
import time
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

speed_regr = ()
np.set_printoptions(precision=3, suppress=True)


def aver_std_array( data, values ):
    # initialize new_data array
    new_data = ()
    # round by
    data = np.around(data, decimals=1)
    # reshape in 'rows' = 'len(data)/values', columns = 'values'
    rows = len(data)/values
    data.resize(rows*values, 1)
    data = np.array(data).reshape(rows, values)
    # this axis need to get line regrassion parameters
    for row in data:
        new_data = np.append(new_data, [np.average(row), np.std(row)])
        # print np.array([np.average(row), np.std(row)]);
    return new_data

def label_array( data, values ):
    new_data = ()
    data = np.array(data).astype(int)
    data.resize(len(data)/values, values)
    for row in data:
        counts = np.bincount(row)
        # print np.argmax(counts)
        new_data = np.append(new_data, [np.argmax(counts)])
    return new_data

speed_time_index = 0
speed_time_prev = 0 
def find_actions(data, times):
    # TODO: static vars in C-style?
    global speed_time_index
    global speed_time_prev
    delta_time = times[speed_time_index] - speed_time_prev
    row = data[speed_time_index]
    result = predict_defect(row, delta_time/1000)
    
    speed_time_prev = times[speed_time_index]
    print "Time: %f" % speed_time_prev
    speed_time_index += 1
 
    if speed_time_index < len(times) :
        next_call_time = (times[speed_time_index] - speed_time_prev)/1000.0
        print "Next call: %f" % next_call_time
        threading.Timer(next_call_time, find_actions, [data, times]).start()
    else : 
         print len(times)
         print "time is out %d" % speed_time_index
    return result 

def predict_defect( data, time):
    global speed_regr
    data = np.array(data).reshape(1, 2)
    predicted_test = speed_regr.predict(data)
    acceleration = data.item((0, 0))
    print "Predicted %d" % predicted_test[0]
    return predicted_test[0]

def init_speed_module(values, trees, data, labels):
    # Fit regression model
    global speed_regr
    speed_regr = RandomForestClassifier(n_estimators=trees)
    speed_regr.fit(data[:, [0,1]], labels)
    print "init_speed_module: ", speed_regr.feature_importances_
    return

def predicted(data):
   return speed_regr.predict(data)

def calculate_speed(data, predicted_data, times, speed):
    result = np.empty([1,1])
    result.fill(speed)
    prev_time = 0
    for i in np.arange (len(data) - 1) :
         delta_time = times[i] - prev_time
         prev_time = times[i]
         predicted_action = predicted_data[i]
         speed = get_speed(speed, delta_time/1000, data.item((0,0)), predicted_data[i])
         np.insert(result, len(result), speed)
    return result

def get_speed( speed, time, acceleration, action):

    print speed, time, acceleration, action
    if action == 1:
        speed = 0
    if action == 2:
        speed = speed
    if action == 3:
        speed = speed + acceleration * time * 3.6
    if action == 4:
        speed = speed + acceleration * time * 3.6

    # print speed
    print "Speed is %2.f" % speed
    return speed

