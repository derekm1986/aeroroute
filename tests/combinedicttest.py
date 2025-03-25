import nav_data_library as ndl

new_ndl = ndl.NavDataLibrary()

testitem1 = new_ndl.combined_dict['J4']

print("test 1", testitem1)

print("test 2", type(testitem1))

print("test 3", type(testitem1[1]))

print("test 4", len(testitem1))

testitem2 = new_ndl.combined_dict['KBOS']

print("test 5", type(testitem2))

print("test 6", testitem2)

print("test 7", type(testitem2[0]))

print("test 8", len(testitem2))

testitem3 = new_ndl.combined_dict['Q822']

print("test 9", type(testitem3))

print("test 10", testitem3)

print("test 11", type(testitem3[0]))

print("test 12", len(testitem3))

# is every entry a list?
list_detector = False
for val in new_ndl.combined_dict.values():
    if not type(val) == list:
        list_detector - True

print("test 13", list_detector)
