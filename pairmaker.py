# takes inputted waypoints and turns them into a list of waypoint pairs


def pairmaker(inputwaypoints):

    waypointpairs = []

    i = 0

    while i <= (len(inputwaypoints) - 2):  # make pairs of each waypoint and the waypoint after it
        waypoint1 = inputwaypoints[i]
        waypoint2 = inputwaypoints[i + 1]
        temporarylist = []
        temporarylist.append(waypoint1)
        temporarylist.append(waypoint2)
        waypointpairs.append(temporarylist)
        i += 1
    
    return waypointpairs
