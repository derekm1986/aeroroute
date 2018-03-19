# takes inputted waypoints and turns them into a list of waypoint pairs


def pairmaker(inputwaypoints):

    i = 0

    while i <= (len(inputwaypoints) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [inputwaypoints[i], inputwaypoints[i + 1]]
        i += 1
        yield pair
