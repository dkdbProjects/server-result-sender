import numpy   as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing

def load_data(filename, cols) :
    # TODO: should be improved later
    print "load_data: Warning! This function return only one column! Be careful!"
    f = open(filename)
    f.readline()  # skip the header 
    data = np.loadtxt(f, delimiter=',', usecols=cols)
    return data

def get_grid(data):
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    return np.meshgrid(np.arange(x_min, x_max, 0.01),
                       np.arange(y_min, y_max, 0.01))

def plot_2D_data(test_data, test_predicted, train_data, train_predicted, range_x, range_y):
    plt.figure()
    plt.ylim(range_y)
    plt.xlim(range_x)
    xx, yy = get_grid(test_data[:, [0, 1]])
    plt.pcolormesh(xx, yy, test_predicted, cmap='seismic')
    plt.scatter(train_data[:, 0], train_data[:, 1], c=train_predicted, s=len(train_data[:, 1]), cmap='seismic')
    plt.show()
    return;


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
