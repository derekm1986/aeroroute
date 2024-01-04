class PointInSpace:

    def __init__(self, identifier, coordinates, type_element, element_name=None):
        self._identifier = identifier
        self._coordinates = coordinates
        self._type_element = type_element
        self._element_name = element_name
        self._available_airways = []
        self._on_airway = None

    def get_identifier(self):
        return self._identifier

    #@property
    #def identifier(self):
    #    return self._identifier

    def get_coordinates(self):
        return self._coordinates

    def get_type_element(self):
        return self._type_element

    def get_element_name(self):
        if self._element_name is not None:
            return self._element_name
        else:
            pass

    def get_available_airways(self):
        return self._available_airways

    def add_available_airway(self, airway) -> None:
        self._available_airways.append(airway)

    def __str__(self):
        return_string = f"{self._identifier} *** {self._type_element}"

        if self._element_name is not None:
            return_string += f" * {self._element_name}"

        return_string += f" * coordinates: {self._coordinates}"

        if self._available_airways:
            return_string += f" * available airways: {self._available_airways}"

        return return_string

    def __repr__(self):
        return_string = f"{self._identifier} *** {self._type_element}"

        if self._element_name is not None:
            return_string += f" * {self._element_name}"

        return_string += f" * coordinates: {self._coordinates}"

        if self._available_airways:
            return_string += f" * available airways: {self._available_airways}"

        return return_string


class Airport:

    def __init__(self, identifier, coordinates, element_name=None):
        self._identifier = identifier
        self._coordinates = coordinates
        self._type_element = 'airport'
        self._element_name = element_name

    def get_identifier(self):
        return self._identifier

    def get_coordinates(self):
        return self._coordinates

    def get_type_element(self):
        return self._type_element

    def get_element_name(self) -> str | None:
        if self._element_name is not None:
            return self._element_name
        else:
            pass

    def __str__(self):
        return f"{self._identifier} *** airport * {self._element_name} * coordinates: {self._coordinates}"

    def __repr__(self):
        return f"{self._identifier} *** airport * {self._element_name} * coordinates: {self._coordinates}"


class AmbiguousPoint:

    def __init__(self, identifier, initial_possibility):
        self.identifier = identifier
        self.possibilities = [initial_possibility]

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
        return self.identifier + ' ambiguous point with ' + str(len(self.possibilities)) + ' possibilities:\n' + \
                str(self.possibilities)

    def __repr__(self):
        return self.identifier + ' ambiguous point with ' + str(len(self.possibilities)) + ' possibilities:\n' + \
                str(self.possibilities)


class TBWrapper:

    def __init__(self, waypoint, original_position, was_ambiguous=False, ambiguous_id=None):
        self.waypoint = waypoint
        self.original_position = original_position
        self.was_ambiguous = was_ambiguous
        self.ambiguous_id = ambiguous_id

    def set_ambiguous_id(self, ambiguous_id: int) -> None:
        assert self.was_ambiguous is True
        self.ambiguous_id = ambiguous_id

    def get_was_ambiguous(self) -> bool:
        return self.was_ambiguous

    def get_original_position(self) -> int:
        return self.original_position

    def get_ambiguous_id(self) -> int:
        return self.ambiguous_id

    def get_waypoint(self):
        return self.waypoint

    def get_coordinates(self):
        assert type(self.waypoint) is not AmbiguousPoint
        return self.waypoint.get_coordinates()

    def __str__(self):
        return ('TBWrapper original position: ' + str(self.original_position) + ', ' + 'Wrapper ambiguous ID: ' +
                str(self.ambiguous_id) + ', Wrapper contains: ' + str(self.waypoint))


class Route:

    def __init__(self):
        self.elements = []

    def add_element(self, element) -> None:
        # put smarts here to protect from:
        # starting/ending with an airway
        # airway next to another airway
        self.elements.append(element)

    def get_element(self, element: int):
        return self.elements[element]
    
    def how_many_elements(self) -> int:
        return len(self.elements)

    def get_first_element(self):
        # return first element
        return self.elements[0]

    def get_last_element(self):
        # return last element
        return self.elements[-1]

    def get_contains_airway(self) -> bool:
        for element in self.elements:
            if type(element) is Airway or type(element) is AmbiguousAirway:
                return True
        return False

    def get_contains_ambiguous_point(self) -> bool:
        for element in self.elements:
            if type(element) is AmbiguousPoint:
                return True
        return False
    
    def get_possibility(self, position: int, possibility_number: int) -> PointInSpace:
        # must be AmbiguousPoint at position
        return self.elements[position].get_possibility(possibility_number)

    def get_possibilities(self, position: int):
        # must be AmbiguousPoint at position
        return self.elements[position].get_possibilities()

    def deambiguate(self, position: int, possibility_number: int) -> None:
        # must be AmbiguousPoint at position
        self.elements[position] = self.elements[position].get_possibility(possibility_number)

    def get_waypoints(self):
        return self.elements

    def __str__(self):  # this doesn't work
        return str(self.elements)

    def __repr__(self):  # this doesn't work
        return str(self.elements)


class Airway:

    def __init__(self, airway_name: str):
        self.airway_name = airway_name
        self.uniqueid = 'testuniqueid'
        self.waypoints = []

    def add_element(self, element) -> None:
        self.waypoints.append(element)

    def set_waypoints(self, waypoints) -> None:
        self.waypoints = waypoints

    def get_airway_name(self) -> str:
        return self.airway_name

    def get_waypoints(self):
        return self.waypoints

    def get_element(self, element):
        return self.waypoints[element]

    def __str__(self):
        return f"{self.airway_name} airway with {len(self.waypoints)} points:\n{self.waypoints}"

    def __repr__(self):
        return f"{self.airway_name} airway with {len(self.waypoints)} points:\n{self.waypoints}"


class AmbiguousAirway:
    def __init__(self, identifier: str, initial_possibility):
        self.identifier = identifier
        self.possibilities = [initial_possibility]

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
        return self.identifier + ' ambiguous airway with ' + str(len(self.possibilities)) + ' possibilities:\n' + \
                str(self.possibilities)

    def __repr__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self.possibilities)) + ' possibilities:\n' + \
                str(self.possibilities)


class Coordinates:
    # store coordinates here - validation checker may have to exist outside of this class - how could an instance return itself as none?
    # would assertions be most appropriate here?
    def __init__(self, latitude: str, longitude: str):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    def __eq__(self, other):
        return self._latitude == other.latitude and self._longitude == other.longitude

    def __repr__(self):
        return self._latitude + ", " + self._longitude


class AirwaySegment:
    # this is to store a segment of an airway while it's in a route
    pass

