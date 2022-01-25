import atsreader
from objects import Airway

# make this more interactive to be more useful

print('Calling atsreader.airwaydictmaker...')

airwaydict = atsreader.airwaydictmaker()

print('atsreader.airwaydictmaker ran')

testwaypoints = airwaydict['Q822'][0].getwaypoints()

print(testwaypoints)

for testwaypoint in testwaypoints:
    print(testwaypoint)
