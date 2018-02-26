print('this should not execute')

class Pointinspace(object):

    def __init__(self, identifier, coordinates):
        self.identifier = identifier
        self.coordinates = coordinates

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates


print('this should not execute either')  #for testing

class Ambiguouselement(object):

    def __init__(self, identifier, possibilities=None):
        if possibilities is None:
            possibilities = []
        self.identifier = identifier
        self.possibilities = possibilities

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)

    def getidentifier(self):
        return self.identifier

    def getpossibilities(self):
        return self.possibilities

#class Navaid(Pointinspace):
