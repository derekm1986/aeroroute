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
        input_list = input_string.upper().split()

        if len(input_list) == 0:
            print("No input detected")
            continue

        if "QUIT" in input_list:
            print('***Program exiting***')
            break

        if len(input_list) == 1:  # single item, what happens if item doesn't exist?
            print('Single item detected, looking up item.')
            found_item = nav_data.nav_data_searcher(input_list[0])
            if found_item is None:
                print(input_list[0] + " not found.")
            else:
                print(found_item)
            continue

        if multiple_adjacent_detector(input_list):  # if true, there were multiple identical adjacent items
            continue

        # no multiple adjacent inputs, pass on to list_parser
        input_waypoints_obj = functions.list_parser(input_list, nav_data)

        if input_waypoints_obj is None:  # something bad came back from string_parser
            continue

        if input_waypoints_obj.get_contains_airway():  # is there an airway in the route?
            # is airway at beginning of route? - not OK
            if isinstance(input_waypoints_obj.get_first_element(), objects.Airway) or \
                    isinstance(input_waypoints_obj.get_first_element(), objects.AmbiguousAirway):
                print("Route cannot start with an airway")
                continue

            # is airway at end of route? - not OK
            if isinstance(input_waypoints_obj.get_last_element(), objects.Airway) or \
                    isinstance(input_waypoints_obj.get_last_element(), objects.AmbiguousAirway):
                print("Route cannot end with an airway")
                continue

            # no airways should touch another airway

            # can any ambiguous elements be solved by matching with an adjacent airway?

            # if there is an airway in input_waypoints_obj, call a function that incorporates the airway into the route

        if input_waypoints_obj.get_contains_ambiguous_point():  # do we contain an AmbiguousElement?

            multiples_matrix = functions.multiple_finder(input_waypoints_obj)

            input_waypoints_obj = functions.deambiguator_brute(input_waypoints_obj, multiples_matrix)

        for item in input_waypoints_obj.get_waypoints():
            print(item)

        sum_distance = functions.distance_summer(input_waypoints_obj)

        print('Distance in nm:', sum_distance)


def multiple_adjacent_detector(input_list: list[str]) -> bool:
    """
    detects if there are multiple adjacent identical strings
    :param input_list: list of strings
    :return: True if detected, False if not detected
    """
    for i in range(len(input_list) - 1):
        if input_list[i] == input_list[i + 1]:
            print('Multiple adjacent input found with name', input_list[i], '- unable to compute.')
            return True
    return False


if __name__ == "__main__":
    main()
