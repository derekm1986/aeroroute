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
  
#allows user to input waypoints to list
    
inputwaypoints = []

while True:
    inp = raw_input("Enter waypoint: ")
    if inp == "done":
        break
    
    originalinput = inp
    
    if inp in airportsreader.airportdict:
        inp = airportsreader.airportdict[inp]
        typeelement = "airport"
    elif inp in pointsinspacedict:
        inp = pointsinspacedict[inp]
        typeelement = "point in space"
    else:
        print "waypoint not found"
        continue
    
    if len(inp) > 1:
        print "Multiple points were found with that name...need more programming.  Hard-coded to use first item."
        #do something for multiple hits here
        print inp
        inp = inp[0]
    else:
        inp = inp[0]

    combinerlist = []
        
    combinerlist.append((originalinput, typeelement, inp))
    
    inputwaypoints.append(combinerlist[0])

print inputwaypoints #for debug
    
    #takes inputted waypoints and turns them into a list of waypoint pairs

waypointpairs = pairmaker.pairmaker(inputwaypoints)

#takes waypoint pairs and uses vincenty() to find the total distance

sumdistance = 0.00 #establish sumdistance and put zero in it
    
for pairs in waypointpairs: #find distance of each waypointpair and sum together
    pairdistance = vincenty.vincenty(*pairs)
    sumdistance = sumdistance + pairdistance

print sumdistance