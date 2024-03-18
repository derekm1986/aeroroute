import airportsreader
import navaidsreader
import waypointsreader
import atsreader
import logging
import objects


class NavDataLibrary(object):
    # trying to keep all the nav data in an object
    def __init__(self):
        logging.info("Loading airports into memory")
        self.airport_dict = airportsreader.airport_dict_maker()
        logging.info("Airports loaded into memory")  # loading airports was successful

        logging.info("Loading NAVAIDs into memory")
        self.navaid_dict = navaidsreader.navaid_dict_maker()
        logging.info("NAVAIDs loaded into memory")  # loading NAVAIDs was successful

        logging.info("Loading waypoints into memory")
        self.waypoint_dict = waypointsreader.waypoint_dict_maker()
        logging.info("Waypoints loaded into memory")  # loading elements was successful

        logging.info("Loading airways into memory")
        self.airway_dict = atsreader.airway_dict_maker()
        logging.info("Airways loaded into memory")  # loading airways was successful

        logging.info("Combining NAVAID and waypoint dictionaries")
        self.points_in_space_dict = self.points_in_space_dict_combiner()
        logging.info("NAVAID and waypoint dictionaries combined")  # dictionary combination was successful
        
        logging.info("Adding airway references to combined dictionary")
        self.airway_matcher()
        logging.info("Airway references added to combined dictionary")  # reference matching was successful

        logging.info("NAV data loading complete")

    def points_in_space_dict_combiner(self):

        points_in_space_dict = self.navaid_dict.copy()

        for key, val in self.waypoint_dict.items():
            if key in points_in_space_dict:
                # the entry is already in points_in_space_dict
                if type(points_in_space_dict[key]) is objects.AmbiguousPoint:
                    # points_in_space_dict already has AmbiguousPoint
                    if type(val) is objects.AmbiguousPoint:
                        # must add AmbiguousPoint to AmbiguousPoint
                        points_in_space_dict[key].add_possibility(self.waypoint_dict[key].possibilities)
                    else:
                        # must add PointInSpace to AmbiguousPoint
                        points_in_space_dict[key].add_possibility(self.waypoint_dict[key])
                else:
                    # points_in_space_dict contains a PointInSpace
                    if type(val) is objects.AmbiguousPoint:
                        # Adding AmbiguousPoint to a PointInSpace, make a new AmbiguousPoint
                        original_point_in_space = points_in_space_dict[key]
                        points_in_space_dict[key] = val
                        points_in_space_dict[key].add_possibility(original_point_in_space)
                    else:
                        # Adding PointInSpace to a PointInSpace
                        points_in_space_dict[key] = objects.AmbiguousPoint(key, points_in_space_dict[key])
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
                for airway in airway_names.possibilities:
                    # print(airway)
                    for waypoint in airway.waypoints:
                        if waypoint.identifier in self.points_in_space_dict:
                            if isinstance(self.points_in_space_dict[waypoint.identifier], objects.AmbiguousPoint):
                                # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                                for point in self.points_in_space_dict[waypoint.identifier].possibilities:
                                    if point.coordinates == waypoint.coordinates:
                                        if airway.identifier not in point.available_airways:
                                            point.add_available_airway(airway.identifier)
                            else:
                                # trying to match with a single item
                                if self.points_in_space_dict[waypoint.identifier].coordinates == \
                                        waypoint.coordinates:
                                    # need to check if it's there first!
                                    if airway.identifier not in \
                                            self.points_in_space_dict[waypoint.identifier].available_airways:
                                        self.points_in_space_dict[waypoint.identifier].add_available_airway(
                                            airway.identifier)
            else:  # we have encountered an Airway by itself
                for waypoint in airway_names.waypoints:
                    if waypoint.identifier in self.points_in_space_dict:
                        if isinstance(self.points_in_space_dict[waypoint.identifier], objects.AmbiguousPoint):
                            # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                            for point in self.points_in_space_dict[waypoint.identifier].possibilities:
                                if point.coordinates == waypoint.coordinates:
                                    if airway_names.identifier not in point.available_airways:
                                        point.add_available_airway(airway_names.identifier)
                        else:
                            # trying to match with a single item
                            if self.points_in_space_dict[waypoint.identifier].coordinates == \
                                    waypoint.coordinates:
                                # need to check if it's there first!
                                if airway_names.identifier not in \
                                        self.points_in_space_dict[waypoint.identifier].available_airways:
                                    self.points_in_space_dict[waypoint.identifier].add_available_airway(
                                        airway_names.identifier)

    def nav_data_searcher(self, item):

        found_item = None

        if "/" in item:  # manual input detected
            found_item = self.manual_waypoint_maker(item)

        elif item in self.airport_dict:
            found_item = self.airport_dict[item]

        elif item in self.points_in_space_dict:
            found_item = self.points_in_space_dict[item]

        elif item in self.airway_dict:  # not finished
            print(item + ' was found in airway_dict, functionality not finished')
            found_item = self.airway_dict[item]

        # elif put something here to read SIDs/STARs
        # is it adjacent to an airport? if no, reject
        # combination of letters and numbers? HYLND6 or CSTL4 or SHB4 or UNOKO3A
        # flag as possible SID/STAR?

        return found_item

    @staticmethod
    def manual_waypoint_maker(input_string: str) -> objects.PointInSpace | None:
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



