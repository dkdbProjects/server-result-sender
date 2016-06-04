# coding: utf-8
import pandas as pd
acc = pd.read_csv("/root/server-result-sender/2805/accelerometer.output")
acc = acc.drop('action', 1)
com = pd.read_csv("/root/server-result-sender/2805/compass.output")
com = com.drop('action', 1)
com_acc = acc.merge(com, on='time_acc', how="outer")
com_acc = com_acc.drop('time', 1)
gps = pd.read_csv("/root/server-result-sender/2805/gps.geo.output")
com_acc.merge(gps, on='time_acc', how="outer")
gps = gps.drop('action', 1)
gps = gps.drop('time', 1)
full = com_acc.merge(gps, on='time_acc', how="outer")
full = full.fillna(method='ffill')
full = full.fillna(method='bfill')

full.to_csv("/root/server-result-sender/test_data/client_test.output", index=False)
