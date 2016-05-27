import numpy   as np
import common  as cmn
import defects as df
#import speed   as sp
import defects as sp # should be removed when updaing speed is done
import turns   as tr
#import position as pos
import behavior_defects as bd
#import road_quality as rq

def init_defects_module(filename, values, trees):
    # defects module use default accelerometer.output
    # accelerometer.output: time,accx,accy,accz,label*
    train_data      = cmn.aver_std_array(cmn.load_data(filename, (3,)), values)
    train_data = train_data.reshape(len(train_data)/2, 2)
    train_predicted = cmn.label_array(cmn.load_data(filename, (4,)), values)
    df.init_defect_regression(values, trees, train_data, train_predicted)
    return

def init_speed_module(filename, values, trees):
    # speed module use default accelerometer.output
    # accelerometer.output: time,accx,accy,accz,label*
    train_data      = cmn.aver_std_array(cmn.load_data(filename, (2,)), values)
    train_data = train_data.reshape(len(train_data)/2, 2)
    train_predicted = cmn.label_array(cmn.load_data(filename, (4,)), values)
    #sp.init_speed_regression(values, trees, train_data, train_predicted)
    sp.init_defect_regression(values, trees, train_data, train_predicted)
    return

def init_turns_module(filename, values, trees):
    # turns module use default compass.output
    # compass.output: time,magn,label*
    train_data   = cmn.get_diff_array(cmn.load_data(filename, (1,)))
    train_data   = cmn.aver_std_array(train_data, values)    
    train_data   = train_data.reshape(len(train_data)/2, 2)  
    train_predicted = cmn.label_array(cmn.load_data(filename, (2,)), values)
    tr.init_turns_regression(values, trees, train_data, train_predicted)
    return

def init_position_module(filename, values, trees):
    return

def init_behavior_defects_module(filename, values, trees):
    # behavior defects module use generated file
    # structure: time,speed,turns,defects,lat,lon,labels*
    train_speed_data   = cmn.label_array(cmn.load_data(filename, (1,)), values)
    train_speed_data   = train_speed_data.reshape(len(train_speed_data), 1)
    train_turns_data   = cmn.label_array(cmn.load_data(filename, (2,)), values)
    train_turns_data   = train_turns_data.reshape(len(train_turns_data), 1)
    train_defects_data = cmn.label_array(cmn.load_data(filename, (3,)), values)
    train_defects_data = train_defects_data.reshape(len(train_defects_data), 1)

    train_data = np.hstack((train_speed_data, train_turns_data, train_defects_data))
    print train_data
    train_predicted = cmn.label_array(cmn.load_data(filename, (6,)), values)
    bd.init_behavior_defect_regression(values, trees, train_data, train_predicted)
    return

def init_road_quality_module(filename, values, trees):
    # road quality module use generated file
    # structure: time,low_defects,high_defects,label*
    print "init_road_quality_module: not done!"
    return
