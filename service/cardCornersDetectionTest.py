import cv2
import numpy as np
from config import CARD
from helpers.getCornersFrom2Points import getContentCorners
from service.cardCornersDetection import findCorners
from helpers.ocr import parseArm, parseEng

# img = cv2.imread('../images/front.jpg', cv2.IMREAD_COLOR)
img = cv2.imread('../images/3.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('../images/4.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('../images/20190227_223451.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('../images/20190227_223532.jpg', cv2.IMREAD_COLOR)

cords = findCorners(img)
if cords == None:
    raise Exception('No cords!')

templateCords, boxCords = cords

a3 = np.array([boxCords], dtype=np.int32)
cv2.polylines(img, a3, True, (0, 255, 0), 6, 8)

for cord in templateCords:
    cv2.rectangle(img, cord[0], cord[1], (255, 0, 0), 6)


def addField(field, parser):
    ownerLineCords = getContentCorners(boxCords, (field['left'], field['top']), field['width'], field['height'],
                                       CARD['width'], CARD['height'])
    ownerLineCordsA3 = np.array([ownerLineCords], dtype=np.int32)
    cv2.polylines(img, ownerLineCordsA3, True, (0, 0, 255), 6, 8)
    print(parser(img, ownerLineCords))


addField(CARD['front']['ownerLineArm'], parseArm)
addField(CARD['front']['ownerLineEng'], parseEng)
addField(CARD['front']['addressLineArm1'], parseArm)
addField(CARD['front']['addressLineArm2'], parseArm)
addField(CARD['front']['addressLineArm3'], parseArm)
addField(CARD['front']['addressLineEng1'], parseEng)
addField(CARD['front']['addressLineEng2'], parseEng)
addField(CARD['front']['addressLineEng3'], parseEng)

cv2.imshow('cords', cv2.resize(img, (645, 405)))
cv2.waitKey(0)

cv2.destroyAllWindows()
