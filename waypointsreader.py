# This file parses the vasFMC format Waypoints.txt file
# Waypoints.txt file must be in same directory

def waypointdictmaker():

    waypoint_file = open("Waypoints.txt")

    global waypointdict

    waypointdict = {} # make an empty dictionary

    for line in waypoint_file:
        waypointid, waypointlat, waypointlong, waypointregion = line.rstrip().split("|")
        waypointlatisnegative = False #establish variable
            
        if waypointlat.startswith("-"):
            waypointlatisnegative = True
            waypointlat = waypointlat[1:]
            
        if len(waypointlat) < 7:
            waypointlat = "0" * (7 - len(waypointlat)) + waypointlat
            
        waypointlatwithdecimal = waypointlat[:len(waypointlat)-6] + "." + waypointlat[len(waypointlat)-6:] #6 decimal places
            
        if waypointlatisnegative == True:
            waypointlatwithdecimal = "-" + waypointlatwithdecimal
            
            
        waypointlongisnegative = False #establish variable
            
        if waypointlong.startswith("-"):
            waypointlongisnegative = True
            waypointlong = waypointlong[1:]

        if len(waypointlong) < 7:
            waypointlong = "0" * (7 - len(waypointlong)) + waypointlong
                
        waypointlongwithdecimal = waypointlong[:len(waypointlong)-6] + "." + waypointlong[len(waypointlong)-6:] #6 decimal places
            
        if waypointlongisnegative == True:
            waypointlongwithdecimal = "-" + waypointlongwithdecimal

        
        waypointdict.setdefault(waypointid, []).append((waypointlatwithdecimal, waypointlongwithdecimal))

    waypoint_file.close()
    
    print "Waypoints loaded into memory"