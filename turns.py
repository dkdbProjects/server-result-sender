# Import the necessary modules and libraries
import threading
import time
import numpy as np
import common as cmn
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

turns_regr = ()
#np.set_printoptions(precision=3, suppress=True)

turns_time_index = 0
turns_time_prev = 0
 
def find_actions(data, times):
    # TODO: static vars in C-style?
    global turns_time_index
    global turns_time_prev
    delta_time = times[turns_time_index] - turns_time_prev
    row = data[turns_time_index]
    result = predict_turn(row, delta_time/1000)
    
    turns_time_prev = times[turns_time_index]
    print "Time: %f" % turns_time_prev
    turns_time_index += 1
 
    if turns_time_index < len(times) :
        next_call_time = (times[turns_time_index] - turns_time_prev)/1000.0
        print "Next call: %f" % next_call_time
        threading.Timer(next_call_time, find_actions, [data, times]).start()
    else : 
         print "time is out %d" % turns_time_index
    return result 

def predict_turn( data, time):
    global turns_regr
    data = np.array(data).reshape(1, 2)
    print "Data: ", data
    result = turns_regr.predict(data)
    if result[0] == 1:
        print "Predicted left"
    if result[0] == 2:
        print "Predicted straight"
    if result[0] == 3:
        print "Predicted right"

    return result

def init_turns_module(values, trees, data, labels):
    # Fit regression model
    global turns_regr
    turns_regr = RandomForestClassifier(n_estimators=trees)
    turns_regr.fit(data[:, [0,1]], labels)
    print "init_turns, importances: ", turns_regr.feature_importances_
    return

def predicted(data):
    return turns_regr.predict(data)
