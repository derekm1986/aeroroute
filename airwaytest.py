import atsreader
import navaidsreader
import waypointsreader
import functions
import airwaymatcher
from objects import Airway

# make this more interactive to be more useful

print('   Loading NAVAIDs into memory...', end="")
navaiddict = navaidsreader.navaid_dict_maker()
print('OK')  # loading NAVAIDs was successful

print('   Loading elements into memory...', end="")
waypointdict = waypointsreader.waypoint_dict_maker()
print('OK')  # loading elements was successful

print('   Combining NAVAID and elements dictionaries...', end="")
pointsinspacedict = functions.points_in_space_dict_combiner(navaiddict, waypointdict)
print("OK")  # dictionary combination was successful


print('Calling atsreader.airwaydictmaker...')

airwaydict = atsreader.airwaydict_maker()

print('atsreader.airwaydictmaker returned')

#print(airwaydict)

airwaymatcher.airway_matcher(airwaydict, pointsinspacedict)

inputstring = input("Enter airway: ")

inputstring = inputstring.upper()

testwaypoints = airwaydict[inputstring][0].get_waypoints()

print(testwaypoints)

for testwaypoint in testwaypoints:
    print(testwaypoint)
