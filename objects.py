class Pointinspace(object):

    def __init__(self, identifier, coordinates, typeelement, elementname=None):
        self.identifier = identifier
        self.coordinates = coordinates
        self.typeelement = typeelement
        self.elementname = elementname
        self.onairways = []

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

    def getairways(self):
        return self.onairways

    def addairway(self, airway):
        self.onairways.append(airway)

    def __str__(self):
        if self.elementname is not None:
            return (self.identifier + ' point-in-space ' + self.typeelement + ' ' + self.elementname +
                    ' coordinates: ' + str(self.coordinates) + ' on airways ' + str(self.onairways))
        else:
            return (self.identifier + ' point-in-space ' + self.typeelement + ' coordinates: ' + str(self.coordinates) +
                    ' on airways ' + str(self.onairways))


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
        return self.identifier + ' airport ' + self.elementname + ' coordinates: ' + str(self.coordinates)


class Ambiguouselement(object):  # consider changing to Ambiguouspoint?

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def addpossibility(self, possibility):
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?
        
    def howmanypossibilities(self):
        return len(self.possibilities)

    def getidentifier(self):
        return self.identifier
    
    def getpossibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def getpossibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous element with ' + str(len(self.possibilities)) + ' possibilities'


class TBWrapper(object):

    def __init__(self, waypoint, originalposition, wasambiguous=False, ambiguousid = None):
        self.waypoint = waypoint
        self.originalposition = originalposition
        self.wasambiguous = wasambiguous
        self.ambiguousid = ambiguousid

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

    def __str__(self):
        return ('TBWrapper original position: ' + str(self.originalposition) + ', ' + 'Wrapper ambiguous ID: ' +
                str(self.ambiguousid) + ', Wrapper contains: ' + str(self.waypoint))


class Route(object):

    def __init__(self):
        self.waypoints = []
        self.containsairway = False

    def addelement(self, element):
        self.waypoints.append(element)
        
    def getelement(self, element):
        return self.waypoints[element]
    
    def howmanyelements(self):
        return len(self.waypoints)

    def getlastelement(self):
        # return last element
        return self.waypoints[-1]

    def getfirstelement(self):
        # return first element
        return self.waypoints[0]

    def getcontainsairway(self):
        self.containsairway = False
        for element in self.waypoints:
            if type(element) is Airway or type(element) is Ambiguousairway:
                self.containsairway = True
                break
        return self.containsairway

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
        # must be Ambiguouselement at position
        self.waypoints[position] = self.waypoints[position].getpossibility(possibilitynumber)

    def getwaypoints(self):
        return self.waypoints

    def __str__(self):  # this doesnt work
        return str(self.waypoints)


class Airway(object):

    def __init__(self, airwayname):
        self.airwayname = airwayname
        self.uniqueid = 'testuniqueid'
        self.waypoints = []

    def addelement(self, element):
        self.waypoints.append(element)

    def setwaypoints(self, waypoints):
        self.waypoints = waypoints

    def getairwayname(self):
        return self.airwayname

    def getwaypoints(self):
        return self.waypoints

    def getelement(self, element):
        return self.waypoints[element]


class Ambiguousairway(object):
    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def addpossibility(self, possibility):
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?

    def howmanypossibilities(self):
        return len(self.possibilities)

    def getidentifier(self):
        return self.identifier

    def getpossibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def getpossibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self.possibilities)) + ' possibilities'
