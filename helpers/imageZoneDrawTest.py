import cv2
from config import CARD
from helpers.imageZoneDraw import drawZone

img = cv2.imread('../images/3.jpg')

print(drawZone(img, CARD['width'], CARD['height']))

cv2.imshow('image', cv2.resize(img, (1016, 641)))
cv2.waitKey(0)
cv2.destroyAllWindows()
