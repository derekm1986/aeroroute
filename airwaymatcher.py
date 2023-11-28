import objects


def airway_matcher(points_in_space_dict, airway_dict):
    for airway_names in airway_dict.values():
        # print(airway_names)
        # print(type(airway_names))
        if isinstance(airway_names, objects.AmbiguousAirway):  # we have encountered an AmbiguousAirway
            for airway in airway_names.get_possibilities():
                # print(airway)
                for waypoint in airway.get_waypoints():
                    if waypoint.get_identifier() in points_in_space_dict:
                        if isinstance(points_in_space_dict[waypoint.get_identifier()], objects.AmbiguousElement):
                            # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                            for point in points_in_space_dict[waypoint.get_identifier()].get_possibilities():
                                if point.get_coordinates() == waypoint.get_coordinates():
                                    if airway.get_airway_name() not in point.get_airways():
                                        point.add_airway(airway.get_airway_name())
                        else:
                            # trying to match with a single item
                            if points_in_space_dict[waypoint.get_identifier()].get_coordinates() == \
                                    waypoint.get_coordinates():
                                # need to check if it's there first!
                                if airway.get_airway_name() not in \
                                        points_in_space_dict[waypoint.get_identifier()].get_airways():
                                    points_in_space_dict[waypoint.get_identifier()].add_airway(airway.get_airway_name())
        else:  # we have encountered an Airway by itself
            for waypoint in airway_names.get_waypoints():
                if waypoint.get_identifier() in points_in_space_dict:
                    if isinstance(points_in_space_dict[waypoint.get_identifier()], objects.AmbiguousElement):
                        # trying to match with an AmbiguousElement in the points_in_space_dict, need a loop
                        for point in points_in_space_dict[waypoint.get_identifier()].get_possibilities():
                            if point.get_coordinates() == waypoint.get_coordinates():
                                if airway_names.get_airway_name() not in point.get_airways():
                                    point.add_airway(airway_names.get_airway_name())
                    else:
                        # trying to match with a single item
                        if points_in_space_dict[waypoint.get_identifier()].get_coordinates() == \
                                waypoint.get_coordinates():
                            # need to check if it's there first!
                            if airway_names.get_airway_name() not in \
                                    points_in_space_dict[waypoint.get_identifier()].get_airways():
                                points_in_space_dict[waypoint.get_identifier()].add_airway(airway_names.get_airway_name())
    return points_in_space_dict
