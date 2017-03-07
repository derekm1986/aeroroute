#this file is for when a route item is returned with multiple lat/longs

import math

def tiebreaker(inputwaypoints):

    shortestdistance = float("inf") #establish worst case scenario so anything would be better
    #shortestdistanceset = #combination of waypoints with shortest distance 
    
    print(inputwaypoints)
    
    foundmultiples = [i for i,x in enumerate(inputwaypoints) if type(x[2]) is list]
    
    #how many waypoints with multiples?
    print("Number of total waypoints with multiples:",len(foundmultiples))
    
    print("Found multiples at position(s):",foundmultiples)
    
    possibilitymatrix = []  #fill with possiblities to try in waypointnumber, latlongnumber format
    
    #how to figure out how many "groups" of multiples there are - are items in foundmultiples consecutive?
    #are these waypoints congruous or are there multiple sets?
    
    position = 0
    
    for waypoints in inputwaypoints:
        if type(waypoints[2]) is list: #multiple lat/long tuples were found in a list
     
            print("Multiple items were found with name", waypoints[0], "...need more programming.")
            print("Number of", waypoints[0], "lat/long possibilties:", len(waypoints[2]))
            
            possibilitymatrix.append((position,(range(len(waypoints[2]))))) #this doesn't work well
            
            waypoints[2] = waypoints[2][0] #remove these when you make logic to do something with multiple lat/longs
            print("Without further programming, first lat/long will be used.") #remove these when you make logic to do something with multiple lat/longs
            
            position = position + 1
            
        else:
            position = position + 1
            
    numberofpossibilities = 1        
            
    if len(possibilitymatrix) == 0:
        pass
    elif len(possibilitymatrix) == 1:
        numberofpossibilities = len(possibilitymatrix[0][1])
    else:
        for waypoints in possibilitymatrix:
            numberofpossibilities = numberofpossibilities * len(waypoints[1])

    print(possibilitymatrix)
    print("Number of possibilities:", numberofpossibilities)


    return inputwaypoints


