#!/usr/bin/python2.7

# include function for test our modules
import sys
import getopt
import numpy   as np
import common  as cmn
import defects as df
import init_server
#import speed   as sp
import defects as sp # should be removed when updaing speed is done
import turns   as tr
#import position as pos
import behavior_defects as bd
#import road_quality as rq

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def test_module(module_name):
    if module_name == "position_module":        
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name 
        test_position_module("test_data/accelerometer_test.output", "yes")

    elif module_name == "road_quality_module":
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_road_quality_module("test_data/road_quality_test.output", "yes", "express")

    elif module_name == "road_quality_module_full":
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_road_quality_module("test_data/client_test.output", "yes", "full")

    elif module_name == "behavior_defects_module_express":
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_behavior_defects_module("test_data/behavior_defects_test.output", "yes", "express")

    elif module_name == "behavior_defects_module_full":
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_behavior_defects_module("test_data/client_test.output", "yes", "full")

    elif module_name == "speed_module":
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_speed_module("test_data/accelerometer_test.output", "yes")

    elif module_name == "turns_module" :
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_turns_module("test_data/compass_test.output", "yes")

    elif module_name == "defects_module" :
        print bcolors.HEADER + "Start module: " + bcolors.ENDC, module_name
        test_defects_module("test_data/accelerometer_test.output", "yes")

    else :
        print bcolors.FAIL + 'No module with name'+ bcolors.ENDC, module_name
    return

def test_position_module(filename, plot):
    # position data structure: time,lat,lon,speed,elapsed_time
    return

