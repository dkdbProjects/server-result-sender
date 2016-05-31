#!/usr/bin/python
# Description:  Here we will determine user position
# Dependencies: speed.py; turns.py;
import math
import utm

def calculate_position(speed,time,angle,x,y):
    i = 0
    time_dif = time[len(time)-1] - time[0]
    print("time")
    print(time_dif)
    dif_x = 0
    dif_y = 0
    speed_av = sum(speed)/len(speed)
    angle_av = sum(angle)/len(angle)
    dif_x = speed_av*5/18*math.sin(angle_av*math.pi/180)*(time_dif)
    dif_y = speed_av*5/18*math.cos(angle_av*math.pi/180)*(time_dif)
    utmcoor = utm.from_latlon(x,y)
    print(utmcoor)
    newx = utmcoor[0] + dif_x;
    newy = utmcoor[1] + dif_y;
    print(utm.to_latlon(newx,newy,utmcoor[2],utmcoor[3]))
    coordinates = utm.to_latlon(newx,newy,utmcoor[2],utmcoor[3])
    return (coordinates)


