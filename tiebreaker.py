#this file is for when a route item is returned with multiple lat/longs

import math
import vincenty
import pairmaker

def tiebreaker(inputwaypoints):

    shortestdistance = float("inf") #establish worst case scenario so anything would be better
    #shortestdistanceset = #combination of waypoints with shortest distance 
    
    print(inputwaypoints)
    
    foundmultiples = [i for i,x in enumerate(inputwaypoints) if len(x[2]) > 1]
    
    print('Found multiples at position(s):',foundmultiples)
    
    #how many waypoints with multiples?
    print("Number of total waypoints with multiples:",len(foundmultiples))
    
    if len(foundmultiples) == 1:
        print('Only one multiple found, using adjacent waypoint(s)')
        if foundmultiples[0] == 0:
            print('One multiple was found at the beginning!')
            possibility = 0
            for iter in inputwaypoints[0][2]:
                print(inputwaypoints[0][2][possibility], inputwaypoints[1][2][0], possibility)
                possibility = possibility + 1
        elif foundmultiples[0] == len(inputwaypoints) - 1:
            print('One multiple was found at the end!')
            possibility = 0
            for iter in inputwaypoints[foundmultiples[0]][2]:
                print(inputwaypoints[foundmultiples[0]-1][2][0], inputwaypoints[foundmultiples[0]][2][possibility], possibility)
                possibility = possibility + 1
        else:
            print('Single multiple found in the middle of the route...need more code!')
    
    if len(foundmultiples) == len(inputwaypoints):
        print('all waypoints are multiples, good luck')
    
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


