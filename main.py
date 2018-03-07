import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker
import tiebreaker
from objects import Ambiguouselement

# make __iter__ for ambiguouselement class

print('\n***Program loading***', '\n')

print('Reading AIRAC data...')

print('   Loading airports into memory...', end="")
airportsreader.airportdictmaker()
print('OK')  # loading airports was successful

print('   Loading NAVAIDs into memory...', end="")
navaidsreader.navaiddictmaker()
print('OK')  # loading NAVAIDs was successful

print('   Loading waypoints into memory...', end="")
waypointsreader.waypointdictmaker()
print('OK')  # loading waypoints was successful

# combining navaiddict and waypointdict dictionaries into one

print('   Combining NAVAID and waypoints dictionaries...', end="")

pointsinspacedict = navaidsreader.navaiddict.copy()

for key, val in waypointsreader.waypointdict.items():
    if key in pointsinspacedict:
        pointsinspacedict[key] += val
    else:
        pointsinspacedict[key] = val
print("OK")  # dictionary combination was successful

######for object testing below

pointsinspacedictobj = navaidsreader.navaiddictobj.copy()

for key, val in waypointsreader.waypointdictobj.items():
    if key in pointsinspacedictobj:
        #the entry is already in pointsinspacedictobj
        if type(pointsinspacedictobj[key]) is Ambiguouselement:
            #pointsinspacedictobj already has Ambiguouselement
            if type(val) is Ambiguouselement:
                #must add Ambiguouselement to Ambiguouselement
                pointsinspacedictobj[key].addpossibility(waypointsreader.waypointdictobj[key].getpossibilities)
            else:
                #must add Pointinspace to Ambiguouselement
                pointsinspacedictobj[key].addpossibility(waypointsreader.waypointdictobj[key])
        else:
            #pointsinspacedictobj contains a Pointinspace
            if type(val) is Ambiguouselement:
                #Adding Ambigouselement to a Pointinspace, make a new Ambiguouselement
                originalpointinspace = pointsinspacedictobj[key]
                pointsinspacedictobj[key] = val
                pointsinspacedictobj[key].addpossibility(originalpointinspace)
            else:
                #Adding Pointinspace to a Pointinspace
                pointsinspacedictobj[key] = Ambiguouselement(key, pointsinspacedictobj[key])
                pointsinspacedictobj[key].addpossibility(val)
    else:
        #the entry is not yet in pointsinspacedictobj, so just add it
        pointsinspacedictobj[key] = val

#######for testing below

#print(navaidsreader.navaiddictobj)

item = airportsreader.airportdictobj['KBOS']
print(item.getidentifier(),item.getcoordinates(),item.gettypeelement(), item.getelementname())

#posstest = testobj.getpossibilities()

#for element in posstest:
#        print(element.getidentifier(), element.getcoordinates())


#print(type(testobjcoord))
#print(len(testobjcoord))
#for possibility in testobjcoord:
#        print(possibility.getcoordinates())
#print(testobjcoord)

#print(navaidsreader.navaiddict['CAM'])

###########################


while True:

    print('\n')
    
    # allows user to input waypoint(s)/exit instructions to list
    print('Type "quit" to exit program, enter 20.000000/-123.000000 format for manual LAT/LONG')
    inputstring = input("Enter input string: ")
    inputstring = inputstring.upper().split()

    if len(inputstring) == 0:
        print("No input detected")
        continue
        
    if "QUIT" in inputstring:
        print('***Program exiting***')
        break
    
    inputwaypoints = []

    manualwaypointnumber = 1
    
    notfoundflag = False
    
    previousitemname = None  # this is used below to detect a double input
    
    doubleinputflag = False
    
    for item in inputstring:
        
        if "/" in item:  # manual input detected
            itemname = 'WAYPOINT'+str(manualwaypointnumber)
            coordinates = [tuple(item.split('/'))]
            # assert that it's valid
            typeelement = "manual waypoint"
            manualwaypointnumber += 1
        
        elif item in airportsreader.airportdict:
            itemname = item
            coordinates = airportsreader.airportdict[item]
            typeelement = "airport"
    
        # elif put something here to read airways
            # typeelement = "airway"
        
        # elif put something here to read SIDs/STARs
        
        elif item in pointsinspacedict:
            itemname = item
            coordinates = pointsinspacedict[item]
            typeelement = "point in space"
    
        else:                                
            print(item, "not found")
            itemname = item # needed for double input detection later
            notfoundflag = True
      
        if previousitemname == itemname and notfoundflag is False:  # double input detection
            print('Multiple adjacent input found with name', itemname, '- unable to compute.')
            doubleinputflag = True
            
        if notfoundflag is False:
            combinerlist = []
            combinerlist.append([itemname, typeelement, coordinates])
            inputwaypoints.append(combinerlist[0])
        
        previousitemname = itemname  # for double input detection
            
    if notfoundflag is True:
        continue
        
    if doubleinputflag is True:
        continue
            
    if len(inputwaypoints) == 1:
        print('Single item detected, printing entry:', inputwaypoints[0])
        continue
    
    # detection of ambiguous elements happens here
    for waypoints in inputwaypoints:
        if len(waypoints[2]) > 1:  # more than one lat/long possibility was found
            inputwaypoints = tiebreaker.tiebreaker(inputwaypoints)  # pass inputwaypoints to tiebreaker because...
            #  an ambiguous element was found
            break  # otherwise this could trigger multiple times

    for waypoints in inputwaypoints:
        waypoints[2] = waypoints[2][0]  # turn list of one lat/long into tuple
    
    # takes inputted waypoints and turns them into a list of waypoint pairs
    waypointpairs = pairmaker.pairmaker(inputwaypoints)

    # takes waypoint pairs and uses vincenty() to find the total distance
    sumdistance = 0.00  # establish sumdistance and put zero in it
    
    for pairs in waypointpairs:  # find distance of each waypointpair and sum together
        pairdistance = vincenty.vincenty(*pairs)
        sumdistance += pairdistance

    print('Distance in nm:', sumdistance)