#!/usr/bin/python

print(__doc__)

# Import the necessary modules and libraries
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing

np.set_printoptions(precision=3, suppress=True)

def get_acc_array( raw_X, values ):
    # initialize new_X array
    new_X = ()
    # round by
    raw_X = np.around(raw_X, decimals=1)
    # reshape in 'rows' = 'len(raw_X)/values', columns = 'values'
    rows = len(raw_X)/values
    raw_X.resize(rows*values, 1)
    raw_X = np.array(raw_X).reshape(rows, values)
    # this axis need to get line regrassion parameters
    for row in raw_X:
        new_X = np.append(new_X, [np.average(row), np.std(row)])
        # print np.array([np.average(row), np.std(row)]);
    return new_X

def get_label_array( raw_Y, values ):
    new_Y = ()
    raw_Y = np.array(raw_Y).astype(int)
    raw_Y.resize(len(raw_Y)/values, values)
    for row in raw_Y:
        counts = np.bincount(row)
        # print np.argmax(counts)
        new_Y = np.append(new_Y, [np.argmax(counts)])
    return new_Y

def get_grid(data):
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    return np.meshgrid(np.arange(x_min, x_max, 0.01),
                         np.arange(y_min, y_max, 0.01))

def plot_data(X_test, Y_predicted, X, Y, lim_x, lim_y):
    plt.figure()
    plt.ylim(lim_y)
    plt.xlim(lim_x)
    xx, yy = get_grid(X_test[:, [0, 1]])
    #predicted = regr.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plt.pcolormesh(xx, yy, Y_predicted, cmap='seismic')
    plt.scatter(X[:, 0], X[:, 1], c=y, s=len(X[:, 1]), cmap='seismic')
    plt.show()
    return

def calculate_speed(data, times, regr, values):
    # TODO: static vars in C-style?
    global time_index
    global speed
    global prev_time
    delta_time = times[values*time_index] - prev_time
    speed_data = data[time_index]
    speed = get_speed(speed, delta_time/1000, speed_data, regr, values)
    
    prev_time = times[values*time_index]
    print "Time: %f" % prev_time
    print speed_data
    time_index += 1
 
    if time_index < len(times) :
        next_call_time = (times[values*time_index] - prev_time)/1000.0
        threading.Timer(next_call_time, calculate_speed, [data, times, regr, values]).start()
        print "Next call: %f" % next_call_time
    else : 
         print len(times)
         print "time is out %d" % time_index
    return speed 

#t_s = 0
def get_speed( speed, time, data, regr, values):

    # predict
    print data
    data = np.array(data).reshape(1, 2)
    Y_test = regr.predict(data)
    acceleration = data.item((0, 0))
    print acceleration
    #global t_s
    #t_s = t_s + acceleration * time * 3.6
    #print "C speed is %2.f" % t_s
    if Y_test[0] == 1:
        speed = 0
        t_s = 0
    if Y_test[0] == 2:
        speed = speed
    if Y_test[0] == 3:
        speed = speed + acceleration * time * 3.6
    if Y_test[0] == 4:
        speed = speed + acceleration * time * 3.6 # ! acceleration have sign +/-

    # print speed
    print "Predicted %d" % Y_test[0]
    print "M speed is %2.f" % speed
    return speed

##########################################
# Start point ############################
##########################################

values = 10
trees=10

f = open("train_data/speed_test_2.output")
f.readline()  # skip the header

# load accelerometer training data
# 0 column is time
# 1 is X (turns)
# 2 is Y (speed)
# 3 is Z (vertical)
# 4 is action_id
data = np.loadtxt(f, delimiter=',', usecols=(2,4))
f.close()
raw_X = data[:, 0] # len is N
rows = len(raw_X)/values
X = get_acc_array(raw_X, values).reshape(rows, 2)
print len(X)

# load action_ids (labels)
# 0 is not used
# 1 is wait
# 2 is constant motion
# 3 is acceleration
# 4 is deceleration
raw_Y = data[:, 1] 
y = get_label_array(raw_Y, values)
print len(y)

# Fit regression model
regr_1 = RandomForestClassifier(n_estimators=trees)
regr_1.fit(X[:, [0,1]], y)
print(regr_1.feature_importances_)

# load check data
f2 = open("train_data/new_accelerometer.output")
f2.readline()  # skip the header
data2 = np.loadtxt(f2, delimiter=',', usecols=(0,2))
raw_X_test = data2[:, 1]
X_test = get_acc_array(raw_X_test, values).reshape(len(raw_X_test)/values, 2)

# predict
xx, yy = get_grid(X_test[:, [0, 1]])
Y_test = regr_1.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

# plot
plot_data(X_test, Y_test, X, y, [-5.0, 5.0], [-0.1, 1.5])

#exit();

# load time data
times = data2[:, 0]
print times

# start calculating speed
time_index = 7530/values
prev_time  = 0
speed = 0
calculate_speed(X_test, times, regr_1, values)
