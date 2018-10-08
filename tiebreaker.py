# this file is for when a route item is returned with multiple lat/longs, keeping separate for testing

import functions
import objects


def testtiebreaker(inputwaypoints, multiplesmatrix):

    print('was sent to testtiebreaker')

    for multipleset in multiplesmatrix:

        print('multipleset was: ', multipleset)
        
        allareambiguous = False
        firstisambiguous = False
        lastisambiguous = False

        possibilitieslist = []
        multiplesetelements = []
        
        if len(multipleset) == inputwaypoints.howmanyelements():
            allareambiguous = True
            firstisambiguous = True
            lastisambiguous = True

        elif 0 in multipleset:
            firstisambiguous = True

        elif inputwaypoints.howmanyelements() - 1 in multipleset:
            lastisambiguous = True

        print('allareambiguous is ' + str(allareambiguous))
        print('firstisambiguous is ' + str(firstisambiguous))
        print('lastisambiguous is ' + str(lastisambiguous))

        for listposition in multipleset:
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(listposition), 
                                       listposition, True))
                
        if allareambiguous is False and firstisambiguous is False:
            # add previous waypoint to beginning of multiplesetelements
            multiplesetelements.insert(0, objects.TBWrapper(inputwaypoints.getelement(multipleset[0] - 1),
                                       multipleset[0] - 1))
            
        if allareambiguous is False and lastisambiguous is False:
            # add following waypoint to end of multiplesetelements 
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(multipleset[-1] + 1),
                                       multipleset[-1] + 1))
            

        print('multiplesetelements is: ', multiplesetelements)

        for thing in multiplesetelements:
            print(thing)

        elementposition = 0

        for element in multiplesetelements:
            print('current element is: ', element)
            if elementposition == 0: # first in the list, no copying needed here
                if element.wasambiguous is False: # single element present
                    possibilitieslist.append([element])
                else: # the element is ambiguous
                    ambiguousid = 0
                    for possibility in element.waypoint.getpossibilities():
                        possibilitieslist.append([objects.TBWrapper(possibility, element.getoriginalposition(), True,
                                                                   ambiguousid)])
                        ambiguousid += 1

            else: # it's after first in the list

                if element.wasambiguous is False: # single element present
                    for item in possibilitieslist:
                        item.append(element) # add to each list by one
                else:  # the element is ambiguous, complicated copy and append operation needed
                    possibilitieslist = functions.complicatedappender(possibilitieslist, element)

            elementposition += 1

        print('possibilitieslist is:') # for debug
        for thing in possibilitieslist:
            print(thing)
            for insidething in thing:
                print(insidething)

        print('there are ', len(possibilitieslist), 'possibilities to compute')

        # compute distances

        leaderboard = []

        for possibility in possibilitieslist:
            print(functions.distancefinder(possibility))
            leaderboard.append([functions.distancefinder(possibility), possibility])

        print('leaderboard is: ', leaderboard)

        shortestdistance = float('Inf')

        for competitor in leaderboard: # establish which is shortest
            print(competitor[0], shortestdistance)
            if competitor[0] < shortestdistance:
                shortestdistance = competitor[0]
                shortestcompetitor = competitor

        print('shortestcompetitor is: ', shortestcompetitor)

        # which is shortest

        # deambiguate the ambiguouselements in shortest list in inputwaypoints

        for point in shortestcompetitor[1]:
            if point.getwasambiguous() is True:
                print(point, 'was ambiguous')
                inputwaypoints.deambiguate(point.getoriginalposition(), point.getambiguousid())
                #deambiguate!!!!


    return inputwaypoints
