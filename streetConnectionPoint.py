

class StreetConnectionPoint:
    id = 0

    def __init__(self, xCoordinate, yCoordinate, isProbabilitySettable=False):

        # id: define streetconnectionpoint's id
        # xCoordinate, yCoordinate: define the connection point's coordinate
        # isProbabilitySettable, determines whether this connectionpoint, if this connectionpoint have more
        #   than 1 outgoing street, can set probability, which influences the car to choose next street. For example,
        #   if there are 2 outgoing streets, man can set probability to 20% and 80%. Then the car choose next street
        #   with this probability


        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.incomingStreets = []
        self.outgoingStreets = []
        self.isProbabilitySettable = isProbabilitySettable
        self.turnProbabilities = []
        self.ischanged = False
        self.id = StreetConnectionPoint.id
        StreetConnectionPoint.id += 1

    def setIncomingStreet(self, incomingStreet):
        # set the streets, which flow into this connectionpoint
        self.incomingStreets.append(incomingStreet)

    def setOutgoingStreet(self, outgoingStreet):
        # set the streets, which flow out of this connectionpoint
        self.outgoingStreets.append(outgoingStreet)

    def isMerge(self):
        # A node is a merge in case it has more than one incoming street
        return ( len(self.incomingStreets) > 1 )

    def setProbabilities(self, probabilities):
        # sets the turn probabilities: The probability the car will drive on a specific street
        if self.isProbabilitySettable:
            self.turnProbabilities = probabilities
            print("Probabilities of Node " + str(self.id) + " updated.")
        else:
            print("You can not set custom probabilities on this node!")

    def getTurnProbabilites(self):
        # get the turn probabilities
        if not self.turnProbabilities:
            # Initialize all turnProbabilities to be equal
            for _ in range(len(self.outgoingStreets)):
                self.turnProbabilities.append(1 / len(self.outgoingStreets))
        return self.turnProbabilities






