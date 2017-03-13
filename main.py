import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker
import tiebreaker

print('\n***Program starting***','\n')

print('Reading AIRAC data...')

print('   Loading airports into memory...', end="")
airportsreader.airportdictmaker()
print('OK') #loading airports was successful

print('   Loading NAVAIDs into memory...', end="")
navaidsreader.navaiddictmaker()
print('OK') #loading NAVAIDs was successful

print('   Loading waypoints into memory...', end="")
waypointsreader.waypointdictmaker()
print('OK') #loading waypoints was successful

#combining navaiddict and waypointdict dictionaries into one

print('   Combining NAVAID and waypoints dictionaries...', end="")

pointsinspacedict = navaidsreader.navaiddict.copy()

for key, val in waypointsreader.waypointdict.items():
    if key in pointsinspacedict:
        pointsinspacedict[key] += val
    else:
        pointsinspacedict[key] = val
print("OK") #dictionary combination was successful

while True:

    print('\n')
    
    #allows user to input waypoint(s)/exit instructions to list
    print('Type "quit" to exit program')
    inputstring = input("Enter input string: ")
    inputstring = inputstring.upper().split()

    if len(inputstring) == 0:
        print("No input detected")
        continue
        
    if "QUIT" in inputstring:
        print('***Program exiting***')
        break
    
    inputwaypoints = []

    for item in inputstring:
    
        inp = item
        elementfound = False
        
        if inp in airportsreader.airportdict:
            inp = airportsreader.airportdict[inp]
            typeelement = "airport"
            elementfound = True
    
        #elif put something here to read airways
            #typeelement = "airway"
        
        #elif put something here to read SIDs/STARs
        
        elif inp in pointsinspacedict:
            inp = pointsinspacedict[inp]
            typeelement = "point in space"
            elementfound = True
    
        else:                                
            print(item, "not found")
        
        if elementfound == True:
            combinerlist = []
            combinerlist.append([item, typeelement, inp])
            inputwaypoints.append(combinerlist[0])

    if elementfound == False:
        continue
            
    if len(inputwaypoints) == 1:
        print('Single item detected, printing entry:',inputwaypoints[0])
        continue
    
    #detection of multiples happens here
    for waypoints in inputwaypoints:
        if len(waypoints[2]) > 1: #only one lat/long possibility was found
            inputwaypoints = tiebreaker.tiebreaker(inputwaypoints) #pass inputwaypoints to tiebreaker because a multiple was found    

    for waypoints in inputwaypoints:
        waypoints[2] = waypoints[2][0] #turn list of one lat/long into tuple
    
    #takes inputted waypoints and turns them into a list of waypoint pairs
    waypointpairs = pairmaker.pairmaker(inputwaypoints)

    #takes waypoint pairs and uses vincenty() to find the total distance
    sumdistance = 0.00 #establish sumdistance and put zero in it
    
    print(waypointpairs)
    
    for pairs in waypointpairs: #find distance of each waypointpair and sum together
        pairdistance = vincenty.vincenty(*pairs)
        sumdistance = sumdistance + pairdistance

    print('Distance in nm:',sumdistance)