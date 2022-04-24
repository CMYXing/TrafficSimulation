
# A street object that consists of multiple lanes (1 by default)
# We assume a street is straight, and connects to another street via connectionPoints
from math import sqrt

from pandas import np

from lane import Lane


class Street:
    id = 0

    def __init__(self, startConnectionPoint, endConnectionPoint, lanes = None, canSpawnCars = False, isTunnel=False):

        # id: define street's id
        # startConnectionPoint, endConnectionPoint: Define the street's start and end point (unit: pixel)
        # lanes: Determines how many parallel lanes in a street
        # canSpawnCars: Determines whether this street can spawn new cars
        # isTunnel: Determines whether this street is tunnel


        self.canSpawnCars = canSpawnCars

        self.startConnectionPoint = startConnectionPoint
        self.endConnectionPoint = endConnectionPoint

        self.startConnectionPoint.setOutgoingStreet(self)
        self.endConnectionPoint.setIncomingStreet(self)

        self.isTunnel = isTunnel

        if lanes is None:
            self.lanes = [Lane(self)]
        else:
            self.lanes = lanes

        self.id = Street.id

        Street.id += 1

    def spawnCar(self):
        # Add a new car on the lane
        if self.canSpawnCars:
            self.lanes[0].spawnCar()
            print("Spawned new car on street " + str(self.id) + ".")
        else:
            print("This street can't spawn cars.")

    def removeCar(self, car):
        # delete a car on the lane
        for lane in self.lanes:
            if car in lane.cars:
                lane.cars.remove(car)

    def getAllCars(self):
        # get all the cars on the street
        cars = []
        for lane in self.lanes:
            cars.extend(lane.cars)

        return cars

    def __getDeltaX(self):
        # get street's length, which is projected on x-axis (unit: pixel)
        return self.endConnectionPoint.xCoordinate - self.startConnectionPoint.xCoordinate

    def __getDeltaY(self):
        # get street's length, which is projected on y-axis (unit: pixel)
        return self.endConnectionPoint.yCoordinate - self.startConnectionPoint.yCoordinate

    def getLength(self):
        # get street's length (unit: pixel)
        deltaX = self.__getDeltaX()
        deltaY = self.__getDeltaY()
        return sqrt(deltaX**2 + deltaY**2)

    def getCoordinateAt(self, fractionOfDistance):
        # Returns the coordinate at a certain fraction of the distance of this street
        # for example fractionOfDistance=0.5 would return the coordinate of the center of this street
        # unit: pixel
        xCoordinate = self.startConnectionPoint.xCoordinate + fractionOfDistance * self.__getDeltaX()
        yCoordinate = self.startConnectionPoint.yCoordinate + fractionOfDistance * self.__getDeltaY()
        return xCoordinate, yCoordinate


    def getStreetVector(self):
        #Returns a vector of the length and direction of the street
        streetStartPoint = [self.startConnectionPoint.xCoordinate,
                            self.startConnectionPoint.yCoordinate]

        streetEndPoint = [self.endConnectionPoint.xCoordinate,
                          self.endConnectionPoint.yCoordinate]

        streetVector = np.array(streetEndPoint) - np.array(streetStartPoint)
        return streetVector

    def getNextStreets(self):
        # return the streets, on which the car can drive
        return self.endConnectionPoint.outgoingStreets

