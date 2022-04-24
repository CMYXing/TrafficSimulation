import Parameter
import param_manager

from tkinter import Tk, Canvas
from userInterfaceDrawer import drawUserInterface, center_window
from drawStreetNetwork import drawStreetNetwork
# from setupStreetNetwork_SN import buildStreetNetwork
from setupStreetNetwork_CN import buildStreetNetwork
from carDrawer import CarDrawer

from logger import Logger
from logger_dict import Logger_dict

tk = Tk()  # Create the window
tk.title("StreetNetwork")  # Title of the window
center_window(tk, Parameter.get_value('Canvas_width') + Parameter.get_value('userInterfaceFrame_width'),
              Parameter.get_value('Window_Height'))  # Set window size

canvas = Canvas(tk, width=Parameter.get_value('Canvas_width'), height=Parameter.get_value('Window_Height'),
                bg="lightgrey")  # Create the canvas
canvas.pack()  # Makes the canvas visible
canvas.grid(row=0, column=0)


streetNetwork = buildStreetNetwork()  # Build a street network
drawStreetNetwork(canvas, streetNetwork)  # Draw the street network on the canvas

# Initialize the car Plotter
allCars = streetNetwork.getAllCars()
carDrawer = CarDrawer(allCars, canvas)
carDrawer.initializeCars()

# Initialize agent status logger
logger = Logger(allCars)
logger_dict = Logger_dict(allCars)

# Draw the user interface
drawUserInterface(tk, streetNetwork, carDrawer, logger, logger_dict, canvas)


canvas.mainloop()

