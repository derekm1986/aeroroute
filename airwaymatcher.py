import objects


def airway_matcher(pointsinspacedict, airwaydict):
    for airwaynames in airwaydict.values():
        # print(airwaynames)
        # print(type(airwaynames))
        if isinstance(airwaynames, objects.AmbiguousAirway):  # we have encountered an Ambiguousairway
            for airway in airwaynames.get_possibilities():
                # print(airway)
                for waypoint in airway.get_waypoints():
                    if waypoint.get_identifier() in pointsinspacedict:
                        if isinstance(pointsinspacedict[waypoint.get_identifier()], objects.AmbiguousElement):
                            # trying to match with an ambiguous element in the pointsinspacedict, need a loop
                            for point in pointsinspacedict[waypoint.get_identifier()].get_possibilities():
                                if point.get_coordinates() == waypoint.get_coordinates():
                                    if airway.get_airway_name() not in point.get_airways():
                                        point.add_airway(airway.get_airway_name())
                        else:
                            # trying to match with a single item
                            if pointsinspacedict[waypoint.get_identifier()].get_coordinates() == \
                                    waypoint.get_coordinates():
                                # need to check if it's there first!
                                if airway.get_airway_name() not in \
                                        pointsinspacedict[waypoint.get_identifier()].get_airways():
                                    pointsinspacedict[waypoint.get_identifier()].add_airway(airway.get_airway_name())
        else:  # we have encountered an Airway by itself
            for waypoint in airwaynames.get_waypoints():
                if waypoint.get_identifier() in pointsinspacedict:
                    if isinstance(pointsinspacedict[waypoint.get_identifier()], objects.AmbiguousElement):
                        # trying to match with an ambiguous element in the pointsinspacedict, need a loop
                        for point in pointsinspacedict[waypoint.get_identifier()].get_possibilities():
                            if point.get_coordinates() == waypoint.get_coordinates():
                                if airwaynames.get_airway_name() not in point.get_airways():
                                    point.add_airway(airwaynames.get_airway_name())
                    else:
                        # trying to match with a single item
                        if pointsinspacedict[waypoint.get_identifier()].get_coordinates() == waypoint.get_coordinates():
                            # need to check if it's there first!
                            if airwaynames.get_airway_name() not in \
                                    pointsinspacedict[waypoint.get_identifier()].get_airways():
                                pointsinspacedict[waypoint.get_identifier()].add_airway(airwaynames.get_airway_name())
    return pointsinspacedict
