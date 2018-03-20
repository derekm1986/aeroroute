import vincenty
import airportsreader


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

    return inputwaypointsobj
