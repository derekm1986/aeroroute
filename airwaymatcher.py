import objects

def airwaymatcher(pointsinspacedict, airwaydict):
    for airwaynames in airwaydict.values():
        for airway in airwaynames:
            for waypoint in airway.getwaypoints():
                if waypoint.getidentifier() in pointsinspacedict:
                    if isinstance(pointsinspacedict[waypoint.getidentifier()], objects.Ambiguouselement):
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
    return pointsinspacedict
