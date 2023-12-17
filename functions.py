import math
import objects


def pair_maker(input_waypoints):

    # below is so that the function will accept a list of elements as well
    if type(input_waypoints) is objects.Route:
        route = input_waypoints.get_waypoints()
    else:
        route = input_waypoints

    i = 0

    while i <= (len(route) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [route[i], route[i + 1]]
        i += 1
        yield pair


def distance_summer(input_tuples) -> float:
  
    sum_distance = 0.00  # establish sum_distance and put zero in it
  
    for pair in pair_maker(input_tuples):
        pair_distance = vincenty_indirect(pair)
        sum_distance += pair_distance

    return sum_distance


def list_parser(input_list, nav_library) -> objects.Route | None:

    output = objects.Route()

    for item in input_list:

        found_item = nav_library.nav_data_searcher(item)

        if found_item is None:  # nothing found by nav_data_searcher!
            print(item, "not found")
            # return from here - then wouldn't see if anything else was not found
            return None

        output.add_element(found_item)

    # if not_found_flag is True:  # maybe need to keep this flag to work with SIDs + STARs?
    #     output = 'invalidinput'

    # check for airway at beginning/end of route
    # if output.howmanyelements() > 1:
    #    if isinstance(output.getelement(0)[0], objects.Airway):  # we started with an airway, not OK!
    #        print("Route cannot begin with an airway - unable to compute.")
    #        output = 'invalidoutput'
    #    if isinstance(output.getelement(output.howmanyelements() - 1)[0], objects.Airway):
    #    we ended with an airway, not OK!
    #        print("Route cannot end with an airway - unable to compute.")
    #        output = 'invalidoutput'

    return output


def multiple_finder(input_waypoints: objects.Route):

    # finding ambiguous waypoint positions and grouping them together into a "matrix"

    found_multiples = [i for i, x in enumerate(input_waypoints.get_waypoints()) if type(x) is objects.AmbiguousPoint]

    multiples_matrix = []

    last_waypoint = -9  # have to fill it with something

    # this groups ambiguous elements together if they are sequential
    for waypoint in found_multiples:  # detect if elements are next to each other
        if waypoint == last_waypoint + 1:  # waypoint is sequential to waypoint before it
            multiples_matrix[len(multiples_matrix) - 1].append(waypoint)  # group with previous waypoint
        else:  # waypoint stands alone
            multiples_matrix.append([waypoint])
        last_waypoint = waypoint

    return multiples_matrix


def vincenty_indirect(pair, heading=False):

    #  Requires a tuple of two objects with the attribute .getcoordinates() which returns a
    #  tuple of type (-lat.00, lon.00)

    lat1 = float(pair[0].get_coordinates()[0])
    lon1 = float(pair[0].get_coordinates()[1])
    lat2 = float(pair[1].get_coordinates()[0])
    lon2 = float(pair[1].get_coordinates()[1])

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

    distanceinNM = s / 1852.0  # s is output in meters, converting to nautical miles ->
    # 1852 meters in a nautical mile (official and exact)

    distanceinNM = round(distanceinNM, 6)  # round to 1mm precision - Vincenty's formulae are only accurate to within
    # .5mm, which is 0.000000269 nm

    if heading is True:
        return distanceinNM, fwdAz, revAz
    else:
        return distanceinNM


def deambiguator_brute(inputwaypoints, multiplesmatrix):

    for multipleset in multiplesmatrix:

        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        possibilitieslist = []
        multiplesetelements = []
        
        if len(multipleset) == inputwaypoints.how_many_elements():
            allareambiguous = True
            firstisambiguous = True
            lastisambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif inputwaypoints.how_many_elements() - 1 in multipleset:
            lastisambiguous = True

        for listposition in multipleset:
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.get_element(listposition),
                                                         listposition, True))
                
        if allareambiguous is False and firstisambiguous is False:
            # add previous waypoint to beginning of multiplesetelements
            multiplesetelements.insert(0, objects.TBWrapper(inputwaypoints.get_element(multipleset[0] - 1),
                                                            multipleset[0] - 1))
            
        if allareambiguous is False and lastisambiguous is False:
            # add following waypoint to end of multiplesetelements 
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.get_element(multipleset[-1] + 1),
                                                         multipleset[-1] + 1))
            
        elementposition = 0

        for element in multiplesetelements:
            if elementposition == 0:  # first in the list, no copying needed here
                if element.was_ambiguous is False: # single element present
                    possibilitieslist.append([element])
                else:  # the element is ambiguous
                    ambiguousid = 0
                    for possibility in element.waypoint.get_possibilities():
                        possibilitieslist.append([objects.TBWrapper(possibility, element.get_original_position(), True,
                                                                    ambiguousid)])
                        ambiguousid += 1

            else:  # it's after first in the list

                if element.was_ambiguous is False:  # single element present
                    for item in possibilitieslist:
                        item.append(element)  # add to each list by one
                else:  # the element is ambiguous, complicated copy and append operation needed

                    returnedlist = []

                    for possibilityfromlist in possibilitieslist:
                        ambiguousid = 0
                        for possibilityfromelement in element.waypoint.get_possibilities():
                            returnedlist.append(possibilityfromlist + [objects.TBWrapper(possibilityfromelement,
                                                                                         element.get_original_position()
                                                                                         , True, ambiguousid)])
                            ambiguousid += 1

                    possibilitieslist = returnedlist

            elementposition += 1

        print('There are', len(possibilitieslist), 'possibilities to compute')

        leaderboard = []

        for possibility in possibilitieslist:  # compute distances
            leaderboard.append([distance_summer(possibility), possibility])

        shortestdistance = float('Inf')  # fill with worst-case scenario so anything else is smaller

        for competitor in leaderboard:  # establish which is shortest
            if competitor[0] < shortestdistance:
                shortestdistance = competitor[0]
                shortestcompetitor = competitor

        for point in shortestcompetitor[1]:  # deambiguate using shortestcompetitor
            if point.get_was_ambiguous() is True:
                inputwaypoints.deambiguate(point.get_original_position(), point.get_ambiguous_id())

    return inputwaypoints


def deambiguator_airway(input_waypoints):
    # use adjacent airways to solve ambiguous elements

    return input_waypoints
