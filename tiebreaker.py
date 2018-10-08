# this file is for when a route item is returned with multiple lat/longs, keeping separate for testing

import functions
import objects


def tiebreaker(inputwaypoints, multiplesmatrix):


    for multipleset in multiplesmatrix:

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
            
        elementposition = 0

        for element in multiplesetelements:
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

        print('there are ', len(possibilitieslist), 'possibilities to compute')

        leaderboard = []

        for possibility in possibilitieslist: # compute distances
            leaderboard.append([functions.distancefinder(possibility), possibility])

        shortestdistance = float('Inf')

        for competitor in leaderboard: # establish which is shortest
            if competitor[0] < shortestdistance:
                shortestdistance = competitor[0]
                shortestcompetitor = competitor

        for point in shortestcompetitor[1]: # deambiguate using shortestcompetitor
            if point.getwasambiguous() is True:
                inputwaypoints.deambiguate(point.getoriginalposition(), point.getambiguousid())

    return inputwaypoints
