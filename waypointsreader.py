# This file parses the vasFMC format Waypoints.txt file
# Waypoints.txt file must be in AIRAC directory

from objects import PointInSpace
from objects import AmbiguousPoint

from objects import Coordinates


def waypoint_dict_maker():

    waypoint_file = open("AIRAC/Waypoints.txt")

    waypoint_dict = {}

    for line in waypoint_file:
        currentline = line.rstrip().split("|")
        waypointid = currentline[0]
        waypointlat = currentline[1]
        waypointlong = currentline[2]

        waypointlatisnegative = False  # establish variable
            
        if waypointlat.startswith("-"):
            waypointlatisnegative = True
            waypointlat = waypointlat[1:]
            
        if len(waypointlat) < 7:
            waypointlat = "0" * (7 - len(waypointlat)) + waypointlat
            
        waypointlatwithdecimal = waypointlat[:-6] + "." + waypointlat[-6:]  # 6 decimal places
            
        if waypointlatisnegative is True:
            waypointlatwithdecimal = "-" + waypointlatwithdecimal

        waypointlongisnegative = False  # establish variable
            
        if waypointlong.startswith("-"):
            waypointlongisnegative = True
            waypointlong = waypointlong[1:]

        if len(waypointlong) < 7:
            waypointlong = "0" * (7 - len(waypointlong)) + waypointlong
                
        waypointlongwithdecimal = waypointlong[:-6] + "." + waypointlong[-6:]  # 6 decimal places
            
        if waypointlongisnegative is True:
            waypointlongwithdecimal = "-" + waypointlongwithdecimal

        waypointcoordinates = Coordinates(waypointlatwithdecimal, waypointlongwithdecimal)

        waypointobj = PointInSpace(waypointid, waypointcoordinates, 'waypoint')

        if waypointid in waypoint_dict:
            if type(waypoint_dict[waypointid]) is AmbiguousPoint:
                waypoint_dict[waypointid].add_possibility(waypointobj)
            else:
                waypoint_dict[waypointid] = AmbiguousPoint(waypointid, waypoint_dict[waypointid])
                waypoint_dict[waypointid].add_possibility(waypointobj)
        else:
            waypoint_dict[waypointid] = waypointobj

    waypoint_file.close()

    return waypoint_dict
