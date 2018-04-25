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


class Possibility(object):

    def __init__(self, waypoint, originalposition, possibility, wasiambiguous=False):
        self.waypoint = waypoint
        self.originalposition = originalposition
        self.possibility = possibility
        self.wasiambiguous = wasiambiguous

    def getoriginalposition(self):
        return self.originalposition

    def getpossibility(self):
        return self.possibility

    def getwasiambiguous(self):
        return self.wasiambiguous

    def getwaypoint(self):
        return self.waypoint

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

    def getroute(self):
        return self.waypoints
