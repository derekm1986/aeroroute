import objects

def airwaymatcher(pointsinspacedict, airwaydict):
    for airwaynames in airwaydict.values():
        #print(airwaynames)
        for airway in airwaynames:
            #print(airway)
            for waypoint in airway.getwaypoints():
                #print(waypoint)
                #print(waypoint.getidentifier())
                if waypoint.getidentifier() in pointsinspacedict:
                    #print(waypoint)
                    if isinstance(pointsinspacedict[waypoint.getidentifier()], objects.Ambiguouselement):
                        # trying to match with an ambiguous element in the pointsinspacedict, need a loop
                        #print("we tried to match with an ambiguouselement")
                        #print(type(pointsinspacedict[waypoint.getidentifier()]))
                        for point in pointsinspacedict[waypoint.getidentifier()].getpossibilities():
                            #print(point)
                            if point.getcoordinates() == waypoint.getcoordinates():
                                #print("we have a match from an ambiguouselement, add to list!!!")
                                if airway.getairwayname() not in point.getairways():
                                    point.addairway(airway.getairwayname())
                    else:
                        # trying to match with a single item
                        # print("we tried to match with a single item")
                        # print(pointsinspacedict[waypoint.getidentifier()])
                        if pointsinspacedict[waypoint.getidentifier()].getcoordinates() == waypoint.getcoordinates():
                            # print("single item match, add to list!!!")
                            # need to check if it's there first!
                            if airway.getairwayname() not in pointsinspacedict[waypoint.getidentifier()].getairways():
                                pointsinspacedict[waypoint.getidentifier()].addairway(airway.getairwayname())
    return pointsinspacedict
