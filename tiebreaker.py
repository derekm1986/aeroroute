# this file is for when a route item is returned with multiple lat/longs, keeping separate for testing

import functions
import objects


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
                    trydistance = functions.distancefinder(((inputwaypoints.getpossibility(0, possibility),
                        inputwaypoints.getelement(1))))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(0, shortestpossibility)
            elif inputwaypoints.howmanyelements() - 1 in multipleset:
                print('Single multiple was found at the end')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints.getpossibilities(multipleset[0]):
                    trydistance = functions.distancefinder((inputwaypoints.getelement(multipleset[0]-1),
                        inputwaypoints.getpossibility(multipleset[0], possibility)))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(multipleset[0], shortestpossibility)
            else:
                print('Single multiple found in middle of route')
                shortestdistance = float("inf")  # establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints.getpossibilities(multipleset[0]):
                    trydistance = functions.distancefinder((inputwaypoints.getelement(multipleset[0]-1),
                        inputwaypoints.getpossibility(multipleset[0], possibility),
                        inputwaypoints.getelement(multipleset[0]+1)))
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                    possibility += 1
                    # put lat/long back where it belongs
                inputwaypoints.deambiguate(multipleset[0], shortestpossibility)

    return inputwaypoints


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

        ###############################################################
        #do magic things here like unpacking possibilities

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
                else: # the element is ambiguous
                    print('more work to do here')
                    ambiguousid = 0
                    for possibility in element.waypoint.getpossibilities():
                        print(len(element.waypoint.getpossibilities())) # copy the ones already present by this number
#                        possibilitieslist.append() to each possibility **use from above**
                        ambiguousid =+ 1

            elementposition += 1


        #for thing in multiplesetelements:
            #unpack somehow
        ###############################################################

    print('possibilitieslist is:', possibilitieslist)

    for thing in possibilitieslist:
        print(thing)

    return inputwaypoints
