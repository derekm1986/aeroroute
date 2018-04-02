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
                for iter in inputwaypoints[0].getpossibilities():
                    tryset = [inputwaypoints[0].getpossibilities()[possibility], inputwaypoints[1]]
                    trydistance = functions.vincenty((inputwaypoints[0].getpossibilities()[possibility],
                        inputwaypoints[1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset                    
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[0] = inputwaypoints[0].getpossibilities()[shortestpossibility]
            elif len(inputwaypoints) - 1 in multipleset:
                print('Single multiple was found at the end')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]].getpossibilities():
                    tryset = [inputwaypoints[multipleset[0]-1],
                        inputwaypoints[multipleset[0]].getpossibilities()[possibility]]
                    trydistance = functions.vincenty((inputwaypoints[multipleset[0]-1],
                        inputwaypoints[multipleset[0]].getpossibilities()[possibility]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[multipleset[0]] = inputwaypoints[multipleset[0]].getpossibilities()[shortestpossibility]
            else:
                print('Single multiple found in middle of route')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]].getpossibilities():
                    tryset = [inputwaypoints[multipleset[0]-1],
                        inputwaypoints[multipleset[0]].getpossibilities()[possibility],
                        inputwaypoints[multipleset[0]+1]]
                    trydistance = functions.vincenty((inputwaypoints[multipleset[0]-1],
                        inputwaypoints[multipleset[0]].getpossibilities()[possibility])) + \
                        functions.vincenty((inputwaypoints[multipleset[0]].getpossibilities()[possibility],
                        inputwaypoints[multipleset[0]+1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[multipleset[0]] = inputwaypoints[multipleset[0]].getpossibilities()[shortestpossibility]
#        elif len(multipleset) > 1:  # more than one multiple is inside multipleset
#            print('multiple set with more than one multiple found, no functionality yet')
#            if 0 in multipleset and len(inputwaypoints) - 1 in multipleset:  # all are multiples
#                print('all are multiples')
#                possibilitytree = []
#                # for possibility in multipleset:
#            elif 0 in multipleset:  # starts at beginning of route
#                print('starts at beginning')
#                possibilitytree = []
#                # for possibility in multipleset:
#                # use end + 1 append to all
#            elif len(inputwaypoints) - 1 in multipleset:  # ends at end of route
#                print('ends at end')
#                # use beginning - 1
#                possibilitytree = [inputwaypoints[multipleset[0]-1][2][0]]
#
#                iterator = 0
#
#                for possibility in multipleset:
                    
#                    position = 0

#                    possibilitytree.append(possibilitytree[0])

#                    for latlong in inputwaypoints[possibility][2]:

#                        possibilitytree.append(inputwaypoints[possibility][2][position])
                    
#                        position += 1

#                    iterator += 1

                # for possibility in multipleset:
                    # copy and extend/append to possibilitytree
#                print(possibilitytree)
#            else: # in middle of route
#                print('in middle')
#                possibilitytree = []
                # use beginning - 1
                # for possibility in mutlipleset:
                # use end + 1 append to all

#            for waypoint in multipleset:
#                print('multipleset contains',waypoint, 'length', len(inputwaypoints[waypoint][2]))
#                for possibility in inputwaypoints[waypoint][2]:
#                    print(possibility)
                    

            

    
#    numberofpossibilities = 1        
            
#    if len(possibilitymatrix) == 0:
#        pass
#    elif len(possibilitymatrix) == 1:
#        numberofpossibilities = len(possibilitymatrix[0][1])
#    else:
#        for waypoints in possibilitymatrix:
#            numberofpossibilities = numberofpossibilities * len(waypoints[1])

#    print(possibilitymatrix)
#    print("Number of possibilities:", numberofpossibilities)

    return inputwaypoints


def testtiebreaker(inputwaypoints, multiplesmatrix):


    for multipleset in multiplesmatrix:

        possibilitieslist = []

        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        if len(multipleset) == len(inputwaypoints):
            allareambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif len(inputwaypoints) - 1 in multipleset:
            lastisambiguous = True

        if allareambiguous == True or firstisambiguous == True:
            # start with first possibility
            for element in multipleset[0]:
                possibilitieslist.append(element)

        else:
            # go to the point before the first ambiguouselement and start the list
            # possibilitieslist.append(inputwaypoints[multipleset[0]-1])
            continue


# -------------------------------------old is below----------------------------------------------

        if len(multipleset) == 1:  # one multiple is found standing by itself
            print('Only one multiple found, using adjacent waypoint(s)')
            if 0 in multipleset:
                print('Single multiple was found at the beginning')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[0].getpossibilities():
                    tryset = [inputwaypoints[0].getpossibilities()[possibility], inputwaypoints[1]]
                    trydistance = functions.vincenty((inputwaypoints[0].getpossibilities()[possibility],
                                                      inputwaypoints[1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[0] = inputwaypoints[0].getpossibilities()[shortestpossibility]
            elif len(inputwaypoints) - 1 in multipleset:
                print('Single multiple was found at the end')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]].getpossibilities():
                    tryset = [inputwaypoints[multipleset[0] - 1],
                              inputwaypoints[multipleset[0]].getpossibilities()[possibility]]
                    trydistance = functions.vincenty((inputwaypoints[multipleset[0] - 1],
                                                      inputwaypoints[multipleset[0]].getpossibilities()[possibility]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[multipleset[0]] = inputwaypoints[multipleset[0]].getpossibilities()[shortestpossibility]
            else:
                print('Single multiple found in middle of route')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]].getpossibilities():
                    tryset = [inputwaypoints[multipleset[0] - 1],
                              inputwaypoints[multipleset[0]].getpossibilities()[possibility],
                              inputwaypoints[multipleset[0] + 1]]
                    trydistance = functions.vincenty((inputwaypoints[multipleset[0] - 1],
                                                      inputwaypoints[multipleset[0]].getpossibilities()[possibility])) + \
                                  functions.vincenty((inputwaypoints[multipleset[0]].getpossibilities()[possibility],
                                                      inputwaypoints[multipleset[0] + 1]))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints[multipleset[0]] = inputwaypoints[multipleset[0]].getpossibilities()[shortestpossibility]