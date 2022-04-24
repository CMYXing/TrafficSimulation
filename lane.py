import mathUtil
from car import Car
import numpy as np
from drawStreetNetwork import LANE_WIDTH


# A lane can hold cars that drive on it
class Lane:

    def __init__(self, street, cars = None):
        if cars is None:
            self.cars = []
        else:
            self.cars = cars

        self.street = street  # The lane must know the street it belongs to


    ## Spawn a car in the lane object
    def spawnCar(self):
        newCar = Car(self)
        self.cars.append(newCar)


    ## Return the start and end coordinates of the lane object
    def getStartAndEndPoint(self):
        streetVector = self.street.getStreetVector()
        lengthOfStreet = np.sqrt(np.abs(streetVector[0]) ** 2 + np.abs(streetVector[1]) ** 2)
        orthogonalNormalizedStreetVector = np.array(mathUtil.getOrthogonalVector(streetVector)) / lengthOfStreet

        laneIndex = self.street.lanes.index(self)
        streetWidth = len(self.street.lanes) * LANE_WIDTH

        streetStartPoint = np.array([self.street.startConnectionPoint.xCoordinate, self.street.startConnectionPoint.yCoordinate])
        streetEndPoint = np.array([self.street.endConnectionPoint.xCoordinate, self.street.endConnectionPoint.yCoordinate])

        lowerMostStartPoint = streetStartPoint - (streetWidth / 2 - LANE_WIDTH / 2) * orthogonalNormalizedStreetVector
        lowerMostEndPoint = streetEndPoint - (streetWidth / 2 - LANE_WIDTH / 2) * orthogonalNormalizedStreetVector

        # Shift the start and endpoints by the lane index
        laneStart = lowerMostStartPoint + laneIndex * orthogonalNormalizedStreetVector * LANE_WIDTH
        laneEnd = lowerMostEndPoint + laneIndex * orthogonalNormalizedStreetVector * LANE_WIDTH
        return laneStart, laneEnd


    ## Return the coordinate at a certain fraction of the distance of this street
    # e.g., fractionOfDistance=0.5 would return the coordinate of the center of this street
    def getCoordinateAt(self, fractionOfDistance):
        startPoint, endPoint = self.getStartAndEndPoint()
        xCoordinate = startPoint[0] + fractionOfDistance * self.__getDeltaX()
        yCoordinate = startPoint[1] + fractionOfDistance * self.__getDeltaY()
        return xCoordinate, yCoordinate


    ## Return the component of the lane object length in the horizontal coordinate
    def __getDeltaX(self):
        startPoint, endPoint = self.getStartAndEndPoint()
        return endPoint[0] - startPoint[0]


    ## Return the component of the lane object length in the vertical coordinate
    def __getDeltaY(self):
        startPoint, endPoint = self.getStartAndEndPoint()
        return endPoint[1] - startPoint[1]


    ## Return the length of the lane object
    def getLength(self):
        return np.sqrt(self.__getDeltaX()**2 + self.__getDeltaY()**2)