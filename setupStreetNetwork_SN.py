from street import Street
from streetConnectionPoint import StreetConnectionPoint
from streetNetwork import StreetNetwork


# Build a simple street network
def buildStreetNetwork():

    ### Define all of the street connection nodes ###
    # Entrance nodes
    node0 = StreetConnectionPoint(100, 650)

    # Exit nodes
    node13 = StreetConnectionPoint(950, 100)

    # Merge and intersection nodes
    node4 = StreetConnectionPoint(650, 600)
    node7 = StreetConnectionPoint(950, 200, isProbabilitySettable=True)

    # Rest of the street nodes
    node1 = StreetConnectionPoint(200, 650)
    node2 = StreetConnectionPoint(350, 650)
    node3 = StreetConnectionPoint(500, 650)
    node5 = StreetConnectionPoint(900, 600)
    node6 = StreetConnectionPoint(950, 550)
    node8 = StreetConnectionPoint(900, 150)
    node9 = StreetConnectionPoint(150, 150)
    node10 = StreetConnectionPoint(100, 200)
    node11 = StreetConnectionPoint(100, 550)
    node12 = StreetConnectionPoint(150, 600)


    ### Define all of the streets ###
    # Entrance Streets
    street1 = Street(node0, node1, canSpawnCars=True)

    # Exit Streets
    street14 = Street(node7, node13)

    # Merge and intersection streets
    street4 = Street(node3, node4)
    street13 = Street(node12, node4)
    street5 = Street(node4, node5)

    street7 = Street(node6, node7)
    street8 = Street(node7, node8)
    #street14 = Street(node7, node13)

    # Rest of the streets
    street2 = Street(node1, node2)
    street3 = Street(node2, node3)
    street6 = Street(node5, node6)
    street9 = Street(node8, node9)
    street10 = Street(node9, node10)
    street11 = Street(node10, node11)
    street12 = Street(node11, node12)


    # All streets to be drawn in the simulation
    streets = [street1,
               street2,
               street3,
               street4,
               street5,
               street6,
               street7,
               street8,
               street9,
               street10,
               street11,
               street12,
               street13,
               street14,
             ]

    streetNetwork = StreetNetwork(streets)

    return streetNetwork
