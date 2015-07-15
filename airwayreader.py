# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in same directory

#need to finish

text_file = open("ATS.txt")

airwayinput = raw_input("Enter identifier for airway: ")

airwayresult = []

for line in text_file:
    if line.startswith(airwayinput + "|"):
        line = line.rstrip()
        line = line.split("|")
        #navaidlat = line[6]
        #navaidlong = line[7]
        #navaidlatwithdecimal = navaidlat[:len(navaidlat)-6] + "." + navaidlat[len(navaidlat)-6:] #6 decimal places
        #navaidlongwithdecimal = navaidlong[:len(navaidlong)-6] + "." + navaidlong[len(navaidlong)-6:] #6 decimal places
        #navaidresult.append(navaidlatwithdecimal + " " + navaidlongwithdecimal)
    
print airwayresult

text_file.close()