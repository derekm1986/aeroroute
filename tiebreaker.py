# this file is for when a route item is returned with multiple lat/longs, keeping separate for testing

import functions


def tiebreaker(inputwaypoints, multiplesmatrix):
        
    print('multiplesmatrix contents:', multiplesmatrix)  # for debug
               
    for multipleset in multiplesmatrix:
        # print(multipleset) #for debug
        if len(multipleset) == 1:  # one multiple is found standing by itself
            print('Only one multiple found, using adjacent waypoint(s)')
            if 0 in multipleset:
                print('Single multiple was found at the beginning')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints.getpossibilities(0):
                    tryset = [inputwaypoints.getroute()[0].getpossibilities()[possibility], inputwaypoints.getroute()[1]]
                    trydistance = functions.vincentyindirect((inputwaypoints.getroute()[0].getpossibilities()[possibility],
                        inputwaypoints.getroute()[1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(0, shortestpossibility)
            elif inputwaypoints.howmanyelements() - 1 in multipleset:
                print('Single multiple was found at the end')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints.getpossibilities(multipleset[0]):
                    tryset = [inputwaypoints.getroute()[multipleset[0]-1],
                        inputwaypoints.getroute()[multipleset[0]].getpossibilities()[possibility]]
                    trydistance = functions.vincentyindirect((inputwaypoints.getroute()[multipleset[0]-1],
                        inputwaypoints.getroute()[multipleset[0]].getpossibilities()[possibility]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(multipleset[0], shortestpossibility)
            else:
                print('Single multiple found in middle of route')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints.getpossibilities(multipleset[0]):
                    tryset = [inputwaypoints.getroute()[multipleset[0]-1],
                        inputwaypoints.getroute()[multipleset[0]].getpossibilities()[possibility],
                        inputwaypoints.getroute()[multipleset[0]+1]]
                    trydistance = functions.vincentyindirect((inputwaypoints.getroute()[multipleset[0]-1],
                        inputwaypoints.getroute()[multipleset[0]].getpossibilities()[possibility])) + \
                        functions.vincentyindirect((inputwaypoints.getroute()[multipleset[0]].getpossibilities()[possibility],
                        inputwaypoints.getroute()[multipleset[0]+1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(multipleset[0], shortestpossibility)

    return inputwaypoints


def testtiebreaker(inputwaypoints, multiplesmatrix):


    for multipleset in multiplesmatrix:

        possibilitieslist = []

        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        if len(multipleset) == inputwaypoints.howmanyelements():
            allareambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif inputwaypoints.howmanyelements() - 1 in multipleset:
            lastisambiguous = True

        if allareambiguous == True or firstisambiguous == True:
            # start with first possibility
            for element in inputwaypoints.getelement(multipleset[0]):
                possibilitieslist.append(element)

        else:
            possibilitieslist.append(inputwaypoints.getelement(multipleset[0]-1))
            # go to the point before the first ambiguouselement and start the list

    print(possibilitieslist)

    return inputwaypoints