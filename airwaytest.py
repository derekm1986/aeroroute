import atsreader
from objects import Airway

# make this more interactive to be more useful

print('Running atsreader...')

airwaydict = atsreader.airwaydictmaker()

print('atsreader.airwaydictmaker ran successfully')

testwaypoints = airwaydict['Q822'][0].getwaypoints()

print(testwaypoints)

for testwaypoint in testwaypoints:
    print(testwaypoint)
