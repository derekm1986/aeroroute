# This file parses the FAA's coded departure routes
# codedswap_db.csv file must be in routes directory

class CDR:
    def __init__(self, cdr_id, dep_airport, arr_airport, route):
        self._cdr_id = cdr_id
        self._dep_airport = dep_airport
        self._arr_airport = arr_airport
        self._route = route

    @property
    def cdr_id(self):
        return self._cdr_id
    
    @property
    def dep_airport(self):
        return self._dep_airport
    
    @property
    def arr_airport(self):
        return self._arr_airport
    
    @property
    def route(self):
        return self._route
    
    def __repr__(self):
        return f"CDR {self._cdr_id}, {self._dep_airport}, {self._arr_airport}, {self._route})"


def cdr_dict_maker():

    cdr_file = open("routes/codedswap_db.csv")

    cdr_dict = {}

    next(cdr_file)  # Skip the header line

    for line in cdr_file:
        
        current_line = line.rstrip().split(",")
        cdr_id = current_line[0]
        dep_airport = current_line[1]
        arr_airport = current_line[2]
        route = current_line[4]

        cdr_dict[cdr_id] = CDR(cdr_id, dep_airport, arr_airport, route)

    cdr_file.close()

    return cdr_dict


print(cdr_dict_maker())