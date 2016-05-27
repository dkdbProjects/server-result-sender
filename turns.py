# Import the necessary modules and libraries
import threading
import time
import numpy as np
import common as cmn
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

turns_regr = ()
np.set_printoptions(precision=3, suppress=True)

time_index = 0
prev_time = 0
 
def find_actions(data, times):
    # TODO: static vars in C-style?
    global time_index
    global prev_time
    delta_time = times[time_index] - prev_time
    row = data[time_index]
    result = predict_turn(row, delta_time/1000)
    
    prev_time = times[time_index]
    print "Time: %f" % prev_time
    time_index += 1
 
    if time_index < len(times) :
        next_call_time = (times[time_index] - prev_time)/1000.0
        print "Next call: %f" % next_call_time
        threading.Timer(next_call_time, find_actions, [data, times]).start()
    else : 
         print "time is out %d" % time_index
    return result 

def predict_turn( data, time):
    global turns_regr
    data = np.array(data).reshape(1, 2)
    result = turns_regr.predict(data)
    print "Predicted ", result
    return result

def init_turns_regression(values, trees, data, labels):
    # Fit regression model
    global turns_regr
    turns_regr = RandomForestClassifier(n_estimators=trees)
    turns_regr.fit(data[:, [0,1]], labels)
    print "init_turns, importances: ", turns_regr.feature_importances_
    return

def predicted(data):
    return turns_regr.predict(data)
