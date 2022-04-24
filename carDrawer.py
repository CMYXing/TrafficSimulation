from carIllustration import CarIllustration



class CarDrawer:
    def __init__(self, cars, canvas):
        self.cars = cars
        self.carIllustrations = []
        self.canvas = canvas


    ##  initialize carIllustration list, purpose is to display the Car object in the animation
    def initializeCars(self):
        self.carIllustrations = []
        for car in self.cars:  # every car in the list cars should be displayed
            self.carIllustrations.append(CarIllustration(car, self.canvas))


########################################START OF MOVE CARS########################################
##################################################################################################

    ## Updates the car drawings.
    # The 'cars' list should contain all cars that need to be drawn.
    def moveCars(self, cars):
        if set(self.cars) != set(cars):
            # This means the new list of cars differs from the old list
            # First check which cars are new
            for car in cars:
                if car not in self.cars:
                    self.__addNewCar(car)

            # Now check which cars have been removed from the 'old' list - these are the cars that exited
            for oldCar in self.cars:
                if oldCar not in cars:
                    self.__removeCar(oldCar)

        car_n = len(self.carIllustrations)  # the number of the car in the list carIllustrations

        # Update the direction angle of all cars
        # Used to determine the order of cars crossing the intersection/merge
        for i in range(car_n):
            angle = self.carIllustrations[i].update()

            if angle < 0:
                angle += 360
            self.cars[i].car_direction_angle = angle

    ## Add a car object and a car illustration object
    # car -  Car that accessed to the street network
    def __addNewCar(self, car):
        self.cars.append(car)
        self.carIllustrations.append(CarIllustration(car, self.canvas))

    ## Remove a car object and a car illustration object
    # car - Car that exited from the street network
    def __removeCar(self,car):
        self.cars.remove(car)
        # remove also the corresponding carIllustration object
        for carIllustration in self.carIllustrations:
            if carIllustration.car == car:
                for bar in carIllustration.bars:
                    self.canvas.delete(bar)
                self.carIllustrations.remove(carIllustration)
        print("Car " + str(car.id) + " exited the street network. Stopped drawing it.")

########################################END OF MOVE CARS#########################################
#################################################################################################
