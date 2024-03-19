class Location:
    
    # trying to make this a super class from which all nav data objects inherit
    def __init__(self, identifier, coordinates, type_element):
        self._identifier = identifier
        self._coordinates = coordinates
        self._type_element = type_element

    @property
    def identifier(self):
        return self._identifier

    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def type_element(self):
        return self._type_element


class PointInSpace(Location):

    def __init__(self, identifier, coordinates, type_element, element_name=None):
        super().__init__(identifier, coordinates, type_element)
        self._element_name = element_name
        self._available_airways = []
        self._on_airway = None

    @property
    def element_name(self):
        return self._element_name
    
    @property
    def available_airways(self):
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


class Airport(Location):

    def __init__(self, identifier, coordinates, element_name=None):
        super().__init__(identifier, coordinates, 'airport')
        self._element_name = element_name

    @property
    def element_name(self) -> str | None:
        return self._element_name
    
    def __str__(self):
        return f"{self._identifier} *** airport * {self._element_name} * coordinates: {self._coordinates}"

    def __repr__(self):
        return f"{self._identifier} *** airport * {self._element_name} * coordinates: {self._coordinates}"


class AmbiguousPoint:

    def __init__(self, identifier, initial_possibility):
        self._identifier = identifier
        self._possibilities = [initial_possibility]

    def __iter__(self):
        for possibility in self._possibilities:
            yield possibility

    def add_possibility(self, possibility) -> None:
        if type(possibility) is list:
            self._possibilities.extend(possibility)
        else:
            self._possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?
        
    @property
    def num_possibilities(self) -> int:
        return len(self._possibilities)

    @property
    def identifier(self) -> str:
        return self._identifier
    
    def get_possibility(self, possibility_number: int):
        return self._possibilities[possibility_number]

    @property
    def possibilities(self):
        return self._possibilities

    def __str__(self):
        return self._identifier + ' ambiguous point with ' + str(len(self._possibilities)) + ' possibilities:\n' + \
                str(self._possibilities)

    def __repr__(self):
        return self._identifier + ' ambiguous point with ' + str(len(self._possibilities)) + ' possibilities:\n' + \
                str(self._possibilities)


class TBWrapper:
    # Tie Breaker wrapper, needed for deambiguatorbrute function
    def __init__(self, waypoint, original_position, was_ambiguous=False, ambiguous_id=None):
        self._waypoint = waypoint
        self._original_position = original_position
        self._was_ambiguous = was_ambiguous
        self._ambiguous_id = ambiguous_id

    @property
    def was_ambiguous(self) -> bool:
        return self._was_ambiguous

    @property
    def original_position(self) -> int:
        return self._original_position

    @property
    def ambiguous_id(self) -> int:
        return self._ambiguous_id

    @property
    def waypoint(self):
        return self._waypoint

    @property
    def coordinates(self):
        return self._waypoint.coordinates

    def __repr__(self):
        return ('TBWrapper original position: ' + str(self._original_position) + ', ' + 'Wrapper ambiguous ID: ' +
                str(self._ambiguous_id) + ', Wrapper contains: ' + str(self._waypoint))


class Route:

    def __init__(self):
        self._elements = []

    def add_element(self, element) -> None:
        # put smarts here to protect from:
        # starting/ending with an airway
        # airway next to another airway
        self._elements.append(element)

    def get_element(self, element: int):
        return self._elements[element]
    
    @property
    def num_elements(self) -> int:
        return len(self._elements)

    @property
    def first_element(self):
        # return first element
        return self._elements[0]

    @property
    def last_element(self):
        # return last element
        return self._elements[-1]

    @property
    def contains_airway(self) -> bool:
        for element in self._elements:
            if type(element) is Airway or type(element) is AmbiguousAirway:
                return True
        return False

    @property
    def contains_ambiguous_point(self) -> bool:
        for element in self._elements:
            if type(element) is AmbiguousPoint:
                return True
        return False
    
    @property
    def contains_ambiguous_airway(self) -> bool:
        for element in self._elements:
            if type(element) is AmbiguousAirway:
                return True
        return False
    
    def get_possibility(self, position: int, possibility_number: int) -> PointInSpace:
        # must be AmbiguousPoint at position
        return self._elements[position].get_possibility(possibility_number)

    #def get_possibilities(self, position: int): # not sure if I need this
    #    # must be AmbiguousPoint at position
    #    return self._elements[position].get_possibilities()

    def deambiguate(self, position: int, possibility_number: int) -> None:
        # must be AmbiguousPoint at position
        self._elements[position] = self._elements[position].get_possibility(possibility_number)

    @property
    def elements(self):
        return self._elements

    def __iter__(self):
        for element in self._elements:
            yield element

    def __str__(self):  # this doesn't work
        return str(self._elements)

    def __repr__(self):  # this doesn't work
        return str(self._elements)


class Airway:

    def __init__(self, identifier: str):
        self._identifier = identifier
        self._waypoints = []

    def add_waypoint(self, waypoint) -> None:
        self._waypoints.append(waypoint)

    def set_waypoints(self, waypoints) -> None:
        self._waypoints = waypoints

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def waypoints(self):
        return self._waypoints

    def get_waypoint(self, waypoint: int):
        return self._waypoints[waypoint]

    def get_segment(self, beginning, end):
        # to get a segment of the airway so it can be used in a Route, not finished yet!
        return None

    def __str__(self):
        return f"{self._identifier} airway with {len(self._waypoints)} points:\n{self._waypoints}"

    def __repr__(self):
        return f"{self._identifier} airway with {len(self._waypoints)} points:\n{self._waypoints}"


class AmbiguousAirway:
    def __init__(self, identifier: str, initial_possibility):
        self._identifier = identifier
        self._possibilities = [initial_possibility]

    def __iter__(self):
        for possibility in self._possibilities:
            yield possibility

    def add_possibility(self, possibility) -> None:
        if type(possibility) is list:
            self._possibilities.extend(possibility)
        else:
            self._possibilities.append(possibility)
        # should this be .extend instead of append in case I get passed a list?

    @property
    def num_possibilities(self) -> int:
        return len(self._possibilities)

    @property
    def identifier(self) -> str:
        return self._identifier

    def get_possibility(self, possibility_number: int):
        return self._possibilities[possibility_number]

    @property
    def possibilities(self):
        return self._possibilities

    def __str__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self._possibilities)) + ' possibilities:\n' + \
                str(self._possibilities)

    def __repr__(self):
        return self.identifier + ' ambiguous airway with ' + str(len(self._possibilities)) + ' possibilities:\n' + \
                str(self._possibilities)


class Coordinates:
    # store coordinates here - validation checker may have to exist outside of this class - how could an instance return itself as none?
    def __init__(self, latitude: str, longitude: str):
        #force latitude between these two numbers
        if float(latitude) < -90.0 or float(latitude) > 90.0:
            raise TypeError
        #force longitude between these two numbers
        if float(longitude) < -180.0 or float(longitude) > 180.0:
            raise TypeError
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


class AirwayInRoute:
    # this is to store a segment of an airway while it's in a route
    def __init__(self, identifier, waypoints=[]):
        self._identifier = identifier
        self._waypoints = waypoints

    @property
    def identifier(self):
        return self._identifier

    @property
    def waypoints(self):
        return self._waypoints
