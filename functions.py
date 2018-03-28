import vincenty
import airportsreader
import navaidsreader
import waypointsreader
from objects import *


def pointsinspacedictcombiner():

    global pointsinspacedictobj

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


def pairmaker(inputwaypoints):

    i = 0

    while i <= (len(inputwaypoints) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [inputwaypoints[i], inputwaypoints[i + 1]]
        i += 1
        yield pair


def distancefinder(input):
  
    sumdistance = 0.00  # establish sumdistance and put zero in it
  
    for pair in pairmaker(input):
        pairdistance = vincenty.vincenty(*pair)
        sumdistance += pairdistance

    return sumdistance


def stringreader(inputstring):

    output = []

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
            output.append(founditem)

        previousitemname = itemname  # for double input detection

    if notfoundflag is True:
        output = 'invalidinput'

    if doubleinputflag is True:
        output = 'invalidinput'

    return output

def multiplefinder(inputwaypoints):

    # finding ambiguous waypoint positions

    foundmultiples = [i for i, x in enumerate(inputwaypoints) if type(x) is Ambiguouselement]

    multiplesmatrix = []

    lastwaypoint = -9  # have to fill it with something

    # this groups ambiguous waypoints together if they are sequential
    for waypoint in foundmultiples:  # detect if waypoints are next to each other
        if waypoint == lastwaypoint + 1:  # waypoint is sequential to waypoint before it
            multiplesmatrix[len(multiplesmatrix) - 1].append(waypoint)  # group with previous
        else:  # waypoint stands alone
            multiplesmatrix.append([waypoint])
        lastwaypoint = waypoint

    return multiplesmatrix

#def testtiebreaker(inputroute):


