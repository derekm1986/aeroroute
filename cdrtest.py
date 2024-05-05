import sys

# Add the aeroroute directory to the system path
sys.path.append('../aeroroutesrc')

<<<<<<< Updated upstream
from aeroroute import cdrreader
=======
print(sys.path)

import cdrreader
>>>>>>> Stashed changes

# test aeroroute using all cdrs

cdr_dict = cdrreader.cdr_dict_maker()

for val in cdr_dict.values():
    #print(aeroroute.aeroroute_input(val.route_string))
    print(val.cdr_id, val.distance)
