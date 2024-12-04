import nav_data_library as ndl

new_ndl = ndl.NavDataLibrary()

testitem1 = new_ndl.combined_dict['J4']

print(testitem1)

print(type(testitem1))

print(type(testitem1[1]))

print(len(testitem1))

testitem2 = new_ndl.combined_dict['KBOS']

print(type(testitem2))

print(testitem2)

print(type(testitem2[0]))

print(len(testitem2))

testitem3 = new_ndl.combined_dict['Q822']

print(type(testitem3))

print(testitem3)

print(type(testitem3[0]))

print(len(testitem3))