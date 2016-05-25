#!/usr/bin/python

print(__doc__)

# Import the necessary modules and libraries
import threading
import time
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

defect_regr = ()
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

time_index = 0
prev_time = 0 
def find_actions(data, times):
    # TODO: static vars in C-style?
    global time_index
    global prev_time
    delta_time = times[time_index] - prev_time
    row = data[time_index]
    result = predict_defect(row, delta_time/1000)
    
    prev_time = times[time_index]
    print "Time: %f" % prev_time
    time_index += 1
 
    if time_index < len(times) :
        next_call_time = (times[time_index] - prev_time)/1000.0
        print "Next call: %f" % next_call_time
        threading.Timer(next_call_time, find_actions, [data, times]).start()
    else : 
         print len(times)
         print "time is out %d" % time_index
    return result 

def predict_defect( data, time):
    global defect_regr
    data = np.array(data).reshape(1, 2)
    predicted_test = defect_regr.predict(data)
    acceleration = data.item((0, 0))
    print "Predicted %d" % predicted_test[0]
    return predicted_test[0]

def init_defect_regression(values, trees, data, labels):
    # Fit regression model
    global defect_regr
    defect_regr = RandomForestClassifier(n_estimators=trees)
    defect_regr.fit(data[:, [0,1]], labels)
    print(defect_regr.feature_importances_)
    return

def predicted(data):
   return defect_regr.predict(data)
