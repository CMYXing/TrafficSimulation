################### use the car object to produce an illustration for it#############
#####################################################################################
import PIL.Image as Image
from numpy import arctan, pi, cos, sin, array
from random import randrange
from PIL import ImageTk

import Parameter

## According to the appropriate size of CAR_Dimension
CAR_DIMENSIONS = Parameter.get_value('CAR_Dimension')[0], Parameter.get_value('CAR_Dimension')[0]
LANE_WIDTH = Parameter.get_value('LANEWIDTH')
Scale = Parameter.get_value('SCALE')
bar_number_limit = Parameter.get_value('barnumberlimit')

## The CarIllustration class' purpose is to display the Car object in the animation
class CarIllustration:

    def __init__(self, car, canvas):
        # Let's place the car correctly
        self.car = car
        self.street = self.car.getStreet()  # Returns the street this car belongs to
        self.xCoordinate, self.yCoordinate = self.street.getCoordinateAt(car.getProgressOnLane())
        self.canvas = canvas

        # pick a random car image
        filenames = ["car_blue2.png" , "car_gray2.png", "car_green2.png", "car_red2.png"]
        self.filename = filenames[randrange(0, 4)]

        # Use PIL library to open and rotate the car image
        self.carImage = Image.open(self.filename)
        self.angle = 0
        self.carImage = self.carImage.rotate(self.angle)
        self.imageDimension = CAR_DIMENSIONS  # Make image smaller, otherwise, it's too big
        self.carImage.thumbnail(self.imageDimension, Image.ANTIALIAS)

        # Now, convert to tkinter image so we can show it in the animation
        self.tkCarImage = ImageTk.PhotoImage(self.carImage)
        self.shape = canvas.create_image(self.xCoordinate, self.yCoordinate, image=self.tkCarImage)
        self.bar_number = 0
        self.bars = []
        self.update()

    ##################################### END OF SELF INITIALIZATION #####################################


    ## Complete the animation of the car turning
    def rotateImage(self, angle):
        self.carImage = Image.open(self.filename)
        self.carImage.thumbnail(self.imageDimension, Image.ANTIALIAS)
        self.angle = angle
        self.tkCarImage = ImageTk.PhotoImage(self.carImage.rotate(self.angle))
        self.shape = self.canvas.create_image(self.xCoordinate, self.yCoordinate, image=self.tkCarImage)
        ## when there is a tunnel,hide the car
        if self.car.getStreet().isTunnel:
            self.canvas.itemconfigure(self.shape, state='hidden')
            for bar in self.bars:
                self.canvas.itemconfigure(bar, state='hidden')


    ## define bar's color according to car's acceleration
    def calc_bars_color(self):
        [red_CV, green_CV, blue_CV] = [200.0, 200.0, 200.0]  # grey tone at acc=0
        if (self.car.acceleration <= -5.0):  # very strong deceleration
            [red, green, blue] = [255.0, 0.0, 0.0]
        elif (-5.0 < self.car.acceleration <= 0):  # deceleration
            x = abs(self.car.acceleration) / 5.0
            red = red_CV + (255 - red_CV) * x
            # green = green_CV + ( 0 - green_CV)*x
            green = green_CV - green_CV * x
            blue = green
        elif (0 < self.car.acceleration < 2.0):
            x = abs(self.car.acceleration) / 2.0
            red = red_CV - red_CV * x
            green = green_CV - green_CV * x
            blue = blue_CV + (255.0 - blue_CV) * x
        elif (self.car.acceleration >= 2.0):
            [red, green, blue] = [0.0, 0.0, 255.0]


        return '#%02x%02x%02x' % (int(red), int(green), int(blue))

    #claculate bar's coordinate
    def bar_coordinate_update(self):
        bar_angle = (self.angle + 90)/180*pi
        angle = self.angle/180*pi
        bar_coordinate1 = array([self.xCoordinate, self.yCoordinate])+(CAR_DIMENSIONS[0]/2 + Scale) * array([-cos(angle), sin(angle)]) - LANE_WIDTH/4 * array([-cos(bar_angle), sin(bar_angle)])
        bar_coordinate2 = array([self.xCoordinate, self.yCoordinate])+(CAR_DIMENSIONS[0]/2 + Scale) * array([-cos(angle), sin(angle)]) + LANE_WIDTH/4 * array([-cos(bar_angle), sin(bar_angle)])
        x1 = bar_coordinate1[0]
        y1 = bar_coordinate1[1]
        x2 = bar_coordinate2[0]
        y2 = bar_coordinate2[1]
        return x1, y1, x2, y2

    ## Update the movement of the car illustration
    def update(self):
        # Maybe the street,where the car is located on, has changed:
        self.street = self.car.getStreet()
        if self.street is None:
            return self.angle
        # Store the "old" coordinates for later
        self.previousXCoordinate = self.xCoordinate
        self.previousYCoordinate = self.yCoordinate
        # Calculate the new coordinates for the illustration
        self.xCoordinate, self.yCoordinate = self.car.lane.getCoordinateAt(self.car.getProgressOnLane())
        # Move the animation shape object
        self.canvas.coords(self.shape,
                      self.xCoordinate,
                      self.yCoordinate)

        ##### Now rotate the image######
        # The rotation can be determined by the change in coordinates
        dx = self.xCoordinate - self.previousXCoordinate
        dy = self.yCoordinate - self.previousYCoordinate

        ## Calculate the correct angle depending on the driving direction
        if dx != 0 or dy != 0:  # If the car is parked in place (dx=dy=0),
                                # the car illustration angle of the previous time step is followed.
            if (dx < 0 and dy == 0):
                self.angle = -180
            elif (dx > 0 and dy == 0):
                self.angle = 0
            elif (dx == 0 and dy > 0):
                self.angle = -90
            elif (dx == 0 and dy < 0):
                self.angle = 90
            elif (dx == 0 and dy == 0):
                pass
            else:
                if (dx > 0 and dy > 0):
                    self.angle = - 90 + arctan(dx / dy) * 360 / (2 * pi)
                elif (dx > 0 and dy < 0):
                    self.angle = 90 + arctan(dx / dy) * 360 / (2 * pi)
                elif (dx < 0 and dy > 0):
                    self.angle = -90 + arctan(dx / dy) * 360 / (2 * pi)
                elif (dx < 0 and dy < 0):
                    self.angle = 90 + arctan(dx / dy) * 360 / (2 * pi)
            self.rotateImage(self.angle)  # Update the angle of the car illustration

            ##update acceleration bar
            if self.bar_number < bar_number_limit:
                bar_color = self.calc_bars_color()
                bar_x1, bar_y1, bar_x2, bar_y2 = self.bar_coordinate_update()
                self.bars.append(self.canvas.create_line(bar_x1, bar_y1, bar_x2, bar_y2, width=2, fill=bar_color))
                self.bar_number += 1
            elif self.bar_number == bar_number_limit:
                self.canvas.delete(self.bars[0])
                del self.bars[0]
                bar_color = self.calc_bars_color()
                bar_x1, bar_y1, bar_x2, bar_y2 = self.bar_coordinate_update()
                self.bars.append(self.canvas.create_line(bar_x1, bar_y1, bar_x2, bar_y2, width=2, fill=bar_color))
            else:
                self.canvas.delete(self.bars[0])
                self.canvas.delete(self.bars[1])
                del self.bars[0]
                del self.bars[1]
                bar_color = self.calc_bars_color()
                bar_x1, bar_y1, bar_x2, bar_y2 = self.bar_coordinate_update()
                self.bars.append(self.canvas.create_line(bar_x1, bar_y1, bar_x2, bar_y2, width=2, fill=bar_color))
                self.bar_number -= 1

            if self.car.getStreet().isTunnel or Parameter.get_value('show_bar') == 0:
                for bar in self.bars:
                    self.canvas.itemconfigure(bar, state='hidden')

        return self.angle



