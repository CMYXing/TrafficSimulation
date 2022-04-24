# The CarState object is only a "data-object"
# It only holds information about the longitudinal coordinate, speed and does nothing else

import numpy as np
from random import choices, choice
from ground_structure import *
import Parameter
import userInterfaceDrawer

Scale = Parameter.get_value('SCALE')

class Car:
    carCounter = 0 # the amount of the current cars

    def __init__(self, lane):
        # From the car's view, it only has longitudinal information
        self.longitudinalCoordinate = 0  # the current position
        self.nextLongitudinalCoordinate = 0  # the next position

        self.speed = Parameter.get_value('init_speed')    # 15 m/s
        self.nextSpeed = 0  #  m/s
        self.acceleration = Parameter.get_value('init_acc')  #  0m/s^2
        self.nextAcceleration = 0  # m/s^2
        self.Laneprogress = 0  # how long has the car driven on the (new) lane
        self.nextLaneprogress = 0
        self.previousLaneProgress = 0

        self.changeLane = False

        self.car_direction_angle = 0

        self.lane = lane  # The car also knows which lane it is on
        # self.previousLane = lane
        self.actuell_route_index = 0  # the index of self.route
        self.route = self.__get_car_route()  # route is a list of street number,the car will drive to the end
        self.NoExit = False  # the car will always stay in network if self.NoExit = True

        self.calculateValue = False

        self.constraint_params = Parameter.get_value('constraint_params')

        # here is to select the parameters in order 15 sets of data in a round
        self.idm_params = Parameter.get_value('idm_params')[Car.carCounter % 15]

        # Environment model of the agent
        self.env = Env()

        # Every car have a dictionary which contains acceleraation noise from other cars
        self.value_dict = {}

        # We need a way to track individual cars (for logging), so we assign an ID to each one
        # It's a simple incremental number
        # Pythons built in id() function can not be used because it is not unique in our case
        self.id = Car.carCounter
        Car.carCounter += 1

    ################################# END OF INITIALIZATION #################################


    ## move the car and set the new coordinate as "longitudinalCoordinate"
    def move(self):
        self.previousLaneProgress = self.Laneprogress
        self.previousLane = self.lane

        if self.lane is None:
            # this means the car has exited the street network
            # and nothing should be done
            return

        # loading Dynamic Models
        self.__calculateCarStateAccordingToMovementModel()
        # calculates how long has the car driven in current lane
        self.Laneprogress += (self.nextLongitudinalCoordinate - self.longitudinalCoordinate) * Scale

        # getProgressOnLane(): returns how far the car has driven on this(next) street
        # if 0<getProgressOnLane()< 1,this means the car driven on this street
        # if getProgressOnLane() >= 1,this means the car surpassed the end of the street
        if self.getProgressOnLane() >= 1:
            # it has to be removed from the current one and passed to the next lane
            # calculates how much the car has driven "over the lane"
            surpassedLaneDistance = self.getProgressOnLane() * self.lane.getLength() - self.lane.getLength()
            self.changeLane = True

            # put the car at the right coordinate of the new lane
            self.Laneprogress = surpassedLaneDistance

        self.calculateValue = True


    ##################################### START OF ROUTE ######################################


    ## The car will choose complete route to drive at the beginning
    # get the complete car route
    def __get_car_route(self):
        Route = []
        lane = self.lane
        Route.append(lane)
        nextStreets = lane.street.getNextStreets()

        while len(nextStreets) != 0:
            endConnectionPoint = lane.street.endConnectionPoint
            if endConnectionPoint.isProbabilitySettable:
                # find the next street according to weighted probabilities
                nextStreetChoices = choices(nextStreets, weights=endConnectionPoint.getTurnProbabilites(), k=1)
                nextStreetChoice = nextStreetChoices[0]
            else:
                # choose next street randomly
                nextStreetChoice = choice(nextStreets)
            lane = nextStreetChoice.lanes[0]
            Route.append(lane)
            nextStreets = lane.street.getNextStreets()

            if len(Route) > 100:  # prevent cars from circulating on the road without going out
                self.NoExit = True
                break
        return Route


    ## after node's probability is chanaged, the car route will be updated with new probability
    def update_car_route(self):
        Route = []
        routeindex = self.actuell_route_index
        lane = self.route[routeindex]

        # find the node whose probability is changed
        while routeindex < len(self.route):
            lane = self.route[routeindex]
            endConnectionPoint = lane.street.endConnectionPoint
            routeindex += 1
            if endConnectionPoint.ischanged:
                break

        # choose the rest lane after the changed node
        Route.extend(self.route[0:routeindex])
        Route.extend(self.find_rest_route(lane))
        self.route = Route


    ## when node has changed, find the rest lane after the changed node
    def find_rest_route(self, lane):
        Route = []
        nextStreets = lane.street.getNextStreets()
        while len(nextStreets) != 0:
            endConnectionPoint = lane.street.endConnectionPoint
            if endConnectionPoint.isProbabilitySettable:
                # find the next street according to weighted probabilities
                nextStreetChoices = choices(nextStreets, weights=endConnectionPoint.getTurnProbabilites(), k=1)
                nextStreetChoice = nextStreetChoices[0]
            else:
                # choose next street randomly
                nextStreetChoice = choice(nextStreets)
            lane = nextStreetChoice.lanes[0]
            Route.append(lane)
            nextStreets = lane.street.getNextStreets()
            if len(Route) > 100:  # prevent cars from circulating on the road without going out
                self.NoExit = True
                break
        if len(Route) <= 100:
            self.NoExit = False
        return Route

    ################################## END OF ROUTE ##################################


    ## update the longitudinal Coordinate,speed and acceleration
    def updateState(self):
        self.longitudinalCoordinate = self.nextLongitudinalCoordinate
        self.speed = self.nextSpeed
        self.acceleration = self.nextAcceleration
        self.calculateValue = False

        # update lane information
        if self.changeLane:
            # reomove the current car of the list of cars in this lane
            self.lane.cars.remove(self)
            # determine whether the car has driven through all the streets in the list the index of the route correspond street
            if self.actuell_route_index >= len(self.route) - 1:
                if self.NoExit:
                    route_temp = self.route[-10:]
                    route_temp.extend(self.find_rest_route(self.lane))
                    self.route = route_temp
                    self.actuell_route_index = 10
                    self.lane = self.route[self.actuell_route_index]
                    self.lane.cars.append(self)
                else:
                    self.lane.street.removeCar(self)
                    self.lane = None
                    return
            else:
                self.actuell_route_index += 1
                self.lane = self.route[self.actuell_route_index]
                self.lane.cars.append(self)

        self.changeLane = False


    ##################################################################################

    ### Get all vehicles near the car object
    ## return a list of cars, which drive on next and previous lanes
    def __getAllCarsNearby(self):
        allCarsNearby = []
        for car in self.__getCarsOnSameLane():
            if self is not car:
                allCarsNearby.append(car)
        if self.__getAllCarsInNextLane() is not None:
            allCarsNearby.extend(self.__getAllCarsInNextLane())
        if self.__getAllCarsInPreviousLane() is not None:
            allCarsNearby.extend(self.__getAllCarsInPreviousLane())
        return allCarsNearby


    ## Returns number of other cars on this lane
    def __getCarsOnSameLane(self):
        return self.lane.cars


    ## Returns the list of cars on next lane
    def __getAllCarsInNextLane(self):
        routeIndex = self.actuell_route_index + 1
        if routeIndex < len(self.route):
            return self.route[routeIndex].cars
        else:
            return None


    ## Returns the list of cars on previous lane
    def __getAllCarsInPreviousLane(self):
        routeIndex = self.actuell_route_index - 1
        if routeIndex >= 0:
            return self.route[routeIndex].cars
        else:
            return None

    ##################################################################################

    ## get the length of the rest of this lane
    def __getDistanceToEndConnectionPoint(self):
        return (1 - self.getProgressOnLane()) * self.lane.getLength()

    ## get the car in front of this car
    def __getCarInFront(self):
        carsOnSameLane = self.__getCarsOnSameLane()
        # cars on next lane are always in front
        allCarsInFront = []
        carsOnrestLanes = []

        ## add all cars that are on the same lane and in front of this car
        for car in carsOnSameLane:
            if car.calculateValue:
                if car.previousLaneProgress / car.lane.getLength() > self.getProgressOnLane():
                    allCarsInFront.append(car)
            elif car.getProgressOnLane() > self.getProgressOnLane():
                allCarsInFront.append(car)

        if len(allCarsInFront) == 0:
            ## we must look on the rest lanes
            id = self.actuell_route_index + 1
            while id < len(self.route):
                if self.lane != self.route[id]:
                    carsOnrestLanes = self.route[id].cars
                    if len(carsOnrestLanes) != 0:
                        break
                id += 1

            # all of rest lane also has no cars
            if len(carsOnrestLanes) == 0:
                return None
            # there is a car in front, let's find it
            else:
                closestCarInFrontOfSelf = min(carsOnrestLanes, key=lambda car: car.getProgressOnLane())
                return closestCarInFrontOfSelf

        # Below, a lambda expression is used. See https://stackoverflow.com/questions/6085467/python-min-function-with-a-list-of-objects for reference
        closestCarInFrontOfSelf = min(allCarsInFront, key=lambda car: car.getProgressOnLane())
        return closestCarInFrontOfSelf


    ## calculate the distance of two cars for 3 case
    def __getDistanceBetweenTwoLongitudinalCars(self, firstCar, secondCar):
        # If the previous car has already been calculated at that time step,
        # it needs to be calculated with information from its previous time step!

        distance = 0

        if firstCar is None:
            distance = self.constraint_params['d_max'] * Scale  # case 1: there is no car in front

        elif firstCar.lane == secondCar.lane:  # case 2: two cars on the same lane
            distance = firstCar.previousLaneProgress - secondCar.getProgressOnLane() * secondCar.lane.getLength()

        elif firstCar.lane != secondCar.lane:  # case 3: they are on two connected lanes
            secondcar_index = secondCar.actuell_route_index

            if firstCar.calculateValue:
                if firstCar.previousLane != secondCar.lane:
                    firstcar_index = secondCar.route.index(firstCar.previousLane, secondcar_index)
                    for i in range(secondcar_index, firstcar_index):
                        distance += secondCar.route[i].getLength()
                distance = distance + firstCar.previousLaneProgress \
                           - secondCar.getProgressOnLane() * secondCar.lane.getLength()

            else:
                firstcar_index = secondCar.route.index(firstCar.lane, secondcar_index)
                for i in range(secondcar_index, firstcar_index):
                    distance += secondCar.route[i].getLength()
                distance = distance + firstCar.getProgressOnLane() * firstCar.lane.getLength() \
                           - secondCar.getProgressOnLane() * secondCar.lane.getLength()

        return distance


    ## get the distance of the front car
    def __getDistanceToFrontCar(self):
        self.carInFront = self.__getCarInFront()
        return self.__getDistanceBetweenTwoLongitudinalCars(self.carInFront, self)


    ## get next lane the car should drive
    def __getNextLane(self):
        nextStreets = self.getStreet().getNextStreets()
        if not nextStreets:
            return None

        endConnectionPoint = self.getStreet().endConnectionPoint
        if endConnectionPoint.isProbabilitySettable:
            # find the next street according to weighted probabilities
            nextStreetChoices = choices(
                nextStreets, weights=endConnectionPoint.getTurnProbabilites(), k=1)
            nextStreetChoice = nextStreetChoices[0]

        else:
            # choose next street randomly
            nextStreetChoice = choice(nextStreets)

        return nextStreetChoice.lanes[0]


    ## returns the street this car belongs to
    def getStreet(self):
        if self.lane is None:
            return None
        else:
            return self.lane.street

    ## returns how far the car has driven on this lane (as a percentage from 0 to 1)
    def getProgressOnLane(self):
        laneLength = self.lane.getLength()
        if self.calculateValue:
            return self.previousLaneProgress/self.previousLane.getLength()
        else:
            return self.Laneprogress/laneLength


    ################################## START OF MovementModel #######################################
    #################################################################################################

    ## According to movement model calculate and set new xva state
    ## xva means position x, speed v & acceleration a
    ## acceleration can be seted with/without gaussian noise
    def __calculateCarStateAccordingToMovementModel(self):

        # Inteligent Driver Model, considers only one other car ((infront))
        if self.idm_params['advance_mode'] in ['idm', 'ext_idm', 'lim_idm', 'lim_idm+']:
            ext = False
            limited = False
            if self.idm_params['advance_mode'] in ['ext_idm']:
                ext = True
            if self.idm_params['advance_mode'] in ['lim_idm', 'lim_idm+']:
                limited = True

            v_min = self.constraint_params['v_min']
            v_max = self.constraint_params['v_max']  # Maximum speed and minimum of speed limit

            # Get most relevant other agents from environment
            other_agents = []
            selected = None

            # Don't consider anything further away than d_max m
            closest = self.constraint_params['d_max']  # d_max = maximal sensor duration

            mergeAgent_drive = []  # the cars, which have priority to go
            intersectAgent_drive = []  # the cars, which have priority to go
            # add car, which is merge agent, to the list of mergeAgent_drive
            if len(self.env['merge_agents']) > 0:
                for car in self.env['merge_agents']:
                    if self.addAgents(car):
                        mergeAgent_drive.append(car)
            # add car, which is intersect agent, to the list of intersectAgent_drive
            if len(self.env['intersect_agents']) > 0:
                for car in self.env['intersect_agents']:
                    if self.addAgents(car):
                        intersectAgent_drive.append(car)

            # calculate the distance d between ego car and the infront agent
            # considering whether there is a infront agent and whether there is a merge/intersect agent, there are 9 cases
            if self.__getCarInFront() is None:
                # case1: no car infront and no merge car and intersect car
                if len(mergeAgent_drive) == 0 and len(intersectAgent_drive) == 0:
                    pass

                # case2: no car infront and have merge car
                elif len(mergeAgent_drive) != 0 and len(intersectAgent_drive) == 0:
                    # max() means:the max value of getProgressOnLane() from the list merge Agent_drive
                    # find the merge agent, which is closest to the merge point
                    closestCar_other = max(mergeAgent_drive, key=lambda car: car.getProgressOnLane())
                    # scaling 4 pixel per meter
                    d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                    # getDistanceToEndConnectionPoint() means: get the length of the rest of this lane
                    # consider only agents whos back bumper is in front of the own front bumper
                    d = d - 0.5 * (
                                self.constraint_params['car_length'] + closestCar_other.constraint_params['car_length'])
                    if d < closest:  # if distance d is infront and in detection range
                        selected = closestCar_other  # choose this ONE other agent
                        closest = d

                # case3: no car infront and have intersect car
                elif len(mergeAgent_drive) == 0 and len(intersectAgent_drive) != 0:
                    # find the intersect agent, which is closest to the intersect point
                    closestCar_other = max(intersectAgent_drive, key=lambda car: car.getProgressOnLane())
                    # scaling 4 pixel per meter
                    d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                    d = d - 0.5 * (
                                self.constraint_params['car_length'] + closestCar_other.constraint_params['car_length'])

                    if d < closest:  # if distance d is infront and in detection range
                        selected = closestCar_other  # choose this ONE other agent
                        closest = d

                # case4: no car infront, have intersect car and merge car
                else:
                    other_agents.extend(intersectAgent_drive)
                    other_agents.extend(mergeAgent_drive)
                    # find the merge/intersect agent, which is closest to the merge/intersect point
                    closestCar_other = max(other_agents, key=lambda car: car.getProgressOnLane())
                    # scaling 4 pixel per meter
                    d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                    d = d - 0.5 * (
                                self.constraint_params['car_length'] + closestCar_other.constraint_params['car_length'])
                    if d < closest:  # if distance d is infront and in detection range
                        selected = closestCar_other  # choose this ONE other agent
                        closest = d

            else:
                # case5: have car infront and the car drive in the same lane
                if self.lane == self.__getCarInFront().lane:
                    closestCar_other = self.__getCarInFront()
                    # scaling 4 pixel per meter
                    d = (self.__getDistanceToFrontCar()) / Scale
                    d = d - 0.5 * (
                                self.constraint_params['car_length'] + closestCar_other.constraint_params['car_length'])
                    # if distance d is infront and in detection range
                    if d < closest:
                        selected = closestCar_other  # choose this ONE other agent
                        closest = d


                else:
                    # case6: have car infront but the front car is in next lane and have no merge car and intersect car
                    if len(mergeAgent_drive) == 0 and len(intersectAgent_drive) == 0:
                        closestCar_other = self.__getCarInFront()
                        # scaling 4 pixel per meter
                        d = (self.__getDistanceToFrontCar()) / Scale
                        d = d - 0.5 * (
                                self.constraint_params['car_length'] + closestCar_other.constraint_params['car_length'])
                        if d < closest:
                            selected = closestCar_other  # choose this ONE other agent
                            closest = d

                    # case7: have car infront but the front car is in next lane and have merge car
                    elif len(mergeAgent_drive) != 0 and len(intersectAgent_drive) == 0:
                        # find the merge agent, which is closest to the merge point
                        closestCar_other = max(mergeAgent_drive, key=lambda car: car.getProgressOnLane())
                        # scaling 4 pixel per meter
                        d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                        d = d - 0.5 * (self.constraint_params['car_length'] + closestCar_other.constraint_params[
                            'car_length'])
                        if d < closest:
                            selected = closestCar_other  # choose this ONE other agent
                            closest = d


                    # case8: have car infront but the front car is in next lane and have intersect car
                    elif len(mergeAgent_drive) == 0 and len(intersectAgent_drive) != 0:
                        # find the intersect agent, which is closest to the intersect point
                        closestCar_other = max(intersectAgent_drive, key=lambda car: car.getProgressOnLane())
                        # scaling 4 pixel per meter
                        d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                        d = d - 0.5 * (self.constraint_params['car_length'] + closestCar_other.constraint_params[
                            'car_length'])
                        if d < closest:
                            selected = closestCar_other  # choose this ONE other agent
                            closest = d


                    # case9: have car infront but the front car is in next lane and have merge car and intersect car
                    else:
                        other_agents.extend(intersectAgent_drive)
                        other_agents.extend(mergeAgent_drive)
                        # find the merge/intersect agent, which is closest to the merge/intersect point
                        closestCar_other = max(other_agents, key=lambda car: car.getProgressOnLane())
                        # scaling 4 pixel per meter
                        d = (self.__getDistanceToEndConnectionPoint() - closestCar_other.__getDistanceToEndConnectionPoint()) / Scale
                        d = d - 0.5 * (self.constraint_params['car_length'] + closestCar_other.constraint_params[
                            'car_length'])
                        if d < closest:
                            selected = closestCar_other  # choose this ONE other agent
                            closest = d



            # accroding to the idm parameter, calculate the acceleration without gaussian noise
            self.acceleration = self.dvdt_idm(selected, closest, limited, ext)

            # accroding to the idm parameter, calculate the acceleration with gaussian noise
            # considering the noise from selected car
            if self.idm_params['noise_mode'] == 1:
                if selected is not None:
                    closestCarInfront_id = selected.id
                    self.acceleration += self.value_dict[closestCarInfront_id]

            self.nextLongitudinalCoordinate, self.nextSpeed, self.nextAcceleration = \
                calc_next_xva_state(self.longitudinalCoordinate, self.speed, self.acceleration,
                                    Parameter.get_value('delta_t'), v_min, v_max, const_acc=True)

    ####################################################################################################
    ##################################### END OF MovementModel #########################################


    ## get the id of the car
    def getCarID(self):
        return self.id


    ## decide whether the can can be added to car list
    def addAgents(self, car):
        addAgent = False
        if self.__getDistanceToEndConnectionPoint() > car.__getDistanceToEndConnectionPoint():
            addAgent = True
        elif self.__getDistanceToEndConnectionPoint() == car.__getDistanceToEndConnectionPoint() and \
                                    self.car_direction_angle < car.car_direction_angle:
            addAgent = True
        return addAgent

    #####################################################################################################


    ## The keys in the dict should by updated every time step as same as Env changes.
    ## So if a additional agents appears in the enviroment, it must also get a new entriy in value_dict.
    def updateEnv_And_ValueDict(self):

        # define empty different agents to prevent compilation error
        long_agents = []
        merge_agents = []
        paral_agents = []
        intersect_agents = []

        ## long_agents
        allCarsNearby = self.__getAllCarsNearby()
        if len(allCarsNearby) > 0:
            for car in allCarsNearby:
                allCarsNearby_car = car.__getAllCarsNearby()
                if self in allCarsNearby_car:
                    long_agents.append(car)
        carInFront = self.__getCarInFront()
        if carInFront is not None:
            if carInFront not in long_agents:
                long_agents.append(carInFront)

        ## merge_agents and intersect_agents
        endConnectionPoint = self.getStreet().endConnectionPoint
        if endConnectionPoint.isMerge():  # Check if the next node is a merge
            # Check if the other incoming streets of this merge have cars
            for street in endConnectionPoint.incomingStreets:
                if street is not self.getStreet() and street.getAllCars():
                    for car in street.getAllCars():
                        if self.route[self.actuell_route_index + 1] == car.route[car.actuell_route_index + 1]:
                            merge_agents.append(car)
                        else:
                            intersect_agents.append(car)

        # each agent has its own dictionary, which has entries for all other agents detected by him
        self.env = Env(long_agents=long_agents, merge_agents=merge_agents,
                       intersect_agents=intersect_agents, paral_agents=paral_agents)


        # add all different agents to the list agents
        agents = []
        agents.extend(long_agents)
        agents.extend(merge_agents)
        agents.extend(intersect_agents)
        agents.extend(paral_agents)

        # the agents should have the following dictionaries called value_dict:
        value_dict = {}
        for car in agents:
            value_dict[car.id] = self.recalc_value_dicts(car)
        self.value_dict = value_dict


    ## After updating the keys,
    ## every time step a method "recalc_value_dicts()" should be run which adapts all values in the dicts of all agents
    def recalc_value_dicts(self, car):
        v = self.speed
        delta_v = car.speed - self.speed
        if v == 0:
            return 0
        else:
            # (1 - Delta v / v) * min{0.2, gaussian noise with sigma = 0.1}
            return (1 - delta_v / v) * min(0.2, float(np.random.normal(0, 0.1, 1)))


    ## returns the next dvdt value of the car object based on IDM considering only one car infront
    # param in_front: other agent in front of the car object
    def dvdt_idm(self, infront, distance, limited=False, ext=False):
        if infront is None:  # no other car infront the car object --> assume direct behind my view horizon d_max is an obstacle (in_front_v=0.0)
            in_front_v = 0.0
        else:  # the other Agent named in_front is driving infront of the car object
            in_front_v = infront.speed  # x-Position of the agent infront

        # def dvdt_idm(v, v_other, distance, d_0, T_idm, a_max, b_comf, b_max, t_react=0.5, v_target=33.3, v_exp=1.0,
        # d_exp=1.0, ext=False, limited=False, idm_mode=None):
        dvdt = dvdt_idm(v=self.speed, v_other=in_front_v, distance=distance, d_0=self.idm_params['d_0'],
                        T_idm=self.idm_params['T_idm'], a_max=self.constraint_params['a_max'],
                        b_comf=self.idm_params['b_comf'], b_max=self.constraint_params['b_max'],
                        t_react=self.constraint_params['t_react'], v_target=self.idm_params['v_0'],
                        v_exp=self.idm_params['v_exp'], d_exp=self.idm_params['d_exp'], limited=limited,
                        ext=ext, idm_mode=self.idm_params['advance_mode'])
        return dvdt



