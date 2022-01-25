import atsreader
from objects import Airway

# make this more interactive to be more useful

print('Running atsreader...')

atsreader.airwaydictmaker()

print('atsreader ran successfully')

testwaypoints = atsreader.airwaydict['Q822'][0].getwaypoints()

print(testwaypoints)

for testwaypoint in testwaypoints:
    print(testwaypoint)
