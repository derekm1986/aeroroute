# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in AIRAC directory

# need to finish

from objects import Airway

def airwaydictmaker():
    print('   ***airwaydictmaker was called***')

    ats_file = open("AIRAC/ATS.txt")

    global airwaydict

    airwaydict = {}

    lastsecondid = None

    contents = ats_file.read()

    paragraphs = contents.split("\n\n")
    #  each paragraph should be an airway

    #  remove blank strings that will occur at end of list
    while ("" in paragraphs):
        paragraphs.remove("")

    splitparagraphs = []

    for paragraph in paragraphs:
        splitparagraphs.append(paragraph.split('\n'))
    #  each split paragraph is an airway with lines in a list

#    print(splitparagraphs)

    for splitparagraph in splitparagraphs:

        for line in splitparagraph:

            if line.startswith("A"):  #  this is the beginning of an airway
                currentline = line.rstrip().split("|")
                routeid = currentline[1]

                currentairway = Airway(routeid)

                airwaylist = []

            elif line.startswith("S"):

                currentline = line.rstrip().split("|")
                firstid = currentline[1]
                firstlat = currentline[2]
                firstlong = currentline[3]
                secondid = currentline[4]
                secondlat = currentline[5]
                secondlong = currentline[6]

                firstwaypoint = [firstid, firstlat, firstlong]
                secondwaypoint = [secondid, secondlat, secondlong]

#                print(firstwaypoint, secondwaypoint) #  for testing

                if firstwaypoint not in airwaylist:
                    airwaylist.append(firstwaypoint)

                if secondwaypoint not in airwaylist:
                    airwaylist.append(secondwaypoint)

#        print(airwaylist)

        currentairway.addelement(airwaylist)
                #  is this in the right place?



        if routeid in airwaydict:
            airwaydict[routeid].append(currentairway)
        else:
            airwaydict[routeid] = [currentairway]

        print('current route is ' + routeid) # for testing
        print('airwaynamefrom object is ' + currentairway.getairwayname())  # for testing


    
    print(airwaydict) # for testing

    #do stuff here

#    print(airwaydict['UV456']) # for testing

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
