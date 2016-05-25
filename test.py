#!/usr/bin/python2.7

# include function for test our modules
import sys
import getopt
import numpy   as np
import common as cmn
import defects as df
#import speed   as sp
#import turns   as tr
#import position as pos
#import road_quality as rq

def test_module(module_name):
    if module_name == "position_module":         
        test_position_module("test_data/accelerometer_test.output")
    elif module_name == "road_quality_module":
        test_road_quality_module("test_data/accelerometer_test.output")
    elif module_name == "speed_module":
        test_speed_module("test_data/accelerometer_test.output")
    elif module_name == "turns_module" :
        test_turns_module("test_data/accelerometer_test.output")
    elif module_name == "defects_module" :
        test_defects_module("test_data/accelerometer_test.output")
    else :
        print 'No module with name', module_name
    return

def test_position_module():
    # position data structure: time,lat,lon,speed
    return

def test_road_quality_module():
    # road_quality data structure: time,defect,turn,speed
    return

def test_speed_module(filename):
    print "test_speed_module: Warning! This function currently use defect_module, not speed_module!"
    # should use sp instead df
    # will changed when functions is added

    # initialize defect module
    train_values    = 10
    train_trees     = 10
    filename_train  = "train_data/speed_acc_data.output"
    # defects data use default accelerometer.output
    # accelerometer.output: time,accx,accy,accz,label*
    train_data      = cmn.aver_std_array(cmn.load_data(filename_train, (2,)), train_values)
    train_predicted = cmn.label_array(cmn.load_data(filename_train, (4,)), train_values)
    train_data = train_data.reshape(len(train_data)/2, 2)
    df.init_defect_regression(train_values, train_trees, train_data, train_predicted)

    # test defect module
    test_values = 10
    test_data   = cmn.aver_std_array(cmn.load_data(filename, (2,)), test_values)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
    test_data = test_data.reshape(len(test_data)/2, 2)
    xx, yy = cmn.get_grid(test_data[:, [0, 1]])
    test_predicted = df.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    cmn.plot_2D_data(test_data, test_predicted, train_data, train_predicted, [-5.0, 5.0], [-0.1, 2.5]);
    df.find_actions(test_data, test_times)
    return

def test_turns_module(filename):
    # initialize turns module 
    train_values   = 10
    train_trees    = 10
    filename_train = "train_data/turn_com_data.output"
    # turns use default compass.output
    # compass.output: time,magn,label*
    train_data      = cmn.aver_std_array(cmn.load_data(filename_train, (1,)), train_values)
    train_predicted = cmn.label_array(cmn.load_data(filename_train, (2,)), train_values)
    #tr.init_defect_regression(train_values, train_trees, train_data, train_predicted)

    # test defect module
    test_values = 10
    test_data   = cmn.aver_std_array(cmn.load_data(filename, (1,)), test_values)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
    test_data   = test_data.reshape(len(test_data)/2, 2)
    xx, yy = cmn.get_grid(test_data[:, [0, 1]])
    test_predicted = tr.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    #plot_2D_data(test_data, tr.predicted(test_data), train_data, train_predicted, [-5.0, 5.0], [-2.0, 2.0]);
    #tr.find_actions(test_data, test_times)
    return

def test_defects_module(filename):
    # initialize defect module
    train_values    = 10
    train_trees     = 10
    filename_train  = "train_data/speed_acc_data.output"
    # defects data use default accelerometer.output
    # accelerometer.output: time,accx,accy,accz,label*
    train_data      = cmn.aver_std_array(cmn.load_data(filename_train, (3,)), train_values)
    train_predicted = cmn.label_array(cmn.load_data(filename_train, (4,)), train_values)
    train_data = train_data.reshape(len(train_data)/2, 2)
    df.init_defect_regression(train_values, train_trees, train_data, train_predicted)

    # test defect module
    test_values = 10
    test_data   = cmn.aver_std_array(cmn.load_data(filename, (3,)), test_values)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
    test_data = test_data.reshape(len(test_data)/2, 2)
    xx, yy = cmn.get_grid(test_data[:, [0, 1]])
    test_predicted = df.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    cmn.plot_2D_data(test_data, test_predicted, train_data, train_predicted, [-20.0, 20.0], [-0.1, 10.0]);
    df.find_actions(test_data, test_times)
    return


# start point
def main(argv):
    print "Welcome to our test module!"

    try:
        opts, args = getopt.getopt(argv,"hlt:")
    except getopt.GetoptError:
        print 'Usage: test.py -t <test_name>'
        print 'Get list of tests: test.py -l'
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: test.py -t <test_name>'
            print 'Get list of tests: test.py -l'
            sys.exit()
	elif opt == "-l":
            print 'List of tests:'
            print 'speed_module, turns_module, defects_module, position_module, road_quality_module'
            sys.exit()
        elif opt == "-t":
            print arg
            test_module(arg)
            sys.exit()
    print "No params, exit..."
    print 'Usage: test.py -t <test_name>'
    print 'Get list of tests: test.py -l'
    return

if __name__ == "__main__":
   main(sys.argv[1:])
