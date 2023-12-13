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

    def add_airway(self, airway) -> None:
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

    def get_element_name(self) -> str | None:
        if self.elementname is not None:
            return self.elementname
        else:
            pass

    def __str__(self):
        return self.identifier + ' airport ' + self.elementname + ' coordinates: ' + str(self.coordinates)


class AmbiguousPoint(object):  # consider changing to Ambiguouspoint?

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def add_possibility(self, possibility) -> None:
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?
        
    def how_many_possibilities(self) -> int:
        return len(self.possibilities)

    def get_identifier(self) -> str:
        return self.identifier
    
    def get_possibility(self, possibility_number: int):
        return self.possibilities[possibility_number]

    def get_possibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous element with ' + str(len(self.possibilities)) + ' possibilities'


class TBWrapper(object):

    def __init__(self, waypoint, originalposition, wasambiguous=False, ambiguous_id=None):
        self.waypoint = waypoint
        self.originalposition = originalposition
        self.wasambiguous = wasambiguous
        self.ambiguous_id = ambiguous_id

    def set_ambiguous_id(self, ambiguous_id: int) -> None:
        assert self.wasambiguous is True
        self.ambiguous_id = ambiguous_id

    def get_was_ambiguous(self) -> bool:
        return self.wasambiguous

    def get_original_position(self) -> int:
        return self.originalposition

    def get_ambiguous_id(self) -> int:
        return self.ambiguous_id

    def get_waypoint(self):
        return self.waypoint

    def get_coordinates(self):
        assert type(self.waypoint) is not AmbiguousPoint
        return self.waypoint.get_coordinates()

    def __str__(self):
        return ('TBWrapper original position: ' + str(self.originalposition) + ', ' + 'Wrapper ambiguous ID: ' +
                str(self.ambiguous_id) + ', Wrapper contains: ' + str(self.waypoint))


class Route(object):

    def __init__(self):
        self.elements = []
        self.contains_airway = False
        self.contains_ambiguous_element = False

    def add_element(self, element) -> None:
        self.elements.append(element)
        
    def get_element(self, element):
        return self.elements[element]
    
    def how_many_elements(self) -> int:
        return len(self.elements)

    def get_last_element(self):
        # return last element
        return self.elements[-1]

    def get_first_element(self):
        # return first element
        return self.elements[0]

    def get_contains_airway(self) -> bool:
        self.contains_airway = False
        for element in self.elements:
            if type(element) is Airway or type(element) is AmbiguousAirway:
                self.contains_airway = True
                break
        return self.contains_airway

    def get_contains_ambiguous_element(self) -> bool:
        for element in self.elements:
            if type(element) is AmbiguousPoint:
                self.contains_ambiguous_element = True
                break
        return self.contains_ambiguous_element
    
    def get_possibility(self, position, possibilitynumber):
        # must be Ambiguouselement at position
        return self.elements[position].getpossibility(possibilitynumber)

    def get_possibilities(self, position):
        # must be Ambiguouselement at position
        return self.elements[position].getpossibilities()

    def deambiguate(self, position, possibilitynumber) -> None:
        # must be Ambiguouselement at position
        self.elements[position] = self.elements[position].get_possibility(possibilitynumber)

    def get_waypoints(self):
        return self.elements

    def __str__(self):  # this doesn't work
        return str(self.elements)


class Airway(object):

    def __init__(self, airwayname):
        self.airwayname = airwayname
        self.uniqueid = 'testuniqueid'
        self.waypoints = []

    def add_element(self, element) -> None:
        self.waypoints.append(element)

    def set_waypoints(self, waypoints) -> None:
        self.waypoints = waypoints

    def get_airway_name(self) -> str:
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

    def add_possibility(self, possibility) -> None:
        if type(possibility) is list:
            self.possibilities.extend(possibility)
        else:
            self.possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?

    def how_many_possibilities(self) -> int:
        return len(self.possibilities)

    def get_identifier(self) -> str:
        return self.identifier

    def get_possibility(self, possibilitynumber):
        return self.possibilities[possibilitynumber]

    def get_possibilities(self):
        return self.possibilities

    def __str__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self.possibilities)) + ' possibilities'
