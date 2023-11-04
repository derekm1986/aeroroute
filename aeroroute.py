"""
A program I use to get the length of routes typed in human-readable
format.  Requires AIRAC files in vasFMC format in a /AIRAC/ folder.
"""
import airportsreader
import waypointsreader
import navaidsreader
import atsreader
import functions
import airwaymatcher


def main():
    """
    The main method of the program
    :return: nothing
    """

    print('\n***Aeroroute loading***', '\n')

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

    print('   Loading airways into memory...', end="")
    airwaydict = atsreader.airwaydictmaker()
    print('OK')  # loading airways was successful

    print('\nCombining NAVAID and waypoints dictionaries...', end="")
    pointsinspacedict = functions.pointsinspacedictcombiner(navaiddict, waypointdict)
    print("OK")  # dictionary combination was successful

    print('Adding airway references to combined dictionary...', end="")
    pointsinspacedict = airwaymatcher.airwaymatcher(pointsinspacedict, airwaydict)
    print("OK")  # reference matching was successful

    while True:

        # allows user to input waypoint(s)/exit instructions to list
        print('\nType "quit" to exit program, enter 20.000000/-123.000000 format for manual waypoints')
        inputstring = input("Enter input string: ")
        inputstring = inputstring.upper().split()

        if len(inputstring) == 0:
            print("No input detected")
            continue

        doubleinputflag = False  # double adjacent input detection

        if len(inputstring) > 1:
            for i in range(len(inputstring) - 1):
                if inputstring[i] == inputstring[i + 1]:
                    print('Multiple adjacent input found with name', inputstring[i], '- unable to compute.')
                    doubleinputflag = True
                    break

        if doubleinputflag:
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

        if inputwaypointsobj.getcontainsairway():  # is there an airway in the route?
            # is airway at beginning of route? - not OK
            if isinstance(inputwaypointsobj.getelement(0), list):
                print("Route cannot start with an airway")
                continue

            # is airway at end of route? - not OK
            if isinstance(inputwaypointsobj.getelement(inputwaypointsobj.howmanyelements() - 1), list):
                print("Route cannot end with an airway")
                continue

            # no airways should touch another airway

            # can any ambiguous elements be solved by matching with an adjacent airway?


            # if there is an airway in inputwaypointsobj, call a function that incorporates the airway into the route

        if inputwaypointsobj.getcontainsambiguity():  # do we contain an ambiguouselement?

            multiplesmatrix = functions.multiplefinder(inputwaypointsobj)

            inputwaypointsobj = functions.deambiguatorbrute(inputwaypointsobj, multiplesmatrix)

        for item in inputwaypointsobj.getwaypoints():
            print(item)

        sumdistance = functions.distancefinder(inputwaypointsobj)

        print('Distance in nm:', sumdistance)


if __name__ == "__main__":
    main()
