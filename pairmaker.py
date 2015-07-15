#takes inputted waypoints and turns them into a list of waypoint pairs

def pairmaker(inputwaypoints):

    waypointpairs = []

    i = 0

    while i <= (len(inputwaypoints) - 2): #make pairs of each waypoint and the waypoint after it
        waypoint1 = inputwaypoints[i]
        waypoint2 = inputwaypoints[i + 1]
        waypointpairs.append(waypoint1 + waypoint2) #why does this line blow up??!?!
        i = i + 1
    
    return waypointpairs