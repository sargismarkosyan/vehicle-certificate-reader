import numpy as np
from helpers.getCornersFrom2Points import getLineAngleFrom2Points


def validateCords(cords, screenWidth, screenHeight, maxAngleDiff, maxDistance):
    boxTopLeft = cords[0]
    boxTopRight = cords[1]
    boxBottomRight = cords[2]

    angle = getLineAngleFrom2Points(boxTopLeft, boxTopRight)
    if np.rad2deg(angle) > maxAngleDiff or np.rad2deg(angle) < -maxAngleDiff:
        return False

    if boxTopLeft[0] < -maxDistance or \
            boxTopLeft[0] > maxDistance or \
            boxTopLeft[1] < -maxDistance or \
            boxTopLeft[1] > maxDistance or \
            boxBottomRight[0] < screenWidth - maxDistance or \
            boxBottomRight[0] > screenWidth + maxDistance or \
            boxBottomRight[1] < screenHeight - maxDistance or \
            boxBottomRight[1] > screenHeight + maxDistance:
        return False

    return True
