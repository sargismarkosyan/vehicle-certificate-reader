import cv2
import numpy as np
from helpers.getCornersFrom2Points import getCorners

boxWidth = 100
boxHeight = 50
point1 = (230, 205) #x, y
point2 = (280, 240)
distPoint1 = (30, 5)
distPoint2 = (80, 40)

cords = getCorners(point1, point2, distPoint1, distPoint2, boxWidth, boxHeight)

img = np.zeros((500, 800, 3), np.uint8)
cv2.circle(img, point1, 0, (0, 0, 255), 3)
cv2.circle(img, point2, 0, (0, 0, 255), 3)
cv2.circle(img, cords[0], 0, (0, 255, 0), 3)
cv2.circle(img, cords[1], 0, (0, 255, 0), 3)
cv2.circle(img, cords[2], 0, (0, 255, 0), 3)
cv2.circle(img, cords[3], 0, (0, 255, 0), 3)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
