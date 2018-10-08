import airportsreader
import waypointsreader
import navaidsreader
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
        inputwaypointsobj = functions.deambiguator(inputwaypointsobj, multiplesmatrix)

    sumdistance = functions.distancefinder(inputwaypointsobj)

    print('Distance in nm:', sumdistance)
