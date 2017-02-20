import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker
import tiebreaker

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

print("NAVAID and waypoints dictionaries combined")

#allows user to input waypoints to list
inputstring = input("Enter input string: ")
inputstring = inputstring.upper().split()

inputwaypoints = []

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
        print(item, "not found")
        exit()
    combinerlist = []
    combinerlist.append([item, typeelement, inp])
    inputwaypoints.append(combinerlist[0])

multiplefound = False #create multiplefound and fill it with False to start
    
#detection of multiples happens here
for waypoints in inputwaypoints:
    if len(waypoints[2]) == 1: #only one lat/long was found
        waypoints[2] = waypoints[2][0] #turn list of one lat/long into tuple
    else:
        multiplefound = True

if multiplefound == True:
    inputwaypoints = tiebreaker.tiebreaker(inputwaypoints) #pass inputwaypoints to tiebreaker
    
#takes inputted waypoints and turns them into a list of waypoint pairs
waypointpairs = pairmaker.pairmaker(inputwaypoints)

#takes waypoint pairs and uses vincenty() to find the total distance
sumdistance = 0.00 #establish sumdistance and put zero in it
    
for pairs in waypointpairs: #find distance of each waypointpair and sum together
    pairdistance = vincenty.vincenty(*pairs)
    sumdistance = sumdistance + pairdistance

print(sumdistance)