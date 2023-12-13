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
    
    print('\n***Aeroroute loading***', '\n')

    logging.info("Program starting")

    # create nav_data_library object
    nav_data = nav_data_library.NavDataLibrary()

    while True:

        # allows user to input waypoint(s)/exit instructions to list
        print('\nType "quit" to exit program, enter 20.000000/-123.000000 format for manual elements')
        input_string = input("Enter input string: ")
        input_string = input_string.upper().split()

        if len(input_string) == 0:
            print("No input detected")
            continue

        if "QUIT" in input_string:
            print('***Program exiting***')
            break

        if len(input_string) == 1:  # single item
            print('Single item detected, printing entry:', nav_data.nav_data_searcher(input_string[0]))
            continue

        # double adjacent input detection
        double_input_flag = False
        if len(input_string) > 1:
            for i in range(len(input_string) - 1):
                if input_string[i] == input_string[i + 1]:
                    print('Multiple adjacent input found with name', input_string[i], '- unable to compute.')
                    double_input_flag = True
                    break

        if double_input_flag:
            continue

        # no double inputs, pass on to list_parser
        input_waypoints_obj = functions.list_parser(input_string, nav_data)

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


if __name__ == "__main__":
    main()
