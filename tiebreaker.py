#this file is for when a route item is returned with multiple lat/longs

import math
import vincenty
import pairmaker

def tiebreaker(inputwaypoints):

    
    #shortestdistanceset = #combination of waypoints with shortest distance 
    
    #print(inputwaypoints)
    
    foundmultiples = [i for i,x in enumerate(inputwaypoints) if len(x[2]) > 1] #finding positions of multiples
    
    #newfoundmultiples = #make better foundmultiples here, list of lists of adjacent multiples
    #for waypoint in inputwaypoints:
        #if len(waypoint[2]) > 1:
            #print('Found a multiple at position')
    
    print('Found multiples at position(s):',foundmultiples)
    
    #how many waypoints with multiples?
    print("Number of total waypoints with multiples:",len(foundmultiples))
    
    if len(foundmultiples) == 1: #this will only work if one multiple is found
        print('Only one multiple found, using adjacent waypoint(s)')
        if foundmultiples[0] == 0:
            print('One multiple was found at the beginning!')
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
                #put lat/long back where it belongs, hard coded for first case only
            inputwaypoints[0][2] = [inputwaypoints[0][2][shortestpossibility]]
        elif foundmultiples[0] == len(inputwaypoints) - 1:
            print('One multiple was found at the end!')
            shortestdistance = float("inf") #establish worst case scenario so anything would be better
            possibility = 0
            for iter in inputwaypoints[foundmultiples[0]][2]:
                tryset = [[inputwaypoints[foundmultiples[0]-1][2][0], inputwaypoints[foundmultiples[0]][2][possibility]]]
                trydistance = vincenty.vincenty(inputwaypoints[foundmultiples[0]-1][2][0], inputwaypoints[foundmultiples[0]][2][possibility])
                if trydistance < shortestdistance:
                    shortestdistance = trydistance
                    shortestpossibility = possibility
                    shortestset = tryset
                possibility += 1
                #put lat/long back where it belongs
            inputwaypoints[foundmultiples[0]][2] = [inputwaypoints[foundmultiples[0]][2][shortestpossibility]]
        else:
            shortestdistance = float("inf") #establish worst case scenario so anything would be better
            possibility = 0
            print('Single multiple found in middle of route')
            for iter in inputwaypoints[foundmultiples[0]][2]:
                tryset = [[inputwaypoints[foundmultiples[0]-1][2][0], inputwaypoints[foundmultiples[0]][2][possibility], inputwaypoints[foundmultiples[0]+1][2][0]]]
                trydistance = vincenty.vincenty(inputwaypoints[foundmultiples[0]-1][2][0], inputwaypoints[foundmultiples[0]][2][possibility]) + vincenty.vincenty(inputwaypoints[foundmultiples[0]][2][possibility], inputwaypoints[foundmultiples[0]+1][2][0])
                if trydistance < shortestdistance:
                    shortestdistance = trydistance
                    shortestpossibility = possibility
                    shortestset = tryset
                possibility += 1
                #put lat/long back where it belongs
            inputwaypoints[foundmultiples[0]][2] = [inputwaypoints[foundmultiples[0]][2][shortestpossibility]]
            
    elif len(foundmultiples) > 1 and len(foundmultiples) < len(inputwaypoints): #some waypoints are multiples
        print('some waypoints are multiples')
    
    elif len(foundmultiples) == len(inputwaypoints): #all waypoints have multiples
        print('all waypoints are multiples, good luck')
    
    print(inputwaypoints)

    
#    possibilitymatrix = []  #fill with possiblities to try in waypointnumber, latlongnumber format
    
    #create consecutive group(s)    
    #how to figure out how many "groups" of multiples there are - are items in foundmultiples consecutive?
    #are these waypoints congruous or are there multiple sets?
    
#    position = 0
    
#    for waypoints in inputwaypoints:
#        if len(waypoints[2]) > 1: #multiple lat/long tuples were found in the list
     
#            print("Multiple items were found with name", waypoints[0], "...need more programming.")
#            print("Number of", waypoints[0], "lat/long possibilties:", len(waypoints[2]))
            
#            possibilitymatrix.append((position,(range(len(waypoints[2]))))) #this doesn't work well
            
#            print("Without further programming, first lat/long will be used.") #remove these when you make logic to do something with multiple lat/longs
            
#            position = position + 1
            
#        else:
#            position = position + 1
            
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


