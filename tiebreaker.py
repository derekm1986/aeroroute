#this file is for when a route item is returned with multiple lat/longs

def tiebreaker(inputwaypoints):

    shortestdistance = 999999.0 #establish worst case scenario so anything would be better
    #shortestdistanceset = #combination of waypoints with shortest distance 
    
    foundmultiples = [i for i,x in enumerate(inputwaypoints) if type(x[2]) is list]
    
    print foundmultiples
    
    for waypoints in inputwaypoints:
        if type(waypoints[2]) is list: #multiple lat/long tuples were found in a list

    ###################################        
            print "Multiple items were found with name", waypoints[0], "...need more programming.  Without further programming, first lat/long will be used."
            waypoints[2] = waypoints[2][0] #remove these when you make logic to do something with multiple lat/longs
    ###################################
    
    #how many waypoints with multiples?
    print len(foundmultiples)
    
    #are these waypoints congruous or are there multiple sets?

    return inputwaypoints


