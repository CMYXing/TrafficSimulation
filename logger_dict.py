# A class that logs the state of various cars and stores the log in an output file
import Parameter
from datetime import datetime
import ast

class Logger_dict:

    def __init__(self, cars):
        self.cars = cars
        currentTimestamp = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
        self.outputFilename = "simulation_dict" + currentTimestamp + ".txt"
        self.simulation_dict = {}

    def log(self):
        self.__writeLogToFile()

    def __getCurrentSimulationDict(self):
        current_dict = {Parameter.get_value('step_number'): self.__getLogForCurrentSimulationStep()}
        self.simulation_dict.update(current_dict)
        return self.simulation_dict


    ## Get the log of the current time step
    def __getLogForCurrentSimulationStep(self):
        logData = {}
        for car in self.cars:
            # We want to know the state of each car
            gcsas = {car.id: self.__getCarStateAsList(car)}
            logData.update(gcsas)
        return logData


    ## Save logger data to file
    def __writeLogToFile(self):
        # Open a file with 'w+' mode
        with open(self.outputFilename, 'w+') as file:
            dict_data = self.__getCurrentSimulationDict()
            file.write('{')
            for key in dict_data:
                file.write('\n')
                file.writelines(str(key) + ': ' + str(dict_data[key]) + ',')
            file.write('\n' + '}')

    ## Return the car status as a string
    def __getCarStateAsList(self, car):
        return [car.longitudinalCoordinate, car.speed, car.acceleration]



