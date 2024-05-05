#from cdrreader import cdr_dict_maker
<<<<<<< Updated upstream
from aeroroute.cdrreader import cdr_dict_maker

=======
from cdrreader import cdr_dict_maker
>>>>>>> Stashed changes


def cdr_finder_dep_arr(dep_airport, arr_airport):
    cdr_dict = cdr_dict_maker()
    result_list = []
    for key, val in cdr_dict.items():
        if dep_airport in val.dep_airport and arr_airport in val.arr_airport:
            result_list.append(val)
    result_list = sorted(result_list, key=lambda x: x.distance)

    return result_list
