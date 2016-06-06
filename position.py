#!/usr/bin/python
# Description:  Here we will determine user position
# Dependencies: speed.py; turns.py;
import math
import utm

def calculate_position(speed, time, angle, lat, lon):
    dif_x = speed * 5/18 * math.sin( angle*math.pi/180 )*time
    dif_y = speed * 5/18 * math.cos( angle*math.pi/180 )*time
    utmcoor = utm.from_latlon(lat, lon)
    newx = utmcoor[0] + dif_x;
    newy = utmcoor[1] + dif_y;
    print "old x and y ", utmcoor
    print "new x and y ", (newx, newy)
    coordinates = utm.to_latlon(newx, newy, utmcoor[2], utmcoor[3])
    print "old lat and lon ", (lat, lon)
    print "new lat and lon ", coordinates
    return (coordinates)


