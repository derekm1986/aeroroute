#this file is for when a route item is returned with multiple lat/longs

import math
import vincenty
import pairmaker

def tiebreaker(inputwaypoints):

    #print(inputwaypoints)
    
    foundmultiples = [i for i,x in enumerate(inputwaypoints) if len(x[2]) > 1] #finding positions of ambiguous waypoints
    
    multiplesmatrix = []
    
    lastwaypoint = -9999 #have to fill it with something
     
    #this groups ambiguous waypoints together if they are sequential
    for waypoint in foundmultiples: #detect if waypoints are next to each other
        if waypoint == lastwaypoint + 1: #waypoint is sequential to waypoint before it         
            multiplesmatrix[len(multiplesmatrix) - 1].append(waypoint) #group with previous
        else: #waypoint stands alone
            multiplesmatrix.append([waypoint])
        lastwaypoint = waypoint
        
#       if waypoint == 0:
#            print('waypoint was at the beginning')
#            matrixflag = 'beginning'
#            #do something to show it was at the beginning
            
#       if waypoint == len(inputwaypoints) - 1:
#            print('waypoint was at the end')
#            matrixflag = 'end'
#            #do something to show it was at the end

    print('multiplesmatrix contents:', multiplesmatrix) #for debug
               
    for multipleset in multiplesmatrix:
        #print(multipleset) #for debug
        if len(multipleset) == 1: #one multiple is found standing by itself
            print('Only one multiple found, using adjacent waypoint(s)')
            if 0 in multipleset:
                print('Single multiple was found at the beginning')
                shortestdistance = float("inf") #establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[0][2]:
                    tryset = [[inputwaypoints[0][2][possibility], inputwaypoints[1][2][0]]]
                    trydistance = vincenty.vincenty(inputwaypoints[0][2][possibility], inputwaypoints[1][2][0])
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset                    
                    possibility += 1
                    #put lat/long back where it belongs
                inputwaypoints[0][2] = [inputwaypoints[0][2][shortestpossibility]]
            elif len(inputwaypoints) - 1 in multipleset:
                print('Single multiple was found at the end')
                shortestdistance = float("inf") #establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]][2]:
                    tryset = [[inputwaypoints[multipleset[0]-1][2][0], inputwaypoints[multipleset[0]][2][possibility]]]
                    trydistance = vincenty.vincenty(inputwaypoints[multipleset[0]-1][2][0], inputwaypoints[multipleset[0]][2][possibility])
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    #put lat/long back where it belongs
                inputwaypoints[multipleset[0]][2] = [inputwaypoints[multipleset[0]][2][shortestpossibility]]
            else:
                print('Single multiple found in middle of route')
                shortestdistance = float("inf") #establish worst case scenario so anything would be better
                possibility = 0
                for iter in inputwaypoints[multipleset[0]][2]:
                    tryset = [[inputwaypoints[multipleset[0]-1][2][0], inputwaypoints[multipleset[0]][2][possibility], inputwaypoints[multipleset[0]+1][2][0]]]
                    trydistance = vincenty.vincenty(inputwaypoints[multipleset[0]-1][2][0], inputwaypoints[multipleset[0]][2][possibility]) + vincenty.vincenty(inputwaypoints[multipleset[0]][2][possibility], inputwaypoints[multipleset[0]+1][2][0])
                    if trydistance < shortestdistance:
                        shortestdistance = trydistance
                        shortestpossibility = possibility
                        shortestset = tryset
                    possibility += 1
                    #put lat/long back where it belongs
                inputwaypoints[multipleset[0]][2] = [inputwaypoints[multipleset[0]][2][shortestpossibility]]
        elif len(multipleset) > 1: #more than one multiple is inside multipleset
            print('multiple set with more than one multiple found, no functionality yet')
            if 0 in multipleset and len(inputwaypoints) - 1 in multipleset: #all are multiples
                print('all are multiples')
            elif 0 in multipleset: #starts at beginning
                print('starts at beginning')
            elif len(inputwaypoints) - 1 in multipleset: #ends at end
                print('ends at end')
            else: #in middle
                print('in middle')

            for waypoint in multipleset:
                print('multipleset contains',waypoint, 'length', len(inputwaypoints[waypoint][2]))
                for possibility in inputwaypoints[waypoint][2]:
                    print(possibility)
                    

            

    
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