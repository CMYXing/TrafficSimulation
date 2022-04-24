from tkinter import LAST, CENTER
import numpy as np

import Parameter
LANE_WIDTH = Parameter.get_value('LANEWIDTH')
scale = Parameter.get_value('SCALE')



# This method draws the street network given to it
def drawStreetNetwork(canvas, streetNetwork):
    for street in streetNetwork.streets:
        text = __drawStreet(canvas, street)

    for customNode in streetNetwork.getAllNodesWhereProbabilityCanBeCustomized():
        __drawCustomNode(canvas, customNode)


def __drawStreet(canvas, street):

    # Use the canvas to draw streets on it
    streetWidth = len(street.lanes) * LANE_WIDTH

    #draw the street itself


    #draw the connection point of the street
    __drawCircleWith(canvas, street.startConnectionPoint.xCoordinate, street.startConnectionPoint.yCoordinate, streetWidth/2, fill="white")
    __drawCircleWith(canvas, street.endConnectionPoint.xCoordinate, street.endConnectionPoint.yCoordinate, streetWidth/2, fill="white")

    text = __drawLanes(canvas, street)

    __drawDirectionArrowOnStreet(canvas, street)

    return text


def __drawCircleWith(canvas, centerPointX, centerPointY, radius, fill):
    # Ovals (or circles) in tkinter are drawn from one corner to the other
    # however, we want to draw a circle with a center point and a radius
    # so we have to determine the corner coordinates first
    upperLeftCornerX = centerPointX - radius
    upperLeftCornerY = centerPointY - radius

    lowerRightCornerX = centerPointX + radius
    lowerRightCornerY = centerPointY + radius

    return canvas.create_oval(upperLeftCornerX, upperLeftCornerY, lowerRightCornerX, lowerRightCornerY, fill=fill, outline="")


def __drawLanes(canvas, street):
    for lane in street.lanes:
        laneStart, laneEnd = lane.getStartAndEndPoint()

        if street.isTunnel:
            tunnelLine = canvas.create_line(laneStart[0], laneStart[1],
                            laneEnd[0], laneEnd[1],
                            width=LANE_WIDTH - 4, fill="darkgrey")
            canvas.lower(tunnelLine)
        else:
            canvas.create_line(laneStart[0], laneStart[1],
                           laneEnd[0], laneEnd[1],
                           width = LANE_WIDTH-4, fill="white")

    if Parameter.get_value('show_road_ID'):
        text = canvas.create_text((laneStart[0]+laneEnd[0])/2, (laneStart[1]+laneEnd[1])/2, anchor=CENTER,
                       text=str(street.id) + '(' + str(int(street.getLength()/scale)) + ' m)', fill="red")
        canvas.lift(text)



def __drawDirectionArrowOnStreet(canvas, street):
    streetVector = street.getStreetVector()
    arrowStart = np.array([street.startConnectionPoint.xCoordinate, street.startConnectionPoint.yCoordinate]) + streetVector*0.4
    arrowEnd = np.array([street.endConnectionPoint.xCoordinate, street.endConnectionPoint.yCoordinate]) - streetVector*0.4

    arrow = canvas.create_line(arrowStart[0], arrowStart[1], arrowEnd[0], arrowEnd[1], arrow=LAST, fill="lightgrey")
    if street.isTunnel:
        canvas.lower(arrow)


def __drawCustomNode(canvas, customNode):
    if Parameter.get_value('show_road_ID'):
        __drawCircleWith(canvas, customNode.xCoordinate,
                         customNode.yCoordinate,
                         LANE_WIDTH / 2, fill="Sea Green1")
        canvas.create_text(customNode.xCoordinate, customNode.yCoordinate, anchor=CENTER,
                           text=customNode.id)


