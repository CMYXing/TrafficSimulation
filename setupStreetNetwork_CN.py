from street import Street
from streetConnectionPoint import StreetConnectionPoint
from streetNetwork import StreetNetwork


# Build a complex street network
def buildStreetNetwork():

    ### Define all of the street connection nodes ###
    # Entrance nodes
    node0 = StreetConnectionPoint(100,700)
    node30 = StreetConnectionPoint(100, 50)

    # Exit nodes
    node29 = StreetConnectionPoint(1100, 245)

    # Merge and intersection nodes
    node4 = StreetConnectionPoint(700, 650)
    node9 = StreetConnectionPoint(950, 300, isProbabilitySettable=True)
    node10 = StreetConnectionPoint(850, 245, isProbabilitySettable=True)
    node13 = StreetConnectionPoint(450, 50)
    node15 = StreetConnectionPoint(400, 300)

    # Rest of the street nodes
    node1 = StreetConnectionPoint(250, 700)
    node2 = StreetConnectionPoint(400, 700)
    node3 = StreetConnectionPoint(600, 700)
    node5 = StreetConnectionPoint(1050, 650)
    node6 = StreetConnectionPoint(1150, 550)
    node7 = StreetConnectionPoint(1150, 350)
    node8 = StreetConnectionPoint(1100, 300)
    node11 = StreetConnectionPoint(850, 100)
    node12 = StreetConnectionPoint(800, 50)
    node14 = StreetConnectionPoint(400, 100)
    node16 = StreetConnectionPoint(400, 450)
    node17 = StreetConnectionPoint(350, 500)
    node18 = StreetConnectionPoint(150, 500)
    node19 = StreetConnectionPoint(100, 550)
    node20 = StreetConnectionPoint(100, 600)
    node21 = StreetConnectionPoint(150, 650)
    node22 = StreetConnectionPoint(150, 300)
    node23 = StreetConnectionPoint(100, 250)
    node24 = StreetConnectionPoint(100, 200)
    node25 = StreetConnectionPoint(150, 150)
    node26 = StreetConnectionPoint(250, 150)
    node27 = StreetConnectionPoint(650, 245)
    node28 = StreetConnectionPoint(500, 150)

    ### Define all of the streets ###
    # Entrance Streets
    street1 = Street(node0, node1, canSpawnCars=True)
    street31 = Street(node30, node13, canSpawnCars=True)

    # Exit Streets
    street30 = Street(node10, node29)

    # Merge and intersection streets
    street4 = Street(node3, node4)
    street22 = Street(node21, node4)
    street5 = Street(node4, node5)

    street9 = Street(node8, node9)
    street10 = Street(node9, node10)
    street32 = Street(node9, node15)

    #street10 = Street(node9, node10)
    street28 = Street(node27, node10)
    street11 = Street(node10, node11)
    #street30 = Street(node10, node29)

    street13 = Street(node12, node13)
    #street31 = Street(node30, node13, canSpawnCars=True)
    street14 = Street(node13, node14)

    street15 = Street(node14, node15)
    #street32 = Street(node9, node15)
    street16 = Street(node15, node16)
    street23 = Street(node15, node22)

    # Tunnel
    street33 = Street(node26, node28, isTunnel=True)

    # Rest of the streets
    street2 = Street(node1, node2)
    street3 = Street(node2, node3)
    street6 = Street(node5, node6)
    street7 = Street(node6, node7)
    street8 = Street(node7, node8)
    street12 = Street(node11, node12)
    street17 = Street(node16, node17)
    street18 = Street(node17, node18)
    street19 = Street(node18, node19)
    street20 = Street(node19, node20)
    street21 = Street(node20, node21)
    street24 = Street(node22, node23)
    street25 = Street(node23, node24)
    street26 = Street(node24, node25)
    street27 = Street(node25, node26)
    street29 = Street(node28, node27)


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
               street15,
               street16,
               street17,
               street18,
               street19,
               street20,
               street21,
               street22,
               street23,
               street24,
               street25,
               street26,
               street27,
               street28,
               street29,
               street30,
               street32,
               street33,
               street31
             ]

    streetNetwork = StreetNetwork(streets)

    return streetNetwork

