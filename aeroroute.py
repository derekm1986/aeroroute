"""
A program I use to get the length of routes typed in human-readable
format.  Requires AIRAC files in vasFMC format in a /AIRAC/ folder.
"""
import nav_data_library
import functions
import objects
import logging


def main() -> None:
    """
    The main method of the program
    :return: nothing
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s (%(levelname)s): %(message)s (Line: %(lineno)d [%(filename)s])",
        datefmt='%Y-%m-%d %I:%M:%S %p',
        filename='aeroroute.log',
        encoding='utf-8',
        filemode='w'
    )
    
    print('\n***Aeroroute loading***')

    logging.info("Program starting")

    # create nav_data_library object
    nav_data = nav_data_library.NavDataLibrary()

    while True:

        # allows user to input waypoint(s)/exit instructions to list
        print('\nType "quit" to exit program, enter 20.000000/-123.000000 or 5029N/05120W format for manual waypoints')
        input_string = input("Enter input string: ")
        print("")
        input_string = input_string.upper()

        logging.info("Input string was: " + input_string)  # log inputted string

        input_list = input_string.split()

        if len(input_list) == 0:
            print("No input detected")
            continue

        if "QUIT" in input_list:
            print('***Program exiting***')
            break
        
        if len(input_list) == 1:  # single item, what happens if item doesn't exist?
            print('Single item detected, looking up item.')
            logging.info("Looking up single item: " + input_list[0])
            found_item = nav_data.nav_data_searcher(input_list[0])
            if found_item is None:
                logging.info("Single item " + input_list[0] + " not found.")
                print(input_list[0] + " not found.")
            else:
                logging.info("Single item " + input_list[0] + " is " + str(found_item))
                print(found_item)
            continue

        if multiple_adjacent_string_detector(input_list):  # if true, there were multiple identical adjacent items
            continue

        # no multiple adjacent inputs, pass on to list_parser
        input_route_obj = functions.list_parser(input_list, nav_data)

        if input_route_obj is None:  # something bad came back from string_parser
            logging.warning("string_parser returned None, back to beginning of loop")
            continue

        if input_route_obj.contains_airway:  # is there an airway in the route?
            # is airway at beginning of route? - not OK
            if isinstance(input_route_obj.first_element, (objects.Airway, objects.AmbiguousAirway)):
                logging.warning("Route started with an airway, back to beginning of loop")
                print("Route cannot start with an airway")
                continue

            # is airway at end of route? - not OK
            if isinstance(input_route_obj.last_element, (objects.Airway, objects.AmbiguousAirway)):
                logging.warning("Route ended with an airway, back to beginning of loop")
                print("Route cannot end with an airway")
                continue

            # no airways should touch another airway
            if adjacent_airway_detector(input_route_obj):
                # airways touch other airways - not OK
                continue

            # go through each airway to detect an ambiguous airway and solve it
            #while input_route_obj.contains_airway:
                # this could be infinite if no changes are made
            #    print("going through each airway")
            # call a function that incorporates an airwayinroute into the route

        if input_route_obj.contains_ambiguous_point:  # try solving with adjacent airways

            logging.info("Ambiguous point(s) detected. Trying to solve using adjacent airways.")
            input_route_obj = functions.deambiguate_points_using_airways(input_route_obj)

        if input_route_obj.contains_ambiguous_point:  # adjacent airways didn't find everything, brute is needed

            logging.info("Ambiguous point(s) still detected. Using brute deambiguator.")
            multiples_map = functions.multiple_point_finder(input_route_obj)
            input_route_obj = functions.deambiguator_brute(input_route_obj, multiples_map)

        for item in input_route_obj.elements:
            print(item)

        sum_distance = functions.distance_summer(input_route_obj)

        print('Distance in nm:', sum_distance)


def multiple_adjacent_string_detector(input_list: list[str]) -> bool:
    """
    detects if there are multiple adjacent identical strings
    :param input_list: list of strings
    :return: True if detected, False if not detected
    """
    for i in range(len(input_list) - 1):
        if input_list[i] == input_list[i + 1]:
            logging.warning("Multiple adjacent input found with name: " + input_list[i])
            print('Multiple adjacent input found with name', input_list[i], '- unable to compute.')
            return True
    return False

def adjacent_airway_detector(input_route_obj) -> bool:
    """
    detects if two Airways or AmbiguousAirways are touching
    :param input_route_obj: input Route object containing route elements
    :return: True if detected, False if not detected 
    """
    for i in range(input_route_obj.num_elements - 1):
        if isinstance(input_route_obj.get_element(i), (objects.Airway, objects.AmbiguousAirway)) and \
                      isinstance(input_route_obj.get_element(i+1), (objects.Airway, objects.AmbiguousAirway)):
            logging.warning("Adjacent airways were found: " + str(input_route_obj.get_element(i)) + " " +
                            str(input_route_obj.get_element(i+1)))
            print(("Adjacent airways found.  Unable to compute."))
            return True
    return False

if __name__ == "__main__":
    main()
