import Parameter
import time
from datetime import datetime
from drawStreetNetwork import drawStreetNetwork

Scale = Parameter.get_value('SCALE')
constraint_params = Parameter.get_value('constraint_params')
currentTimestamp = str( datetime.today().strftime('%Y-%m-%d-%H%M%S') )

def simulation(tk, streetNetwork, carDrawer, logger, logger_dict):

    while Parameter.get_value('control_value'):

        allCarsInNetwork = streetNetwork.getAllCars()
        for car in allCarsInNetwork:
            car.updateEnv_And_ValueDict()

            # Update the routes of all cars if the node probabilities are changed
            for node in streetNetwork.getAllNodesWhereProbabilityCanBeCustomized():
                if node.ischanged:
                    car.update_car_route()

            # Move all cars
            car.move()

        # Record the attributes of agent with each sampling time point
        logger.log()
        logger_dict.log()

        # Update the States of all cars
        for car in allCarsInNetwork:
            car.updateState()

        for node in streetNetwork.getAllNodesWhereProbabilityCanBeCustomized():
            node.ischanged = False

        if Parameter.get_value('visible'):
            carDrawer.moveCars(streetNetwork.getAllCars())

        tk.update()
        time.sleep(Parameter.get_value('delta_t') * Parameter.get_value('slow_motion'))  # sampling time

        # Prevent cars from being generated too fast and causing crashes
        limit = 100
        for street in streetNetwork.streets:
            if street.canSpawnCars == True:
                for car in street.getAllCars():
                    if car.longitudinalCoordinate < limit:
                        limit = car.longitudinalCoordinate

        Parameter.set_value('spawnNewCarCounter', Parameter.get_value('spawnNewCarCounter') + 1)
        if Parameter.get_value('spawnNewCarCounter') > Parameter.get_value('spawnNewCarLimit'):
            if limit > 3 * (constraint_params['car_length']):
                streetNetwork.spawnCar()
                Parameter.set_value('spawnNewCarCounter', 0)


        # Update current time step
        step_number = Parameter.get_value('step_number') + 1
        Parameter.set_value('step_number', step_number)

