import airportsreader
import navaidsreader
import waypointsreader
import atsreader
import functions
import airwaymatcher
import logging


class NavDataLibrary(object):
    # trying to keep all the nav data in an object
    def __init__(self):
        print('   OBJ*Loading airports into memory...', end="")
        self.airport_dict = airportsreader.airport_dict_maker()
        print('OK')  # loading airports was successful

        print('   OBJ*Loading NAVAIDs into memory...', end="")
        self.navaid_dict = navaidsreader.navaid_dict_maker()
        print('OK')  # loading NAVAIDs was successful

        print('   OBJ*Loading waypoints into memory...', end="")
        self.waypoint_dict = waypointsreader.waypoint_dict_maker()
        print('OK')  # loading elements was successful

        print('   OBJ*Loading airways into memory...', end="")
        self.airway_dict = atsreader.airway_dict_maker()
        print('OK')  # loading airways was successful

        print('\nOBJ*Combining NAVAID and waypoint dictionaries...', end="")
        self.points_in_space_dict = functions.points_in_space_dict_combiner(self.navaid_dict, self.waypoint_dict)
        print("OK")  # dictionary combination was successful
        
        print('OBJ*Adding airway references to combined dictionary...', end="")
        self.points_in_space_dict = airwaymatcher.airway_matcher(self.points_in_space_dict, self.airway_dict)
        print("OK")  # reference matching was successful

        logging.info("Test message from object")

    def add_airport_dict(self, airport_dict):
        self.airport_dict = airport_dict

    def lookup_item(self, search_string):
        # put functionality from nav_data_searcher here
        pass
