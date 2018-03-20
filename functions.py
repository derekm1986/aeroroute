import vincenty


def pairmaker(inputwaypoints):

    i = 0

    while i <= (len(inputwaypoints) - 2):  # make pairs of each waypoint and the waypoint after it
        pair = [inputwaypoints[i], inputwaypoints[i + 1]]
        i += 1
        yield pair


def distancefinder(input):
  
  sumdistance = 0.00  # establish sumdistance and put zero in it
  
  for pair in pairmaker(input):
    pairdistance = vincenty.vincenty(*pair)
    sumdistance += pairdistance
    
  return sumdistance
