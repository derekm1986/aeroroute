from cdrreader import cdr_dict_maker

def cdr_finder_dep_arr(dep_airport, arr_airport):
    cdr_dict = cdr_dict_maker()
    result_list = []
    for key, val in cdr_dict.items():
        if dep_airport in val.dep_airport and arr_airport in val.arr_airport:
            result_list.append(val)
    return result_list

#print(cdr_finder_dep_arr("KBOS", "KCLE"))