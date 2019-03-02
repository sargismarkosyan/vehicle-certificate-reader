import math
import numpy as np


def getLineAngleFrom2Points(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    if (y2 - y1) == 0:
        m = 0
    elif (x2 - x1) == 0:
        if (y2 - y1) > 0:
            return math.pi / 2
        else:
            return -math.pi / 2
    else:
        m = (y2 - y1) / (x2 - x1)

    return np.arctan(m)


def getScaleFromPoints(scaledPoint1, scaledPoint2, originalPoint1, originalPoint2):
    scaledPointX = scaledPoint2[0] - scaledPoint1[0]
    scaledPointY = scaledPoint2[1] - scaledPoint1[1]
    originalPointX = originalPoint2[0] - originalPoint1[0]
    originalPointY = originalPoint2[1] - originalPoint1[1]
    scaledAnesthesia = math.sqrt(math.pow(scaledPointX, 2) + math.pow(scaledPointY, 2))
    originalAnesthesia = math.sqrt(math.pow(originalPointX, 2) + math.pow(originalPointY, 2))

    return scaledAnesthesia / originalAnesthesia


def getCordsInOtherSystem(point, cordStart, cordAngle):
    a = cordStart[0]
    b = cordStart[1]
    x_p = point[0]
    y_p = point[1]

    x = a + (x_p * math.cos(cordAngle)) - (y_p * math.sin(cordAngle))
    y = b + (x_p * math.sin(cordAngle)) + (y_p * math.cos(cordAngle))
    return int(x), int(y)


def getContentCorners(corners, fieldTopLeft, fieldWidth, fieldHeight, boxWidth, boxHeight):
    point1 = corners[0]
    point2 = corners[2]
    distPoint1 = (-fieldTopLeft[0], -fieldTopLeft[1])
    distPoint2 = (boxWidth - fieldTopLeft[0], boxHeight - fieldTopLeft[1])

    return getCorners(point1, point2, distPoint1, distPoint2, fieldWidth, fieldHeight)


def getCorners(point1, point2, distPoint1, distPoint2, boxWidth, boxHeight):
    angleOfPointsLineFromBox = getLineAngleFrom2Points(distPoint1, distPoint2)
    angleOfPointsLineFromCords = getLineAngleFrom2Points(point1, point2)
    angleOfBoxFromCords = angleOfPointsLineFromCords - angleOfPointsLineFromBox

    scale = getScaleFromPoints(point1, point2, distPoint1, distPoint2)
    scaledDistPoint1 = (distPoint1[0] * scale, distPoint1[1] * scale)
    scaledBoxWidth = boxWidth * scale
    scaledBoxHeight = boxHeight * scale

    boxTopLeftFromPoint1 = (-scaledDistPoint1[0], -scaledDistPoint1[1])
    boxTopRightFromPoint1 = (-scaledDistPoint1[0] + scaledBoxWidth, -scaledDistPoint1[1])
    boxBottomLeftFromPoint1 = (-scaledDistPoint1[0], -scaledDistPoint1[1] + scaledBoxHeight)
    boxBottomRightFromPoint1 = (-scaledDistPoint1[0] + scaledBoxWidth, -scaledDistPoint1[1] + scaledBoxHeight)

    boxTopLeft = getCordsInOtherSystem(boxTopLeftFromPoint1, point1, angleOfBoxFromCords)
    boxTopRight = getCordsInOtherSystem(boxTopRightFromPoint1, point1, angleOfBoxFromCords)
    boxBottomLeft = getCordsInOtherSystem(boxBottomLeftFromPoint1, point1, angleOfBoxFromCords)
    boxBottomRight = getCordsInOtherSystem(boxBottomRightFromPoint1, point1, angleOfBoxFromCords)

    return boxTopLeft, boxTopRight, boxBottomRight, boxBottomLeft
