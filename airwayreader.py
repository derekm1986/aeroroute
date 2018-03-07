# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in same directory

# need to finish

text_file = open("AIRAC/ATS.txt")

#airwayresult = []

thewholefile = text_file.read()

thewholefile = thewholefile.split("\n\n")  # this only works with Windows-formatted text files, splits data between two blank lines

airwaydict = {}

for airwaystring in thewholefile:
    tempitem = airwaystring.split()
    try:
        firstline = tempitem[0]  # this blows up when you reach the end of the file, hence the need for try/except
    except:
        break
    restofstring = tempitem[1:]
    
    firstline = firstline.split("|")
    airwayid = firstline[1]
    airwaydict.setdefault(airwayid, []).append((restofstring))  # want to put rest of airwaystring here

# airway dictionary is established,
    
for airwaysegment in airwaydict["Q822"][0]:
    airwaysegment = airwaysegment.split("|")
    del airwaysegment[0]  # deletes S at beginning of every line
    print(airwaysegment)    
    
#    if not line.strip():
#        continue
#    else:
#        airwayresult.append(line)



# for line in text_file:
#    if line.startswith(airwayinput + "|"):
#        line = line.rstrip()
#        line = line.split("|")
#       #navaidlat = line[6]
#       #navaidlong = line[7]
#       #navaidlatwithdecimal = navaidlat[:len(navaidlat)-6] + "." + navaidlat[len(navaidlat)-6:] #6 decimal places
#       #navaidlongwithdecimal = navaidlong[:len(navaidlong)-6] + "." + navaidlong[len(navaidlong)-6:] #6 decimal places
#       #navaidresult.append(navaidlatwithdecimal + " " + navaidlongwithdecimal)
    
# print airwayresult

text_file.close()