def test_road_quality_module(filename, plot, test_type):
    # initialize module for testing
    train_values    = 1
    train_trees     = 10
    filename_train  = "train_data/road_quality_data.output"
    init_server.init_road_quality_module(filename_train, train_values, train_trees)

    if test_type == "full": # generate new dataset
        print bcolors.HEADER + "initialize depend modules" + bcolors.ENDC
        init_server.init_speed_module   ("train_data/speed_acc_data.output",   10, 10)
        init_server.init_turns_module   ("train_data/turns_com_data.output",    5, 10)
        init_server.init_defects_module ("train_data/speed_acc_data.output",   10, 10)
        init_server.init_behavior_defects_module("train_data/behavior_defects_data.output", 1, 10) 
        print bcolors.OKGREEN + "Done! " + bcolors.ENDC
 
        # load depend test data and classify actions
        # structure: time,accx,accy,accz,compass,lat,lon,speed
        test_values = 10
        
        print bcolors.HEADER + "Start getting speed data" + bcolors.ENDC
        test_speed_data = cmn.aver_std_array(cmn.load_data(filename, (2,)), test_values)
        test_speed_data = test_speed_data.reshape(len(test_speed_data)/2, 2)
        predicted_speed = df.predicted(test_speed_data)
        predicted_speed = predicted_speed.reshape(len(predicted_speed), 1)
        print bcolors.OKGREEN + "Done! speed data:\n" + bcolors.ENDC, predicted_speed

        print bcolors.HEADER + "Start getting turns data" + bcolors.ENDC
        test_turns_data = cmn.get_diff_array(cmn.load_data(filename, (4,)))
        test_turns_data = cmn.aver_std_array(test_turns_data, test_values)
        test_turns_data = test_turns_data.reshape(len(test_turns_data)/2, 2)
        predicted_turns = df.predicted(test_turns_data)
        predicted_turns = predicted_turns.reshape(len(predicted_turns), 1)
        print bcolors.OKGREEN + "Done! turns data:\n" + bcolors.ENDC, predicted_turns
   
        print bcolors.HEADER + "Start getting defects data" + bcolors.ENDC
        test_defects_data = cmn.aver_std_array(cmn.load_data(filename, (3,)), test_values)
        test_defects_data = test_defects_data.reshape(len(test_defects_data)/2, 2)
        predicted_defects = df.predicted(test_defects_data)
        predicted_defects = predicted_defects.reshape(len(predicted_defects), 1)
        print bcolors.OKGREEN + "Done! defects data:\n" + bcolors.ENDC, predicted_defects

        print bcolors.HEADER + "Start getting behavior defects data" + bcolors.ENDC
        test_behavior_defects_data = np.hstack((predicted_speed, predicted_turns, predicted_defects))
        predicted_behavior_defects = bd.predicted(test_behavior_defects_data)
        predicted_behavior_defects = predicted_behavior_defects.reshape(len(predicted_behavior_defects), 1)
        print bcolors.OKGREEN + "Done! defects data:\n" + bcolors.ENDC, predicted_defects

        print bcolors.HEADER + "Start generating test data" + bcolors.ENDC
        test_times = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
        test_data  = cmn.sum_array(predicted_behavior_defects, test_values)
        print bcolors.OKGREEN + "Done! test_data:\n" + bcolors.ENDC, test_data
        return

    elif test_type == "express":  
        # use default dataset
        # structure: time,low_defects,high_defects,lat,lon,label
        print bcolors.HEADER + "Start getting test data" + bcolors.ENDC
        test_values = 1
        test_low_defects_data   = cmn.label_array(cmn.load_data(filename, (1,)), values)
        test_low_defects_data   = test_low_defects_data.reshape(len(test_low_defects_data), 1)
        test_high_defects_data  = cmn.label_array(cmn.load_data(filename, (2,)), values)
        test_high_defects_data  = test_high_defects_data.reshape(len(test_high_defects_data), 1)
        test_tent_defects_data  = cmn.label_array(cmn.load_data(filename, (3,)), values)
        test_tent_defects_data  = test_tent_defects_data.reshape(len(test_tent_defects_data), 1)

        test_data = np.hstack((test_low_defects_data, test_high_defects_data, test_tent_defects_data))
        test_times = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
        print bcolors.OKGREEN + "Done! test_data:\n" + bcolors.ENDC, test_data
    else :
        print bcolor.FAIL + "road_quality_module: invalid test type, exit" + bcolors.ENDC
        return

    # choose test data sources by test type
    if test_type == "full":
        # generate new dataset
        init_server.init_speed_module   ("train_data/speed_acc_data.output",   10, 10)
        init_server.init_turns_module   ("train_data/turns_acc_data.output",   10, 10)
        init_server.init_defects_module ("train_data/defects_acc_data.output", 10, 10)
        init_server.init_behavior_defects_module("train_data/behavior_defects_data.output", 10, 10)
        
    elif test_type == "express":
        # use default dataset
        # structure: time,low_defects,high_defects
        test_values = 1
        test_data   = cmn.aver_std_array(cmn.load_data(filename, (2,)), test_values)
        test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
        test_data = test_data.reshape(len(test_data)/2, 2)
        rq.find_actions(test_data, test_times)

    else :
        print "road_quality_module: invalid test type, exit"
        return

    # analysis of set of defects and determine road quality

    # compare with previous results of road quality analysis

    # update road quality using voting procedure
    return

