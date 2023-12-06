class NavDataLibrary(object):
    # trying to keep all the nav data in an object
    def __init__(self):
        self.points_in_space_dict = {}
        self.airway_dict = {}
        self.airport_dict = {}

    def add_airway_dict(self, airway_dict):
        # for testing only
        self.airway_dict = airway_dict

    def add_points_in_space_dict(self, points_in_space_dict):
        self.points_in_space_dict = points_in_space_dict

    def add_airport_dict(self, airport_dict):
        self.airport_dict = airport_dict

    def lookup_item(self, search_string):
        pass
