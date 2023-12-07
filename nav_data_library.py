import airportsreader
import navaidsreader
import waypointsreader
import atsreader


class NavDataLibrary(object):
    # trying to keep all the nav data in an object
    def __init__(self):
        print('   OBJLoading airports into memory...', end="")
        self.airport_dict = airportsreader.airport_dict_maker()
        print('OK')  # loading airports was successful

        print('   OBJLoading NAVAIDs into memory...', end="")
        self.navaid_dict = navaidsreader.navaid_dict_maker()
        print('OK')  # loading NAVAIDs was successful

        print('   OBJLoading waypoints into memory...', end="")
        self.waypoint_dict = waypointsreader.waypoint_dict_maker()
        print('OK')  # loading elements was successful

        print('   OBJLoading airways into memory...', end="")
        self.airway_dict = atsreader.airway_dict_maker()
        print('OK')  # loading airways was successful

    def add_airport_dict(self, airport_dict):
        self.airport_dict = airport_dict

    def lookup_item(self, search_string):
        pass