def test_behavior_defects_module(filename, plot, test_type):
    # initialize modules
    train_values    = 1
    train_trees     = 10
    filename_train  = "train_data/behavior_defects_data.output"
    init_server.init_behavior_defects_module(filename_train, train_values, train_trees)
    
    if test_type == "full": # generate new dataset
        print bcolors.HEADER + "initialize depend modules" + bcolors.ENDC
        init_server.init_speed_module   ("train_data/speed_acc_data.output", 10, 10)
        init_server.init_turns_module   ("train_data/turns_com_data.output",  5, 10)
        init_server.init_defects_module ("train_data/speed_acc_data.output", 10, 10)
        print bcolors.OKGREEN + "Done! " + bcolors.ENDC
 
        # load depend test data and classify actions
        # structure: time,accx,accy,accz,compass,lat,lon,speed
        test_values = 10
        
        print bcolors.HEADER + "Start getting speed data" + bcolors.ENDC
        test_speed_data = cmn.aver_std_array(cmn.load_data(filename, (2,)), test_values)
        test_speed_data = test_speed_data.reshape(len(test_speed_data)/2, 2)
        predicted_speed = df.predicted(test_speed_data)
        predicted_speed = predicted_speed.reshape(len(predicted_speed), 1)
        print bcolors.OKGREEN + "Done! speed data:\n" + bcolors.ENDC, predicted_speed

        print bcolors.HEADER + "Start getting turns data" + bcolors.ENDC
        test_turns_data = cmn.get_diff_array(cmn.load_data(filename, (4,)))
        test_turns_data = cmn.aver_std_array(test_turns_data, test_values)
        test_turns_data = test_turns_data.reshape(len(test_turns_data)/2, 2)
        predicted_turns = df.predicted(test_turns_data)
        predicted_turns = predicted_turns.reshape(len(predicted_turns), 1)
        print bcolors.OKGREEN + "Done! turns data:\n" + bcolors.ENDC, predicted_turns
    
        print bcolors.HEADER + "Start getting defects data" + bcolors.ENDC
        test_defects_data = cmn.aver_std_array(cmn.load_data(filename, (3,)), test_values)
        test_defects_data = test_defects_data.reshape(len(test_defects_data)/2, 2)
        predicted_defects = df.predicted(test_defects_data)
        predicted_defects = predicted_defects.reshape(len(predicted_defects), 1)
        print bcolors.OKGREEN + "Done! defects data:\n" + bcolors.ENDC, predicted_defects

        print bcolors.HEADER + "Start generating test data" + bcolors.ENDC
        test_times = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
        test_data  = np.hstack((predicted_speed, predicted_turns, predicted_defects))
        print bcolors.OKGREEN + "Done! test_data:\n" + bcolors.ENDC, test_data

    elif test_type == "express":  
        # use default dataset
        # structure: time,speed,turn,defect,lat,lon
        print bcolors.HEADER + "Start getting test data" + bcolors.ENDC
        test_values = 1
        test_speed_data   = cmn.label_array(cmn.load_data(filename, (1,)), values)
        test_speed_data   = test_speed_data.reshape(len(test_speed_data), 1)
        test_turns_data   = cmn.label_array(cmn.load_data(filename, (2,)), values)
        test_turns_data   = test_turns_data.reshape(len(test_turns_data), 1)
        test_defects_data = cmn.label_array(cmn.load_data(filename, (3,)), values)
        test_defects_data = test_defects_data.reshape(len(test_defects_data), 1)
        test_data = np.hstack((test_speed_data, test_turns_data, test_defects_data))

        test_times = cmn.label_array(cmn.load_data(filename, (6,)), test_values)
        print bcolors.OKGREEN + "Done! test_data:\n" + bcolors.ENDC, test_data
    else :
        print bcolor.FAIL + "behavior_defects_module: invalid test type, exit" + bcolors.ENDC
        return

    # plot result is not used currently

    # skip turns (angle > 10)

    # skip waiting (speed ~ 0)

    # check is arrays is empty

    # get new types for defects
    bd.find_actions(test_data, test_times)
    
    # writing defects to DB is not used in test module
    #bd.add_defects()

    return

def test_speed_module(filename, plot):
    # initialize speed module
    train_values    = 10
    train_trees     = 15
    filename_train  = "train_data/speed_acc_data.output"
    init_server.init_speed_module(filename_train, train_values, train_trees) 
    
    # load test data
    test_values = 10
    test_data   = cmn.aver_std_array(cmn.load_data(filename, (2,)), test_values)
    test_data   = test_data.reshape(len(test_data)/2, 2)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)

    # plot result
    if plot == "yes" :
        train_data      = cmn.aver_std_array(cmn.load_data(filename_train, (2,)), train_values)
        train_data      = train_data.reshape(len(train_data)/2, 2)
        train_predicted = cmn.label_array(cmn.load_data(filename_train, (4,)), train_values)
        xx, yy = cmn.get_grid(test_data[:, [0, 1]])
        test_predicted = sp.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        cmn.plot_2D_data(test_data, test_predicted, test_data, sp.predicted(test_data), [-5.0, 5.0], [-0.1, 2.5]);

    # start finding by time
    sp.find_actions(test_data, test_times)
    return

