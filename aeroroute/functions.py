import objects
import logging
import re
#from vincenty import vincenty_indirect

#from aeroroute import objects
#from aeroroute.vincenty import vincenty_indirect
import vincenty


def pair_maker(input_waypoints):
    """
    generator function that makes pairs of Coordinates
    :param input_waypoints: Route or a list of elements
    :return: tuple of two Coordinates objects
    """
    
    # below is so that the function will accept a list of elements as well
    if type(input_waypoints) is objects.Route:
        route_before_airways = input_waypoints.elements
    else:
        route_before_airways = input_waypoints

    route = []
    
    # looking for airways
    for item in route_before_airways:
        if isinstance(item, objects.AirwayInRoute):
            for waypoint in item.waypoints:
                route.append(waypoint)
        elif isinstance(item, objects.TerminalProcedure):
            pass
        else:
            route.append(item)

    pairs = []
    
    i = 0

    while i <= (len(route) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [route[i].coordinates, route[i + 1].coordinates]
        i += 1
        pairs.append(pair)
    
    return pairs


def distance_summer(input_coordinates) -> float:
    """
    calculates the sum of distances between a list of coordinates
    :param input_coordinates: list of Coordinates objects
    :return: sum of distances in nautical miles
    """

    sum_distance = 0.00  # establish sum_distance and put zero in it
  
    for pair in pair_maker(input_coordinates):
        pair_distance = vincenty.vincenty_indirect(pair)
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

        if "/" in item:  # manual input detected
            found_item = manual_waypoint_maker(item)
        
        else:
            found_item = nav_library.nav_data_searcher(item)

        if found_item is None:  # nothing found by nav_data_searcher!
            found_item = item

        output.add_element(found_item)

    # is there a None in the route?  Could this be a SID or STAR?
    for item in output.elements:
         if isinstance(item, str):
            try:
                previous_item = output.elements[output.elements.index(item) - 1]
            except:
                previous_item = None
            try:
                next_item = output.elements[output.elements.index(item) + 1]
            except:
                next_item = None

            if isinstance(previous_item, objects.Airport) and isinstance(next_item, (objects.PointInSpace, 
                                                                                     objects.AmbiguousPoint)):
                if terminal_procedure_recognizer(item):
                    output.replace_element(output.elements.index(item), 
                                           objects.TerminalProcedure(item, "SID", previous_item.identifier))
    
            elif isinstance(next_item, objects.Airport) and isinstance(previous_item, (objects.PointInSpace, 
                                                                                       objects.AmbiguousPoint)):
                if terminal_procedure_recognizer(item):
                    output.replace_element(output.elements.index(item), 
                                           objects.TerminalProcedure(item, "STAR", next_item.identifier))

    # still a string in the route? then return None
    failure_flag = False

    # re-write to look for valid objects instead
    for item in output.elements:
        if isinstance(item, str):
            print(item, "not found")
            failure_flag = True

    if failure_flag:
        return None

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


def deambiguator_brute(input_route, multiplesmatrix) -> objects.Route:
    """
    deambiguates points in a route using a brute force method
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
            previous_element = input_route.get_element(multipleset[0] - 1)
            # need to check that it is not an airway or procedure!!!!
            if not isinstance(previous_element, (objects.Airway, objects.AmbiguousAirway, 
                                                 objects.AirwayInRoute, objects.TerminalProcedure)):

                multiplesetelements.insert(0, objects.TBWrapper(previous_element, multipleset[0] - 1))      
        
        if allareambiguous is False and lastisambiguous is False:
            # add next waypoint to end of multiplesetelements 
            next_element = input_route.get_element(multipleset[-1] + 1)
            # need to check that it is not an airway or procedure!!!!
            if not isinstance(next_element, (objects.Airway, objects.AmbiguousAirway, 
                                             objects.AirwayInRoute, objects.TerminalProcedure)):

                multiplesetelements.append(objects.TBWrapper(next_element, multipleset[-1] + 1))
        
        elementposition = 0

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


def deambiguate_points_using_airways(input_route) -> objects.Route:
    """
    use adjacent airways to solve ambiguous points
    :param input_route: Route object
    :return: Route object with points deambiguated using airways
    """
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
                current_index = input_route.elements.index(item)
                previous_index = input_route.elements.index(item) - 1
                next_index = input_route.elements.index(item) + 1
                if isinstance(input_route.elements[previous_index], (objects.Airway, objects.AmbiguousAirway)):
                    # previous element was ambiguous and was followed by an airway
                    for waypoint in item.possibilities:
                        for airway in waypoint.available_airways:
                            if airway == input_route.elements[previous_index].identifier:
                                input_route.deambiguate(current_index, item.possibilities.index(waypoint))
                elif isinstance(input_route.elements[next_index], (objects.Airway, objects.AmbiguousAirway)):
                    # next element was ambiguous and was preceded by an airway
                    for waypoint in item.possibilities:
                        for airway in waypoint.available_airways:
                            if airway == input_route.elements[next_index].identifier:
                                input_route.deambiguate(current_index, item.possibilities.index(waypoint))
    return input_route


def deambiguate_airways_using_points(input_route: objects.Route) -> objects.Route:
    """

    how can I make this fail in a better way?

    use adjacent waypoints to solve ambiguous airways
    :param input_route: Route object
    :return: Route object with airways deambiguated using waypoints
    """
    
    for item in input_route.elements:
        
        match_flag = False

        if isinstance(item, objects.AmbiguousAirway):
            
            current_index = input_route.elements.index(item)
            previous_index = input_route.elements.index(item) - 1
            next_index = input_route.elements.index(item) + 1
            previous_item = input_route.elements[previous_index]
            next_item = input_route.elements[next_index]
            
            for airway in item.possibilities:
                match_flag = False
                for waypoint in airway.waypoints:
                    if all([waypoint.identifier == previous_item.identifier,
                           waypoint.coordinates == previous_item.coordinates]):
                        for second_waypoint in airway.waypoints:
                            if all([second_waypoint.identifier == next_item.identifier, 
                                   second_waypoint.coordinates == next_item.coordinates]):
                                input_route.deambiguate(current_index, item.possibilities.index(airway))
                                match_flag = True
                            if match_flag:
                                break
                    if match_flag:
                        break
                if match_flag:
                    break
            if not match_flag:
                print("Unable to deambiguate airway", item.identifier)
                # raise ValueError("Unable to deambiguate airway(s). Cannot continue. RAISED ERROR")
    
    return input_route


def slice_airways(input_route) -> objects.Route:
    """
    slices airways into only the waypoints you want
    :param input_route: Route object
    :return: Route object with airways sliced
    """
    
    for item in input_route.elements:
        if isinstance(item, (objects.Airway)):
            current_index = input_route.elements.index(item)
            previous_index = input_route.elements.index(item) - 1
            next_index = input_route.elements.index(item) + 1
            previous_item = input_route.elements[previous_index]
            next_item = input_route.elements[next_index]

            # are we in the right order or do we need to reverse?

            full_airway_waypoints = []

            for waypoint in item.waypoints:
                full_airway_waypoints.append(waypoint.identifier)

            if full_airway_waypoints.index(previous_item.identifier) > full_airway_waypoints.index(next_item.identifier):
                # we need to reverse the airway waypoints
                item.reverse_waypoints()

            start_position = None  # where is previous position in item.waypoints?
            end_position = None  # where is next position in item.waypoints?

            for waypoint in item.waypoints:
                if waypoint.identifier == previous_item.identifier and waypoint.coordinates == previous_item.coordinates:
                    start_position = item.waypoints.index(waypoint)
                if waypoint.identifier == next_item.identifier and waypoint.coordinates == next_item.coordinates:
                    end_position = item.waypoints.index(waypoint)

            if start_position is None or end_position is None:
                print("Unable to connect airway(s).  Cannot continue.")
                return
            
            input_route.replace_element(current_index, item.get_segment(start_position + 1, end_position))

    return input_route


def manual_waypoint_maker(input_string: str) -> objects.PointInSpace | None:
    """
    turns user-inputted lat/long into usable manual waypoint
    :param input_string: user input lat/long coordinates
    :return: manual waypoint object or None
    """

    # also need to allow for 234234N/234234W format
    if "." in input_string:  # decimal format entered
        coordinates = tuple(input_string.split('/'))
    elif "N" or "S" or "E" or "W" in input_string:  # N/S/E/W degrees/minutes format entered
        coordinates = tuple(input_string.split('/'))  # not done - need to finish!
    else:  # bad coordinates entered
        return None
    # assert that it's valid?  maybe that's handled in new coordinates object?
    manual_waypoint = objects.PointInSpace(input_string, coordinates, 'manual waypoint')

    return manual_waypoint


def terminal_procedure_recognizer(input_string: str) -> bool:
    """
    checks if input string is a terminal procedure using regular expressions
    :param input_string: user input string
    :return: True if input string is a terminal procedure, False if not
    """
    
    # do we start with 3-5 letters, have one number, and may end with a letter?
    pattern = r"^[A-Z]{3,5}\d[A-Z]?$"

    return bool(re.match(pattern, input_string))
