# Modifiable Traffic Simulator
A traffic simulation framework is proposed to allow users to freely implement different car motion models and street networks with little to no limitations. The simulation framework is implemented for evaluation in Python.

The key idea of the traffic simulator is the assumption that any traffic scenario can be modelled using streets and nodes.
A street, hereby, is straight, single lane and unidirectional. Multiple streets are connected to each other via nodes.
Here I need to clarify the understanding of an intersection. Two streets only connect by a node - an intersection is defined by a node. Without a node, two streets do not connect.


The vehicles only consider each other if the streets are connected by a node, not if the streets just pass over each other. You can think of two streets passing over each other as one street being a bridge. The cars don’t ”see” each other. We strictly adhere to the Street-Node concept here. It’s just like in an electrical network where you have wires passing over each other. A connection is only clarified by a node.

## Code
The project consists of the files
* Images:
  * car blue2.png - blue car image
  * car gray2.png - grey car image
  * car green2.png - green car image
  * car red2.py - red car image
* Network setup:
  * setupStreetNetwork CN.py - sets up a complex street network
  * setupStreetNetwork SN.py - sets up a simple street network
* Only animation:
  * carDrawer.py - manages all car illustration objects in the animation pane
  * carIllustration.py - represents an individual car illustration
  * drawStreetNetwork.py - draws the street network
  * userInterfaceDrawer.py - creates the user interface
* Dynamics calculation:
  * ground structure.py - provided basic dynamics structure Parameter setting
  * param manager.py - manages parameters of the simulation
  * Parameter.py - represents an individual parameter
* Logger:
  * logger.py - logs the simulation car states into a .log file
  * logger txt.py - logs the simulation car states in the form of a dictionary into a .txt file
* Mixed:
  * mainStreetNetworkTest.py - the main file functions
  * Live Simulation.py - performs the realtime simulation (moves vehicles and updates the environment)
  * car.py - represents a car, calculates the state of the car based on the motion model
  * lane.py - represents a single lane
  * street.py - represents an individual street
  * streetConnectionPoint.py - represents a node that connects two streets
  * streetNetwork.py - represents a full street network consisting of many streets
  * mathUtil.py - provides space to add math utility

## Starting the simulator

The simulator is started using the mainStreetNetworkTest.py file.

Aside from that, relevant to the user are only car.py and the setupStreetNetwork_*.py
files.
