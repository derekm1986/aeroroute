# This file parses the FAA's coded departure routes
# codedswap_db.csv file must be in routes directory


def cdr_dict_maker():

    cdr_file = open("routes/codedswap_db.csv")

    cdr_dict = {}

    for line in cdr_file:
        
        current_line = line.rstrip().split(",")
        cdr_id = current_line[0]
        dep_airport = current_line[1]
        arr_airport = current_line[2]
        route = current_line[4]

        cdr_dict[cdr_id] = (dep_airport, arr_airport, route)

    cdr_file.close()

    return cdr_dict


print(cdr_dict_maker())