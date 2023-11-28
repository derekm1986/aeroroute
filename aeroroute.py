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
import objects


def main():
    """
    The main method of the program
    :return: nothing
    """

    print('\n***Aeroroute loading***', '\n')

    print('Reading AIRAC data...')

    print('   Loading airports into memory...', end="")
    airport_dict = airportsreader.airportdictmaker()
    print('OK')  # loading airports was successful

    print('   Loading NAVAIDs into memory...', end="")
    navaid_dict = navaidsreader.navaid_dict_maker()
    print('OK')  # loading NAVAIDs was successful

    print('   Loading elements into memory...', end="")
    waypoint_dict = waypointsreader.waypointdictmaker()
    print('OK')  # loading elements was successful

    print('   Loading airways into memory...', end="")
    airway_dict = atsreader.airwaydict_maker()
    print('OK')  # loading airways was successful

    print('\nCombining NAVAID and elements dictionaries...', end="")
    points_in_space_dict = functions.points_in_space_dict_combiner(navaid_dict, waypoint_dict)
    print("OK")  # dictionary combination was successful

    print('Adding airway references to combined dictionary...', end="")
    points_in_space_dict = airwaymatcher.airway_matcher(points_in_space_dict, airway_dict)
    print("OK")  # reference matching was successful

    while True:

        # allows user to input waypoint(s)/exit instructions to list
        print('\nType "quit" to exit program, enter 20.000000/-123.000000 format for manual elements')
        input_string = input("Enter input string: ")
        input_string = input_string.upper().split()

        if len(input_string) == 0:
            print("No input detected")
            continue

        double_input_flag = False  # double adjacent input detection

        # put a flag here for double airway input?

        if len(input_string) > 1:
            for i in range(len(input_string) - 1):
                if input_string[i] == input_string[i + 1]:
                    print('Multiple adjacent input found with name', input_string[i], '- unable to compute.')
                    double_input_flag = True
                    break

        if double_input_flag:
            continue

        if "QUIT" in input_string:
            print('***Program exiting***')
            break

        input_waypoints_obj = functions.string_reader(input_string, airport_dict, points_in_space_dict, airway_dict)

        if input_waypoints_obj == "invalidinput":  # something bad came back from string_reader
            continue

        if len(input_waypoints_obj.get_waypoints()) == 1:
            print('Single item detected, printing entry:', input_waypoints_obj.get_element(0))
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

        if input_waypoints_obj.get_contains_ambiguous_element():  # do we contain an AmbiguousElement?

            multiples_matrix = functions.multiple_finder(input_waypoints_obj)

            input_waypoints_obj = functions.deambiguator_brute(input_waypoints_obj, multiples_matrix)

        for item in input_waypoints_obj.get_waypoints():
            print(item)

        sum_distance = functions.distance_finder(input_waypoints_obj)

        print('Distance in nm:', sum_distance)


if __name__ == "__main__":
    main()
