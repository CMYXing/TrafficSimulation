# Modifiable Traffic Simulator
A traffic simulation framework is proposed to allow users to freely implement different car motion models and street networks with little to no limitations. The simulation framework is implemented for evaluation in Python.

The key idea of the traffic simulator is the assumption that any traffic scenario can be modelled using streets and nodes.
A street, hereby, is straight, single lane and unidirectional. Multiple streets are connected to each other via nodes.
Here I need to clarify the understanding of an intersection. Two streets only connect by a node - an intersection is defined by a node. Without a node, two streets do not connect.


The vehicles only consider each other if the streets are connected by a node, not if the streets just pass over each other. You can think of two streets passing over each other as one street being a bridge. The cars don’t ”see” each other. We strictly adhere to the Street-Node concept here. It’s just like in an electrical network where you have wires passing over each other. A connection is only clarified by a node.


