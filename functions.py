import math
import objects


def pointsinspacedictcombiner(navaiddict, waypointdict):

    pointsinspacedict = navaiddict.copy()

    for key, val in waypointdict.items():
        if key in pointsinspacedict:
            # the entry is already in pointsinspacedict
            if type(pointsinspacedict[key]) is objects.Ambiguouselement:
                # pointsinspacedict already has Ambiguouselement
                if type(val) is objects.Ambiguouselement:
                    # must add Ambiguouselement to Ambiguouselement
                    pointsinspacedict[key].addpossibility(waypointdict[key].getpossibilities())
                else:
                    # must add Pointinspace to Ambiguouselement
                    pointsinspacedict[key].addpossibility(waypointdict[key])
            else:
                # pointsinspacedict contains a Pointinspace
                if type(val) is objects.Ambiguouselement:
                    # Adding Ambigouselement to a Pointinspace, make a new Ambiguouselement
                    originalpointinspace = pointsinspacedict[key]
                    pointsinspacedict[key] = val
                    pointsinspacedict[key].addpossibility(originalpointinspace)
                else:
                    # Adding Pointinspace to a Pointinspace
                    pointsinspacedict[key] = objects.Ambiguouselement(key, pointsinspacedict[key])
                    pointsinspacedict[key].addpossibility(val)
        else:
            # the entry is not yet in pointsinspacedict, so just add it
            pointsinspacedict[key] = val

    return pointsinspacedict


def pairmaker(inputwaypoints):

    # below is so that the function will accept a list of elements as well
    if type(inputwaypoints) is objects.Route:
        route = inputwaypoints.getwaypoints()
    else:
        route = inputwaypoints

    i = 0

    while i <= (len(route) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [route[i], route[i + 1]]
        i += 1
        yield pair


def distancefinder(input):
  
    sumdistance = 0.00  # establish sumdistance and put zero in it
  
    for pair in pairmaker(input):
        pairdistance = vincentyindirect(pair)
        sumdistance += pairdistance

    return sumdistance


def stringreader(inputstring, airportdict, pointsinspacedict, airwaydict):

    output = objects.Route()

    manualwaypointnumber = 1

    notfoundflag = False

    previousitemname = None  # this is used below to detect a double input

    doubleinputflag = False

    for item in inputstring:

        if "/" in item:  # manual input detected
            itemname = 'WAYPOINT' + str(manualwaypointnumber)
            coordinates = tuple(item.split('/'))
            # assert that it's valid
            founditem = objects.Pointinspace(itemname, coordinates, 'manual waypoint')
            manualwaypointnumber += 1

        elif item in airportdict:
            itemname = item
            founditem = airportdict[item]

        elif item in airwaydict: # not finished, also should assert not at beginning or end of inputstring
            print(item + ' was found in airwaydict')

        # elif put something here to read SIDs/STARs

        elif item in pointsinspacedict:
            itemname = item
            founditem = pointsinspacedict[item]

        else:
            print(item, "not found")
            itemname = item  # needed for double input detection later
            notfoundflag = True

        if previousitemname == itemname and notfoundflag is False:  # double input detection
            print('Multiple adjacent input found with name', itemname, '- unable to compute.')
            doubleinputflag = True

        if notfoundflag is False:
            output.addelement(founditem)

        previousitemname = itemname  # for double input detection

    if notfoundflag is True:
        output = 'invalidinput'

    if doubleinputflag is True:
        output = 'invalidinput'

    return output


def multiplefinder(inputwaypoints):

    # finding ambiguous waypoint positions and grouping them together into a "matrix"

    foundmultiples = [i for i, x in enumerate(inputwaypoints.getwaypoints()) if type(x) is objects.Ambiguouselement]

    multiplesmatrix = []

    lastwaypoint = -9  # have to fill it with something

    # this groups ambiguous waypoints together if they are sequential
    for waypoint in foundmultiples:  # detect if waypoints are next to each other
        if waypoint == lastwaypoint + 1:  # waypoint is sequential to waypoint before it
            multiplesmatrix[len(multiplesmatrix) - 1].append(waypoint)  # group with previous waypoint
        else:  # waypoint stands alone
            multiplesmatrix.append([waypoint])
        lastwaypoint = waypoint

    return multiplesmatrix


def vincentyindirect(pair, heading=False):

    #  Requires a tuple of two objects with the attribute .getcoordinates() which returns a
    #  tuple of type (-lat.00, lon.00)

    lat1 = float(pair[0].getcoordinates()[0])
    lon1 = float(pair[0].getcoordinates()[1])
    lat2 = float(pair[1].getcoordinates()[0])
    lon2 = float(pair[1].getcoordinates()[1])

    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    # official WGS-84 ellipsoid parameters for output in meters
    a = 6378137.0
    b = 6356752.314245
    f = 1 / 298.257223563  
    
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1 - f) * math.tan(math.radians(lat1)))
    U2 = math.atan((1 - f) * math.tan(math.radians(lat2)))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    lmbda = L  # "lambda" is a reserved word in Python
    iterLimit = 100
    lmbdaP = 0.0  # jury-rig filling lmbdaP with something first

    while abs(lmbda - lmbdaP) > 1e-12 and iterLimit > 0:

        sinlmbda = math.sin(lmbda)
        coslmbda = math.cos(lmbda)
        sinSigma = math.sqrt(((cosU2 * sinlmbda) ** 2) + (((cosU1 * sinU2) - (sinU1 * cosU2 * coslmbda)) ** 2))
        cosSigma = (sinU1 * sinU2) + (cosU1 * cosU2 * coslmbda)
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = (cosU1 * cosU2 * sinlmbda) / sinSigma
        cosSqAlpha = 1 - (sinAlpha ** 2)  # this will equal zero if two points are along the equator

        if cosSqAlpha == 0:
            cos2SigmaM = 0  # to protect from division error due to cosSqAlpha=0, also C will equal zero below
        else:
            cos2SigmaM = cosSigma - ((2 * sinU1 * sinU2) / cosSqAlpha)

        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        lmbdaP = lmbda
        lmbda = L + (1 - C) * f * sinAlpha * (
                    sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM)))

        iterLimit -= 1

        if iterLimit == 0:
            print('formula failed to converge')
            return float("NaN")

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (
                cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM) - B / 6 * cos2SigmaM *
                                      (-3 + 4 * sinSigma * sinSigma) * (-3 + 4 * cos2SigmaM * cos2SigmaM)))
    s = b * A * (sigma - deltaSigma)

    # to return initial/final azimuths in addition to distance
    fwdAz = math.degrees(math.atan2(cosU2 * sinlmbda, cosU1 * sinU2 - sinU1 * cosU2 * coslmbda))
    revAz = math.degrees(math.atan2(cosU1 * sinlmbda, -sinU1 * cosU2 + cosU1 * sinU2 * coslmbda))

    # print('forwardazimuth: '+ str(fwdAz) + ',  ' + 'reverseazimuth: '+ str(revAz))

    distanceinNM = s / 1852.0  # s is output in meters, converting to nautical miles ->
    # 1852 meters in a nautical mile (official and exact)

    distanceinNM = round(distanceinNM, 6)  # round to 1mm precision - Vincenty's formulae are only accurate to within
    # .5mm, which is 0.000000269 nm

    if heading is True:
        return (distanceinNM, fwdAz, revAz)
    else:
        return distanceinNM


