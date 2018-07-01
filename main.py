import airportsreader
import waypointsreader
import navaidsreader
import tiebreaker
import functions
from objects import Ambiguouselement

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

functions.pointsinspacedictcombiner()

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

    inputwaypointsobj = functions.stringreader(inputstring)

    if inputwaypointsobj == "invalidinput":  # something bad came back from stringreader
        continue

    if len(inputwaypointsobj.getwaypoints()) == 1:
        print('Single item detected, printing entry:', inputwaypointsobj[0])
        continue

    for thing in inputwaypointsobj.getwaypoints():
        print(thing)

    multiplesmatrix = functions.multiplefinder(inputwaypointsobj)

    if len(multiplesmatrix) > 0:
        inputwaypointsobj = tiebreaker.testtiebreaker(inputwaypointsobj, multiplesmatrix)

#    for element in inputwaypointsobj:
#        if type(element) is Ambiguouselement:  # more than one lat/long possibility was found
#            inputwaypointsobj = tiebreaker.tiebreaker(inputwaypointsobj)  # an ambiguous element was found
#            break  # otherwise this could trigger multiple times

    # an ambiguouselement made it too far, code below forces it to the first possibility ------------

    elementplace = 0

    for element in inputwaypointsobj.getwaypoints():
        if type(element) is Ambiguouselement:
            inputwaypointsobj.getwaypoints()[elementplace] = element.getpossibilities()[0]
            elementplace += 1
        else:
            elementplace += 1

    # -----------------------------------------------------------------------------------------------

    sumdistance = functions.distancefinder(inputwaypointsobj)

    print('Distance in nm:', sumdistance)
