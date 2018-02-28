class Pointinspace(object):

    def __init__(self, identifier, coordinates):
        self.identifier = identifier
        self.coordinates = coordinates

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates

class Navaid(Pointinspace):

    def __init__(self, identifier, coordinates):
        Pointinspace.__init__(self, identifier, coordinates)
        self.typeelement = 'NAVAID'
        self.identifier = identifier
        self.coordinates = coordinates

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates

    def gettypeelement(self):
        return self.typeelement


class Ambiguouselement(object):

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)

    def getidentifier(self):
        return self.identifier

    def getpossibilities(self):
        return self.possibilities

#class Navaid(Pointinspace):
