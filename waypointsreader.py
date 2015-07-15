# This file parses the vasFMC format Waypoints.txt file
# Waypoints.txt file must be in same directory

def waypointdictmaker():

    waypoint_file = open("Waypoints.txt")

    global waypointdict

    waypointdict = {} # make an empty dictionary

    for line in waypoint_file:
        waypointid, waypointlat, waypointlong, waypointregion = line.rstrip().split("|")
        waypointlatwithdecimal = waypointlat[:len(waypointlat)-6] + "." + waypointlat[len(waypointlat)-6:] #6 decimal places
        waypointlongwithdecimal = waypointlong[:len(waypointlong)-6] + "." + waypointlong[len(waypointlong)-6:] #6 decimal places
        waypointdict.setdefault(waypointid, []).append((waypointlatwithdecimal, waypointlongwithdecimal))

    waypoint_file.close()
    
    print "Waypoints loaded into memory"