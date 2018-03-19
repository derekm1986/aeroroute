import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker
import tiebreaker
from objects import Ambiguouselement, Pointinspace


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

pointsinspacedictobj = navaidsreader.navaiddictobj.copy()

for key, val in waypointsreader.waypointdictobj.items():
    if key in pointsinspacedictobj:
        # the entry is already in pointsinspacedictobj
        if type(pointsinspacedictobj[key]) is Ambiguouselement:
            # pointsinspacedictobj already has Ambiguouselement
            if type(val) is Ambiguouselement:
                # must add Ambiguouselement to Ambiguouselement
                pointsinspacedictobj[key].addpossibility(waypointsreader.waypointdictobj[key].getpossibilities())
            else:
                # must add Pointinspace to Ambiguouselement
                pointsinspacedictobj[key].addpossibility(waypointsreader.waypointdictobj[key])
        else:
            # pointsinspacedictobj contains a Pointinspace
            if type(val) is Ambiguouselement:
                # Adding Ambigouselement to a Pointinspace, make a new Ambiguouselement
                originalpointinspace = pointsinspacedictobj[key]
                pointsinspacedictobj[key] = val
                pointsinspacedictobj[key].addpossibility(originalpointinspace)
            else:
                # Adding Pointinspace to a Pointinspace
                pointsinspacedictobj[key] = Ambiguouselement(key, pointsinspacedictobj[key])
                pointsinspacedictobj[key].addpossibility(val)
    else:
        # the entry is not yet in pointsinspacedictobj, so just add it
        pointsinspacedictobj[key] = val

print("OK")  # dictionary combination was successful

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

    inputwaypointsobj = []

    manualwaypointnumber = 1

    notfoundflag = False

    previousitemname = None  # this is used below to detect a double input

    doubleinputflag = False

    for item in inputstring:

        if "/" in item:  # manual input detected
            itemname = 'WAYPOINT' + str(manualwaypointnumber)
            coordinates = [tuple(item.split('/'))]
            # assert that it's valid
            founditem = Pointinspace(itemname, coordinates, 'manual waypoint')
            manualwaypointnumber += 1

        elif item in airportsreader.airportdictobj:
            itemname = item
            founditem = airportsreader.airportdictobj[item]

        # elif put something here to read airways

        # elif put something here to read SIDs/STARs

        elif item in pointsinspacedictobj:
            itemname = item
            founditem = pointsinspacedictobj[item]

        else:
            print(item, "not found")
            itemname = item  # needed for double input detection later
            notfoundflag = True

        if previousitemname == itemname and notfoundflag is False:  # double input detection
            print('Multiple adjacent input found with name', itemname, '- unable to compute.')
            doubleinputflag = True

        if notfoundflag is False:
            inputwaypointsobj.append(founditem)

        previousitemname = itemname  # for double input detection

    if notfoundflag is True:
        continue

    if doubleinputflag is True:
        continue

    if len(inputwaypointsobj) == 1:
        print('Single item detected, printing entry:', inputwaypointsobj[0])
        continue

    print(inputwaypointsobj)

    for element in inputwaypointsobj:
        if type(element) is Ambiguouselement:  # more than one lat/long possibility was found
            inputwaypointsobj = tiebreaker.tiebreaker(inputwaypointsobj)  # pass inputwaypoints to tiebreaker because...
            print('an ambiguouselement was found')
            #  an ambiguous element was found
            break  # otherwise this could trigger multiple times

    elementplace = 0

    for element in inputwaypointsobj:
        if type(element) is Ambiguouselement:
            inputwaypointsobj[elementplace] = element.getpossibilities()[0]
            elementplace += 1
        else:
            elementplace += 1

    print(inputwaypointsobj)

    #waypointgen = pairmaker.pairmaker(inputwaypointsobj)

    waypointpairs = []

    for pair in pairmaker.pairmaker(inputwaypointsobj):
        waypointpairs.append(pair)
        print(pair)

    print('waypointpairs is ',waypointpairs)

    # takes waypoint pairs and uses vincenty() to find the total distance
    sumdistance = 0.00  # establish sumdistance and put zero in it
    
    for pairs in waypointpairs:  # find distance of each waypointpair and sum together
        pairdistance = vincenty.vincenty(*pairs)
        sumdistance += pairdistance

    print('Distance in nm:', sumdistance)
