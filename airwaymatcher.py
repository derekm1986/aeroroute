import objects

def airwaymatcher(pointsinspacedict, airwaydict):
    for airwaynames in airwaydict.values():
        #print(airwaynames)
        #print(type(airwaynames))
        if isinstance(airwaynames, objects.AmbiguousAirway):  # we have encountered an Ambiguousairway
            for airway in airwaynames.getpossibilities():
                #print(airway)
                for waypoint in airway.getwaypoints():
                    if waypoint.getidentifier() in pointsinspacedict:
                        if isinstance(pointsinspacedict[waypoint.getidentifier()], objects.AmbiguousElement):
                            # trying to match with an ambiguous element in the pointsinspacedict, need a loop
                            for point in pointsinspacedict[waypoint.getidentifier()].getpossibilities():
                                if point.getcoordinates() == waypoint.getcoordinates():
                                    if airway.getairwayname() not in point.getairways():
                                        point.addairway(airway.getairwayname())
                        else:
                            # trying to match with a single item
                            if pointsinspacedict[waypoint.getidentifier()].getcoordinates() == waypoint.getcoordinates():
                                # need to check if it's there first!
                                if airway.getairwayname() not in pointsinspacedict[waypoint.getidentifier()].getairways():
                                    pointsinspacedict[waypoint.getidentifier()].addairway(airway.getairwayname())
        else:  # we have encountered an Airway by itself
            for waypoint in airwaynames.getwaypoints():
                if waypoint.getidentifier() in pointsinspacedict:
                    if isinstance(pointsinspacedict[waypoint.getidentifier()], objects.AmbiguousElement):
                        # trying to match with an ambiguous element in the pointsinspacedict, need a loop
                        for point in pointsinspacedict[waypoint.getidentifier()].getpossibilities():
                            if point.getcoordinates() == waypoint.getcoordinates():
                                if airwaynames.getairwayname() not in point.getairways():
                                    point.addairway(airwaynames.getairwayname())
                    else:
                        # trying to match with a single item
                        if pointsinspacedict[waypoint.getidentifier()].getcoordinates() == waypoint.getcoordinates():
                            # need to check if it's there first!
                            if airwaynames.getairwayname() not in pointsinspacedict[waypoint.getidentifier()].getairways():
                                pointsinspacedict[waypoint.getidentifier()].addairway(airwaynames.getairwayname())
    return pointsinspacedict
