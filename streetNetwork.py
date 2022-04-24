
# A street network consists of different streets
import random


class StreetNetwork:
    def __init__(self, streets):

        # streets: consititute the streetnetwork
        # spawningStreets: the street set, which can spawn new car
        # routeUpdate: determine whether the car's route is updated

        self.streets = streets
        self.spawningStreets = []
        self.routeUpdate = False

        # Check all streets that can spawn cars
        for street in self.streets:
            if street.canSpawnCars:
                self.spawningStreets.append(street)

        self.customProbabilityNodes = []
        # Check all end nodes for the ability to set custom turn probabilities
        for street in self.streets:
            if street.endConnectionPoint.isProbabilitySettable:
                if street.endConnectionPoint not in self.customProbabilityNodes:
                    self.customProbabilityNodes.append(street.endConnectionPoint)


        if not self.spawningStreets:
            print("There must always be at least one spawning street! Please set up the StreetNetwork with a spawning street.")
        else:
            print("Street network " + str(self) + " initialized.\n Contains " + str(len(self.streets)) +
                  " streets, " + str(len(self.spawningStreets)) + " of them are spawning streets.")



    def getAllCars(self):
        # return all the cars in streetnetwork
        allCarsInStreetNetwork = []
        for street in self.streets:
            allCarsInStreetNetwork.extend(street.getAllCars())

        return allCarsInStreetNetwork

    def spawnCar(self):
        # Spawns a car at any of the spawning streets in the network
        for street in self.spawningStreets:
            street.spawnCar()

    def getAllNodesWhereProbabilityCanBeCustomized(self):
        # return all the nodes that can customize the car's turn probability
        return self.customProbabilityNodes