def deambiguator(inputwaypoints, multiplesmatrix):

    for multipleset in multiplesmatrix:

        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        possibilitieslist = []
        multiplesetelements = []
        
        if len(multipleset) == inputwaypoints.howmanyelements():
            allareambiguous = True
            firstisambiguous = True
            lastisambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif inputwaypoints.howmanyelements() - 1 in multipleset:
            lastisambiguous = True

        for listposition in multipleset:
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(listposition), 
                                       listposition, True))
                
        if allareambiguous is False and firstisambiguous is False:
            # add previous waypoint to beginning of multiplesetelements
            multiplesetelements.insert(0, objects.TBWrapper(inputwaypoints.getelement(multipleset[0] - 1),
                                       multipleset[0] - 1))
            
        if allareambiguous is False and lastisambiguous is False:
            # add following waypoint to end of multiplesetelements 
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(multipleset[-1] + 1),
                                       multipleset[-1] + 1))
            
        elementposition = 0

        for element in multiplesetelements:
            if elementposition == 0: # first in the list, no copying needed here
                if element.wasambiguous is False: # single element present
                    possibilitieslist.append([element])
                else: # the element is ambiguous
                    ambiguousid = 0
                    for possibility in element.waypoint.getpossibilities():
                        possibilitieslist.append([objects.TBWrapper(possibility, element.getoriginalposition(), True,
                                                                   ambiguousid)])
                        ambiguousid += 1

            else:  # it's after first in the list

                if element.wasambiguous is False: # single element present
                    for item in possibilitieslist:
                        item.append(element) # add to each list by one
                else:  # the element is ambiguous, complicated copy and append operation needed

                    returnedlist = []

                    for possibilityfromlist in possibilitieslist:
                        ambiguousid = 0
                        for possibilityfromelement in element.waypoint.getpossibilities():
                            returnedlist.append(possibilityfromlist + [objects.TBWrapper(possibilityfromelement,
                                                                element.getoriginalposition(), True, ambiguousid)])
                            ambiguousid += 1

                    possibilitieslist = returnedlist

            elementposition += 1

        print('There are', len(possibilitieslist), 'possibilities to compute')

        leaderboard = []

        for possibility in possibilitieslist:  # compute distances
            leaderboard.append([distancefinder(possibility), possibility])

        shortestdistance = float('Inf')  # fill with worst-case scenario so anything else is smaller

        for competitor in leaderboard:  # establish which is shortest
            if competitor[0] < shortestdistance:
                shortestdistance = competitor[0]
                shortestcompetitor = competitor

        for point in shortestcompetitor[1]:  # deambiguate using shortestcompetitor
            if point.getwasambiguous() is True:
                inputwaypoints.deambiguate(point.getoriginalposition(), point.getambiguousid())

    return inputwaypoints
