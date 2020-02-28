# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in AIRAC directory

# need to finish

from objects import Airway

def airwaydictmaker():
    print('   ***airwaydictmaker was called***')

    ats_file = open("AIRAC/ATS.txt")

    global airwaydict

    airwaydict = {}

    for line in ats_file:

        if line.startswith("A"):
            currentline = line.rstrip().split("|")
            routeid = currentline[1]
            
            currentairway = Airway(routeid)
            
            print(routeid) # for testing
            
            ################################ move this stuff down?###################
            
            #if routeid not in airwaydict:
            #    airwaydict[routeid] = [Airway(routeid)]
            #else:  # routeid already in airwaydict
                
            #    print("routeid alrady in airwaydict, trying to append", airwaydict[routeid], type(airwaydict[routeid])) # for testing
                
            #    airwaydict[routeid].append(Airway(routeid))

            #########################################################################
            
        elif line.startswith("S"):
            currentline = line.rstrip().split("|")
            firstid = currentline[1]
            firstlat = currentline[2]
            firstlong = currentline[3]
            secondid = currentline[4]
            secondlat = currentline[5]
            secondlong = currentline[6]
            
            print(firstid, firstlat, firstlong, secondid, secondlat, secondlong) # for testing

            currentairway.addelement(firstid)
            
    print(currentairway) # for testing
    
    print(airwaydict) # for testing

    #do stuff here

    ats_file.close()


#def airportdictmaker():

#    airport_file = open("AIRAC/Airports.txt")

#    global airportdict

#    airportdict = {}

#    for line in airport_file:
#        if line.startswith("A"):
#            linefirstletter, airportid, airportname, airportlat, airportlong, airportelevation = line.rstrip().split("|")

#            airportlatisnegative = False  # establish variable

#           if airportlat.startswith("-"):
#                airportlatisnegative = True
#                airportlat = airportlat[1:]

            #if len(airportlat) < 7:
#                airportlat = "0" * (7 - len(airportlat)) + airportlat

#            airportlatwithdecimal = airportlat[:len(airportlat)-6] + "." + airportlat[len(airportlat)-6:]  # 6 decimal places

#            if airportlatisnegative is True:
 #               airportlatwithdecimal = "-" + airportlatwithdecimal

  #          airportlongisnegative = False  # establish variable

   #         if airportlong.startswith("-"):
   #             airportlongisnegative = True
    #            airportlong = airportlong[1:]

     #       if len(airportlong) < 7:
#                airportlong = "0" * (7 - len(airportlong)) + airportlong
#
 #           airportlongwithdecimal = airportlong[:len(airportlong)-6] + "." + airportlong[len(airportlong)-6:]  # 6 decimal places
#
  #          if airportlongisnegative is True:
   #             airportlongwithdecimal = "-" + airportlongwithdecimal

    #        airportobj = Airport(airportid, (airportlatwithdecimal, airportlongwithdecimal), airportname)

     #       airportdict[airportid] = airportobj

    #airport_file.close()







#airwayresult = []

#thewholefile = text_file.read()

#thewholefile = thewholefile.split("\n\n")  # this only works with Windows-formatted text files, splits data between two blank lines

#airwaydict = {}

#for airwaystring in thewholefile:
#    tempitem = airwaystring.split()
#    try:
#        firstline = tempitem[0]  # this blows up when you reach the end of the file, hence the need for try/except
#    except:
#        break
#    restofstring = tempitem[1:]
    
#    firstline = firstline.split("|")
#    airwayid = firstline[1]
#    airwaydict.setdefault(airwayid, []).append((restofstring))  # want to put rest of airwaystring here

# airway dictionary is established,
    
#for airwaysegment in airwaydict["Q822"][0]:
#    airwaysegment = airwaysegment.split("|")
#    del airwaysegment[0]  # deletes S at beginning of every line
#    print(airwaysegment)
    
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

    #text_file.close()
