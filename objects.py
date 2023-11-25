class PointInSpace(object):

    def __init__(self, identifier, coordinates, typeelement, elementname=None):
        self.identifier = identifier
        self.coordinates = coordinates
        self.typeelement = typeelement
        self.elementname = elementname
        self.onairways = []

    def get_identifier(self):
        return self.identifier

    def get_coordinates(self):
        return self.coordinates

    def get_type_element(self):
        return self.typeelement

    def get_element_name(self):
        if self.elementname is not None:
            return self.elementname
        else:
            pass

    def get_airways(self):
        return self.onairways

    def add_airway(self, airway):
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

    def get_identifier(self):
        return self.identifier

    def get_coordinates(self):
        return self.coordinates

    def get_type_element(self):
        return self.typeelement

    def get_element_name(self):
        if self.elementname is not None:
            return self.elementname
        else:
            pass

    def __str__(self):
        return self.identifier + ' airport ' + self.elementname + ' coordinates: ' + str(self.coordinates)


class AmbiguousElement(object):  # consider changing to Ambiguouspoint?

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def add_possibility(self, possibility):
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?
        
    def how_many_possibilities(self):
        return len(self.possibilities)

    def get_identifier(self):
        return self.identifier
    
    def get_possibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def get_possibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous element with ' + str(len(self.possibilities)) + ' possibilities'


class TBWrapper(object):

    def __init__(self, waypoint, originalposition, wasambiguous=False, ambiguousid=None):
        self.waypoint = waypoint
        self.originalposition = originalposition
        self.wasambiguous = wasambiguous
        self.ambiguousid = ambiguousid

    def set_ambiguous_id(self, ambiguousid):
        assert self.wasambiguous is True
        self.ambiguousid = ambiguousid

    def get_was_ambiguous(self):
        return self.wasambiguous

    def get_original_position(self):
        return self.originalposition

    def get_ambiguous_id(self):
        return self.ambiguousid

    def get_waypoint(self):
        return self.waypoint

    def get_coordinates(self):
        assert type(self.waypoint) is not AmbiguousElement
        return self.waypoint.get_coordinates()

    def __str__(self):
        return ('TBWrapper original position: ' + str(self.originalposition) + ', ' + 'Wrapper ambiguous ID: ' +
                str(self.ambiguousid) + ', Wrapper contains: ' + str(self.waypoint))


class Route(object):

    def __init__(self):
        self.waypoints = []
        self.containsairway = False

    def add_element(self, element):
        self.waypoints.append(element)
        
    def get_element(self, element):
        return self.waypoints[element]
    
    def how_many_elements(self):
        return len(self.waypoints)

    def get_last_element(self):
        # return last element
        return self.waypoints[-1]

    def get_first_element(self):
        # return first element
        return self.waypoints[0]

    def get_contains_airway(self):
        self.containsairway = False
        for element in self.waypoints:
            if type(element) is Airway or type(element) is AmbiguousAirway:
                self.containsairway = True
                break
        return self.containsairway

    def get_contains_ambiguity(self):
        self.containsambiguity = False
        for element in self.waypoints:
            if type(element) is AmbiguousElement:
                self.containsambiguity = True
                break
        return self.containsambiguity
    
    def get_possibility(self, position, possibilitynumber):
        # must be Ambiguouselement at position
        return self.waypoints[position].getpossibility(possibilitynumber)

    def get_possibilities(self, position):
        # must be Ambiguouselement at position
        return self.waypoints[position].getpossibilities()

    def deambiguate(self, position, possibilitynumber):
        # must be Ambiguouselement at position
        self.waypoints[position] = self.waypoints[position].get_possibility(possibilitynumber)

    def get_waypoints(self):
        return self.waypoints

    def __str__(self):  # this doesn't work
        return str(self.waypoints)


class Airway(object):

    def __init__(self, airwayname):
        self.airwayname = airwayname
        self.uniqueid = 'testuniqueid'
        self.waypoints = []

    def add_element(self, element):
        self.waypoints.append(element)

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints

    def get_airway_name(self):
        return self.airwayname

    def get_waypoints(self):
        return self.waypoints

    def get_element(self, element):
        return self.waypoints[element]


class AmbiguousAirway(object):
    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def add_possibility(self, possibility):
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?

    def how_many_possibilities(self):
        return len(self.possibilities)

    def get_identifier(self):
        return self.identifier

    def get_possibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def get_possibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self.possibilities)) + ' possibilities'
