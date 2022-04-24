
# A class that logs the state of various cars and stores the log in an output file
from datetime import datetime

class Logger:

    def __init__(self, cars):
        self.cars = cars
        currentTimestamp = str( datetime.today().strftime('%Y-%m-%d-%H%M%S') )
        self.outputFilename = "simulation" + currentTimestamp + ".log"

    def log(self):
        self.__writeLogToFile()

    ## Get the log of the current time step
    def __getLogForCurrentSimulationStep(self):
        logData = []
        for car in self.cars:
            # We want to know the speed of each car
            logData.append({car.id: self.__getCarStateAsString(car)})
        return logData


    ## Save logger data to file
    def __writeLogToFile(self):
        # Open a file with access mode 'a' (append)
        file = open(self.outputFilename, 'a')
        # Append the newest simulationLog to the end of the file
        logLine = str(self.__getLogForCurrentSimulationStep()) + "\n"
        file.write(logLine)
        # Close the file
        file.close()


    ## Return the car status as a string
    def __getCarStateAsString(self, car):
        return "x=" + str(car.longitudinalCoordinate) + "; v=" + str(car.speed) + "; a=" + str(car.acceleration)
