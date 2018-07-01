class Pointinspace(object):

    def __init__(self, identifier, coordinates, typeelement, elementname=None):
        self.identifier = identifier
        self.coordinates = coordinates
        self.typeelement = typeelement
        self.elementname = elementname

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates

    def gettypeelement(self):
        return self.typeelement

    def getelementname(self):
        if self.elementname is not None:
            return self.elementname
        else:
            pass

    def __str__(self):
        return self.identifier + ' ' + self.typeelement + ' coordinates: ' + str(self.coordinates)


class Airport(object):

    def __init__(self, identifier, coordinates, elementname=None):
        self.identifier = identifier
        self.coordinates = coordinates
        self.typeelement = 'airport'
        self.elementname = elementname

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates

    def gettypeelement(self):
        return self.typeelement

    def getelementname(self):
        if self.elementname is not None:
            return self.elementname
        else:
            pass

    def __str__(self):
        return self.identifier + ' ' + self.elementname


class Ambiguouselement(object):

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)
        
    def howmanypossibilities(self):
        return len(self.possibilities)

    def getidentifier(self):
        return self.identifier
    
    def getpossibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def getpossibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous element'


class TBWrapper(object):

    def __init__(self, waypoint, originalposition, wasambiguous=False):
        self.waypoint = waypoint
        self.originalposition = originalposition
        self.wasambiguous = wasambiguous
        self.ambiguousid = None

    def setambiguousid(self, ambiguousid):
        assert self.wasambiguous is True
        self.ambiguousid = ambiguousid

    def getwasambiguous(self):
        return self.wasambiguous

    def getoriginalposition(self):
        return self.originalposition

    def getambiguousid(self):
        return self.ambiguousid

    def getwaypoint(self):
        return self.waypoint

    def getcoordinates(self):
        assert type(self.waypoint) is not Ambiguouselement
        return self.waypoint.getcoordinates()

    def printme(self):
        print('Wrapper original position:', self.originalposition, ',', 'Wrapper ambiguous ID:', self.ambiguousid, ',',
              'Wrapper contains:', self.waypoint)

class Route(object):

    def __init__(self):
        self.waypoints = []

    def addelement(self, element):
        self.waypoints.append(element)
        
    def getelement(self, element):
        return self.waypoints[element]
    
    def howmanyelements(self):
        return len(self.waypoints)
    
    def getcontainsambiguity(self):
        self.containsambiguity = False
        for element in self.waypoints:
            if type(element) is Ambiguouselement:
                self.containsambiguity = True
                break
        return self.containsambiguity
    
    def getpossibility(self, position, possibilitynumber):
        # must be Ambiguouselement at position
        return self.waypoints[position].getpossibility(possibilitynumber)

    def getpossibilities(self, position):
        # must be Ambiguouselement at position
        return self.waypoints[position].getpossibilities()

    def deambiguate(self, position, possibilitynumber):
        #must be Ambiguouselement at position
        self.waypoints[position] = self.waypoints[position].getpossibility(possibilitynumber)

    def getwaypoints(self):
        return self.waypoints

    def printme(self):
        print(self.waypoints)