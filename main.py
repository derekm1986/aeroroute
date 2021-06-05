import airportsreader
import waypointsreader
import navaidsreader
import atsreader
import functions


print('\n***Program loading***', '\n')

print('Reading AIRAC data...')

print('   Loading airports into memory...', end="")
airportdict = airportsreader.airportdictmaker()
print('OK')  # loading airports was successful

print('   Loading NAVAIDs into memory...', end="")
navaiddict = navaidsreader.navaiddictmaker()
print('OK')  # loading NAVAIDs was successful

print('   Loading waypoints into memory...', end="")
waypointdict = waypointsreader.waypointdictmaker()
print('OK')  # loading waypoints was successful

print('   Combining NAVAID and waypoints dictionaries...', end="")
pointsinspacedict = functions.pointsinspacedictcombiner(navaiddict, waypointdict)
print("OK")  # dictionary combination was successful

airwaydict = atsreader.airwaydictmaker()

while True:

    print('\n')
    
    # allows user to input waypoint(s)/exit instructions to list
    print('Type "quit" to exit program, enter 20.000000/-123.000000 format for manual waypoints')
    inputstring = input("Enter input string: ")
    inputstring = inputstring.upper().split()

    if len(inputstring) == 0:
        print("No input detected")
        continue
        
    if "QUIT" in inputstring:
        print('***Program exiting***')
        break

    inputwaypointsobj = functions.stringreader(inputstring, airportdict, pointsinspacedict, airwaydict)

    if inputwaypointsobj == "invalidinput":  # something bad came back from stringreader
        continue

    if len(inputwaypointsobj.getwaypoints()) == 1:
        print('Single item detected, printing entry:', inputwaypointsobj.getelement(0))
        continue

    # if there is an airway in inputwaypointsobj, call a function that incorporates the airway into the route
        
    multiplesmatrix = functions.multiplefinder(inputwaypointsobj)

    if len(multiplesmatrix) > 0:
        inputwaypointsobj = functions.deambiguator(inputwaypointsobj, multiplesmatrix)

    for item in inputwaypointsobj.getwaypoints():
        print(item)

    sumdistance = functions.distancefinder(inputwaypointsobj)

    print('Distance in nm:', sumdistance)
