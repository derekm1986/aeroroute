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
        self.points_in_space_dict = self.points_in_space_dict_combiner()
        print("OK")  # dictionary combination was successful
        
        print('OBJ*Adding airway references to combined dictionary...', end="")
        self.airway_matcher()
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

    def airway_matcher(self):
        for airway_names in self.airway_dict.values():
            # print(airway_names)
            # print(type(airway_names))
            if isinstance(airway_names, objects.AmbiguousAirway):  # we have encountered an AmbiguousAirway
                for airway in airway_names.get_possibilities():
                    # print(airway)
                    for waypoint in airway.get_waypoints():
                        if waypoint.get_identifier() in self.points_in_space_dict:
                            if isinstance(self.points_in_space_dict[waypoint.get_identifier()], objects.AmbiguousElement):
                                # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                                for point in self.points_in_space_dict[waypoint.get_identifier()].get_possibilities():
                                    if point.get_coordinates() == waypoint.get_coordinates():
                                        if airway.get_airway_name() not in point.get_airways():
                                            point.add_airway(airway.get_airway_name())
                            else:
                                # trying to match with a single item
                                if self.points_in_space_dict[waypoint.get_identifier()].get_coordinates() == \
                                        waypoint.get_coordinates():
                                    # need to check if it's there first!
                                    if airway.get_airway_name() not in \
                                            self.points_in_space_dict[waypoint.get_identifier()].get_airways():
                                        self.points_in_space_dict[waypoint.get_identifier()].add_airway(
                                            airway.get_airway_name())
            else:  # we have encountered an Airway by itself
                for waypoint in airway_names.get_waypoints():
                    if waypoint.get_identifier() in self.points_in_space_dict:
                        if isinstance(self.points_in_space_dict[waypoint.get_identifier()], objects.AmbiguousElement):
                            # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                            for point in self.points_in_space_dict[waypoint.get_identifier()].get_possibilities():
                                if point.get_coordinates() == waypoint.get_coordinates():
                                    if airway_names.get_airway_name() not in point.get_airways():
                                        point.add_airway(airway_names.get_airway_name())
                        else:
                            # trying to match with a single item
                            if self.points_in_space_dict[waypoint.get_identifier()].get_coordinates() == \
                                    waypoint.get_coordinates():
                                # need to check if it's there first!
                                if airway_names.get_airway_name() not in \
                                        self.points_in_space_dict[waypoint.get_identifier()].get_airways():
                                    self.points_in_space_dict[waypoint.get_identifier()].add_airway(
                                        airway_names.get_airway_name())
        return


