import vincenty
import pairmaker

def distancefinder(input):
  
  sumdistance = 0.00  # establish sumdistance and put zero in it
  
  for pair in pairmaker.pairmaker(input):
    pairdistance = vincenty.vincenty(pair) # may need a *
    sumdistance += pairdistance
    
  return sumdistance
