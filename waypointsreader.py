# This file parses the vasFMC format Waypoints.txt file
# Waypoints.txt file must be in same directory

from objects import Pointinspace
from objects import Ambiguouselement

def waypointdictmaker():

    waypoint_file = open("AIRAC/Waypoints.txt")

    global waypointdict
    global waypointdictobj

    waypointdict = {}  # make an empty dictionary
    waypointdictobj = {}

    for line in waypoint_file:
        waypointid, waypointlat, waypointlong, waypointregion = line.rstrip().split("|")
        waypointlatisnegative = False  # establish variable
            
        if waypointlat.startswith("-"):
            waypointlatisnegative = True
            waypointlat = waypointlat[1:]
            
        if len(waypointlat) < 7:
            waypointlat = "0" * (7 - len(waypointlat)) + waypointlat
            
        waypointlatwithdecimal = waypointlat[:len(waypointlat)-6] + "." + waypointlat[len(waypointlat)-6:]  # 6 decimal places
            
        if waypointlatisnegative is True:
            waypointlatwithdecimal = "-" + waypointlatwithdecimal
            
            
        waypointlongisnegative = False  # establish variable
            
        if waypointlong.startswith("-"):
            waypointlongisnegative = True
            waypointlong = waypointlong[1:]

        if len(waypointlong) < 7:
            waypointlong = "0" * (7 - len(waypointlong)) + waypointlong
                
        waypointlongwithdecimal = waypointlong[:len(waypointlong)-6] + "." + waypointlong[len(waypointlong)-6:]  # 6 decimal places
            
        if waypointlongisnegative is True:
            waypointlongwithdecimal = "-" + waypointlongwithdecimal

        
        waypointdict.setdefault(waypointid, []).append((waypointlatwithdecimal, waypointlongwithdecimal))

        waypointobj = Pointinspace(waypointid, (waypointlatwithdecimal, waypointlongwithdecimal), 'waypoint')

        if waypointid in waypointdictobj:
            if type(waypointdictobj[waypointid]) is Ambiguouselement:
                waypointdictobj[waypointid].addpossibility(waypointobj)
            else:
                waypointdictobj[waypointid] = Ambiguouselement(waypointid, waypointdictobj[waypointid])
                waypointdictobj[waypointid].addpossibility(waypointobj)
        else:
            waypointdictobj[waypointid] = waypointobj

    waypoint_file.close()
