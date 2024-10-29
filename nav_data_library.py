import airportsreader
import navaidsreader
import waypointsreader
import atsreader
import logging
import objects


class NavDataLibrary(object):
    """
    Holds functionality for Nav Data, along with some functionality
    """
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
        """
        combines waypoint_dict and navaid_dict into one dictionary
        :return: points_in_space_dict
        """

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

    def airway_matcher(self) -> None:
        """
        adds airway references into the points_in_space_dict
        :return: None
        """
        for airway_names in self.airway_dict.values():
            if isinstance(airway_names, objects.AmbiguousAirway):  # we have encountered an AmbiguousAirway
                for airway in airway_names.possibilities:
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
        """
        looks for item inside this Nav Data library
        :param item: string to search for
        :return: found object or none
        """
        found_item = None

        if item in self.airport_dict:
            found_item = self.airport_dict[item]

        elif item in self.points_in_space_dict:
            found_item = self.points_in_space_dict[item]

        elif item in self.airway_dict:
            found_item = self.airway_dict[item]

        return found_item


class NavDataLibrary_combined(object):
    """
    Holds functionality for Nav Data, along with some functionality
    In development
    Want this to instead provide a new combined dictionary whose values contain possibilities from all types of entries
    """
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
        """
        combines waypoint_dict and navaid_dict into one dictionary
        :return: points_in_space_dict
        """

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

    def airway_matcher(self) -> None:
        """
        adds airway references into the points_in_space_dict
        :return: None
        """
        for airway_names in self.airway_dict.values():
            if isinstance(airway_names, objects.AmbiguousAirway):  # we have encountered an AmbiguousAirway
                for airway in airway_names.possibilities:
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
        """
        looks for item inside this Nav Data library
        :param item: string to search for
        :return: found object or none
        """
        found_item = None

        if item in self.airport_dict:
            found_item = self.airport_dict[item]

        elif item in self.points_in_space_dict:
            found_item = self.points_in_space_dict[item]

        elif item in self.airway_dict:
            found_item = self.airway_dict[item]

        return found_item

    def combined_dict_creator(self):
        """
        all dictionaries will be combined into one here, work in progress
        """
        combined_dictionary = {}
    