def test_turns_module(filename, plot):
    # initialize turns module 
    train_values   = 10
    train_trees    = 7
    filename_train = "train_data/turns_com_data.output"
    init_server.init_turns_module(filename_train, train_values, train_trees)

    # load test data
    test_values = 10
    test_aver_data  = cmn.aver_std_array(cmn.load_data(filename, (1,)), test_values)
    test_data   = cmn.get_diff_array(cmn.load_data(filename, (1,)))
    test_data   = cmn.aver_std_array(test_data, test_values)
    test_data   = np.array(test_data).reshape(len(test_data)/2, 2)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
    
    # plot results
    if plot == "yes" :
        train_data      = cmn.get_diff_array(cmn.load_data(filename_train, (1,)))
        train_data      = cmn.aver_std_array(train_data, train_values)
        train_data      = train_data.reshape(len(train_data)/2, 2)
        train_predicted = cmn.label_array(cmn.load_data(filename_train, (2,)), train_values)
        xx, yy = cmn.get_grid(train_data[:, [0, 1]])
        train_predicted = tr.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        cmn.plot_2D_data(train_data, train_predicted, test_data, tr.predicted(test_data), [-2.0, 2.0], [-0.1, 1.5]);

    # start finding by time
    tr.find_actions(test_data, test_times)
    return

def test_defects_module(filename, plot):
    # initialize defect module
    train_values    = 10
    train_trees     = 10
    filename_train  = "train_data/speed_acc_data.output"
    init_server.init_defects_module(filename_train, train_values, train_trees)

    # load test data
    test_values = 10
    test_data   = cmn.aver_std_array(cmn.load_data(filename, (3,)), test_values)
    test_data   = test_data.reshape(len(test_data)/2, 2)
    test_times  = cmn.label_array(cmn.load_data(filename, (0,)), test_values)
    print "test_data", test_data

    # plot results
    if plot == "yes" :
        train_data      = cmn.aver_std_array(cmn.load_data(filename_train, (3,)), train_values)
        train_data = train_data.reshape(len(train_data)/2, 2)
        train_predicted = cmn.label_array(cmn.load_data(filename_train, (4,)), train_values)
        xx, yy = cmn.get_grid(test_data[:, [0, 1]])
        test_predicted = df.predicted(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        cmn.plot_2D_data(test_data, test_predicted, train_data, train_predicted, [0.0, 20.0], [-0.1, 10.0]);

    # start finding by time
    df.find_actions(test_data, test_times)
    return

# start point
def main(argv):
    print "Welcome to our test module!"
    test_list = "List of tests: \n"
    test_list = test_list + 'speed_module,             turns_module,    defects_module\n'
    test_list = test_list + 'behavior_defects_full,    behavior_defects_express\n' 
    test_list = test_list + 'position_module\n'
    test_list = test_list + 'road_quality_module_full, road_quality_module_express \n'
    
    usage_tip = 'Usage: test.py -t <test_name>\nGet list of tests: test.py -l'
    try:
        opts, args = getopt.getopt(argv,"hlt:")
    except getopt.GetoptError:
        print usage_tip
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print usage_tip
            sys.exit()
	elif opt == "-l":
            print test_list
            sys.exit()
        elif opt == "-t":
            test_module(arg)
            sys.exit()
    print "No valid params, exit..."
    print usage_tip
    return

if __name__ == "__main__":
   main(sys.argv[1:])
