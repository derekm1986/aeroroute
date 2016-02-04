import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker

airportsreader.airportdictmaker()
navaidsreader.navaiddictmaker()
waypointsreader.waypointdictmaker()

#combining navaiddict and waypointdict dictionaries into one
pointsinspacedict = navaidsreader.navaiddict.copy()

for key, val in waypointsreader.waypointdict.items():
    if key in pointsinspacedict:
        pointsinspacedict[key] += val
    else:
        pointsinspacedict[key] = val

print "NAVAID and waypoints dictionaries combined"
  
inputwaypoints = []

#allows user to input waypoints to list
inputstring = raw_input("Enter input string: ")
inputstring = inputstring.upper().split()

for item in inputstring:
    
    inp = item
    
    if inp in airportsreader.airportdict:
        inp = airportsreader.airportdict[inp]
        typeelement = "airport"
    
    #elif put something here to read airways
        #typeelement = "airway"
        
    #elif put something here to read SIDs/STARs
        
    elif inp in pointsinspacedict:
        inp = pointsinspacedict[inp]
        typeelement = "point in space"
    
    else:
        print item, "not found"
        exit()
    combinerlist = []
    combinerlist.append([item, typeelement, inp])
    inputwaypoints.append(combinerlist[0])

#detection of multiples happens here
for waypoints in inputwaypoints:
    if len(waypoints[2]) == 1: #only one lat/long was found
        waypoints[2] = waypoints[2][0]
    else:
        print "Multiple items were found with name", waypoints[0], "...need more programming.  Without further programming, first lat/long will be used."
        
        #put logic here
        
        waypoints[2] = waypoints[2][0] #remove this when you make logic to do something with multiple lat/longs
        
#takes inputted waypoints and turns them into a list of waypoint pairs
waypointpairs = pairmaker.pairmaker(inputwaypoints)

#takes waypoint pairs and uses vincenty() to find the total distance
sumdistance = 0.00 #establish sumdistance and put zero in it
    
for pairs in waypointpairs: #find distance of each waypointpair and sum together
    pairdistance = vincenty.vincenty(*pairs)
    sumdistance = sumdistance + pairdistance

print sumdistance