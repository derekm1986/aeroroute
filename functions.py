import math
import objects
import logging


def pair_maker(input_waypoints):
    """
    generator function that makes pairs of Coordinates
    :param input_waypoints: Route or a list of elements
    :return: tuple of two Coordinates objects
    """
    # below is so that the function will accept a list of elements as well
    if type(input_waypoints) is objects.Route:
        route = input_waypoints.elements
    else:
        route = input_waypoints

    for item in route:
        if isinstance(item, (objects.Airway, objects.AmbiguousAirway)):
            print("an airway got too far, we will crash!")
            return

    i = 0

    while i <= (len(route) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [route[i].coordinates, route[i + 1].coordinates]
        i += 1
        yield pair


def distance_summer(input_coordinates) -> float:
    """
    calculates the sum of distances between a list of coordinates
    :param input_coordinates: list of Coordinates objects
    :return: sum of distances in nautical miles
    """
  
    sum_distance = 0.00  # establish sum_distance and put zero in it
  
    for pair in pair_maker(input_coordinates):
        pair_distance = vincenty_indirect(pair)
        sum_distance += pair_distance

    return sum_distance


def list_parser(input_list, nav_library) -> objects.Route | None:
    """
    parses a list of strings into a Route object
    :param input_list: list of strings
    :param nav_library: NavDataLibrary object
    :return: Route object
    """

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


def multiple_point_finder(input_waypoints: objects.Route):
    """
    helper function for deambiguator_brute
    :param input_waypoints: Route object
    :return: list of lists of integers representing positions of multiple points in the route   
    """
    # finding ambiguous waypoint positions and grouping them together into a "matrix"

    found_multiples = [i for i, x in enumerate(input_waypoints.elements) if type(x) is objects.AmbiguousPoint]

    multiples_map = []

    last_waypoint = -9  # have to fill it with something

    # this groups ambiguous elements together if they are sequential
    for waypoint in found_multiples:  # detect if elements are next to each other
        if waypoint == last_waypoint + 1:  # waypoint is sequential to waypoint before it
            multiples_map[len(multiples_map) - 1].append(waypoint)  # group with previous waypoint
        else:  # waypoint stands alone
            multiples_map.append([waypoint])
        last_waypoint = waypoint

    return multiples_map


def vincenty_indirect(pair, heading=False):
    """
    calculates distance between two coordinates using Vincenty's indirect formula
    :param pair: tuple of two Coordinates objects
    :param heading: boolean, if True, returns distance and headings
    :return: distance in nautical miles
    """
    #  Requires a tuple of two Coordinates objects
    #  tuple of type (-lat.00, lon.00)

    lat1 = float(pair[0].latitude)
    lon1 = float(pair[0].longitude)
    lat2 = float(pair[1].latitude)
    lon2 = float(pair[1].longitude)

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
            logging.warning("Vincenty formula failed to converge")
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


def deambiguator_brute(input_route, multiplesmatrix):
    """
    deambiguates points in a route using a brute force method, if an airway in a route, will not work correctly
    :param input_route: Route object
    :param multiplesmatrix: list of lists of integers representing positions of multiple points in the route
    :return: Route object with points deambiguated
    """
    for multipleset in multiplesmatrix:

        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        possibilitieslist = []
        multiplesetelements = []
        
        if len(multipleset) == input_route.num_elements:
            allareambiguous = True
            firstisambiguous = True
            lastisambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif input_route.num_elements - 1 in multipleset:
            lastisambiguous = True

        for listposition in multipleset:
            multiplesetelements.append(objects.TBWrapper(input_route.get_element(listposition),
                                                         listposition, True))
                
        if allareambiguous is False and firstisambiguous is False:
            # add previous waypoint to beginning of multiplesetelements
            multiplesetelements.insert(0, objects.TBWrapper(input_route.get_element(multipleset[0] - 1),
                                                            multipleset[0] - 1))
            
        if allareambiguous is False and lastisambiguous is False:
            # add following waypoint to end of multiplesetelements 
            multiplesetelements.append(objects.TBWrapper(input_route.get_element(multipleset[-1] + 1),
                                                         multipleset[-1] + 1))
            
        elementposition = 0

        print(multiplesetelements) # for testing

        for element in multiplesetelements:
            if elementposition == 0:  # first in the list, no copying needed here
                if element.was_ambiguous is False: # single element present
                    possibilitieslist.append([element])
                else:  # the element is ambiguous
                    ambiguousid = 0
                    for possibility in element.waypoint.possibilities:
                        possibilitieslist.append([objects.TBWrapper(possibility, element.original_position, True,
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
                        for possibilityfromelement in element.waypoint.possibilities:
                            returnedlist.append(possibilityfromlist + [objects.TBWrapper(possibilityfromelement,
                                                                                         element.original_position
                                                                                         , True, ambiguousid)])
                            ambiguousid += 1

                    possibilitieslist = returnedlist

            elementposition += 1

        logging.info("There are " + str(len(possibilitieslist)) + " possibilities to compute.")

        leaderboard = []

        for possibility in possibilitieslist:  # compute distances
            leaderboard.append([distance_summer(possibility), possibility])

        shortestdistance = float('Inf')  # fill with worst-case scenario so anything else is smaller

        for competitor in leaderboard:  # establish which is shortest
            if competitor[0] < shortestdistance:
                shortestdistance = competitor[0]
                shortestcompetitor = competitor

        for point in shortestcompetitor[1]:  # deambiguate using shortestcompetitor
            if point.was_ambiguous is True:
                input_route.deambiguate(point.original_position, point.ambiguous_id)

    return input_route


def deambiguate_points_using_airways(input_route):
    # work in progress
    # use adjacent airways to solve ambiguous elements
    for item in input_route.elements:
        if isinstance(item, objects.AmbiguousPoint):
            if input_route.elements.index(item) == 0:  # starts with AmbiguousPoint
                if isinstance(input_route.elements[1], (objects.Airway, objects.AmbiguousAirway)):
                    # first element was ambiguous and was followed by an airway
                    for waypoint in item.possibilities:
                        for airway in waypoint.available_airways:
                            if airway == input_route.elements[1].identifier:
                                input_route.deambiguate(0, item.possibilities.index(waypoint))
            elif input_route.elements.index(item) == (len(input_route.elements)-1):
                if isinstance(input_route.elements[-2], (objects.Airway, objects.AmbiguousAirway)):
                    # last element was ambiguous and was preceded by an airway!
                    for waypoint in item.possibilities:
                        for airway in waypoint.available_airways:
                            if airway == input_route.elements[-2].identifier:
                                input_route.deambiguate(input_route.num_elements-1, item.possibilities.index(waypoint))
            else:
                print("ambiguous point is in the middle of the route!")
                current_index = input_route.elements.index(item)
                previous_index = input_route.elements.index(item) - 1
                next_index = input_route.elements.index(item) + 1


    return input_route
