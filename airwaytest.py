import atsreader
from objects import Airway

print('Running atsreader...')

atsreader.airwaydictmaker()

testwaypoints = atsreader.airwaydict['Q822'][0].getwaypoints()

print(testwaypoints)

for testwaypoint in testwaypoints:
    print(testwaypoint)
