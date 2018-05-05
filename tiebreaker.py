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

        for listposition in multipleset:
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(listposition), 
                                       listposition, True))
                
        if allareambiguous is False and firstisambiguous is False:
            # add previous waypoint to beginning of testmultipleset
            multiplesetelements.insert(0, objects.TBWrapper(inputwaypoints.getelement(multipleset[0] - 1),
                                       multipleset[0] - 1))
            
        if allareambiguous is False and lastisambiguous is False:
            # add following waypoint to end of testmultipleset 
            multiplesetelements.append(objects.TBWrapper(inputwaypoints.getelement(multipleset[-1] + 1),
                                       multipleset[-1] + 1))
            

        print('multiplesetelements is: ', multiplesetelements)


    print(possibilitieslist)

    return inputwaypoints
