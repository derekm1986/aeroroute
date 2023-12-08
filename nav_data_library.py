import airportsreader
import navaidsreader
import waypointsreader
import atsreader
import functions
import airwaymatcher
import logging
import objects


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
        # self.points_in_space_dict = functions.points_in_space_dict_combiner(self.navaid_dict, self.waypoint_dict)
        self.points_in_space_dict = self.points_in_space_dict_combiner()
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

    def points_in_space_dict_combiner(self):

        points_in_space_dict = self.navaid_dict.copy()

        for key, val in self.waypoint_dict.items():
            if key in points_in_space_dict:
                # the entry is already in points_in_space_dict
                if type(points_in_space_dict[key]) is objects.AmbiguousElement:
                    # points_in_space_dict already has Ambiguouselement
                    if type(val) is objects.AmbiguousElement:
                        # must add Ambiguouselement to Ambiguouselement
                        points_in_space_dict[key].add_possibility(self.waypoint_dict[key].get_possibilities())
                    else:
                        # must add Pointinspace to Ambiguouselement
                        points_in_space_dict[key].add_possibility(self.waypoint_dict[key])
                else:
                    # points_in_space_dict contains a Pointinspace
                    if type(val) is objects.AmbiguousElement:
                        # Adding Ambigouselement to a Pointinspace, make a new Ambiguouselement
                        originalpointinspace = points_in_space_dict[key]
                        points_in_space_dict[key] = val
                        points_in_space_dict[key].add_possibility(originalpointinspace)
                    else:
                        # Adding Pointinspace to a Pointinspace
                        points_in_space_dict[key] = objects.AmbiguousElement(key, points_in_space_dict[key])
                        points_in_space_dict[key].add_possibility(val)
            else:
                # the entry is not yet in points_in_space_dict, so just add it
                points_in_space_dict[key] = val

        return points_in_space_dict

