import aeroroute
import cdrreader

# test aeroroute using all cdrs

cdr_dict = cdrreader.cdr_dict_maker()

print("got here")

for val in cdr_dict.values():
    print(aeroroute.aeroroute_input(val.route_string))
