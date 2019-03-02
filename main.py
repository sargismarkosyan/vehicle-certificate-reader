import re
import cv2
import urllib.request
import numpy as np
from config import CARD
from helpers.ocr import parseArm, parseEng
from helpers.logDraw import drawLogs
from helpers.imageZoneDraw import drawZone
from helpers.getCornersFrom2Points import getContentCorners
from service.cardCornersDetection import findCorners

OPTIMAL_HEIGHT = 600
FONT_SRC = 'fonts/ARIALUNI.TTF'
NAME_EN_REGEXR = r'^[A-Z ]+$'

useVideoCamera = False
usePhoneCamera = True
logs = ['']


def addZoneToCords(zoneCords, point):
    return point[0] + zoneCords[0][0], point[1] + zoneCords[0][1]


def addField(img, imgWithField, boxCords, field, parser):
    cords = getContentCorners(boxCords, (field['left'], field['top']), field['width'], field['height'],
                              CARD['width'], CARD['height'])
    cordsA3 = np.array([cords], dtype=np.int32)
    cv2.polylines(imgWithField, cordsA3, True, (0, 0, 255), 6, 8)
    return parser(img, cords)


def showImage(img):
    imgRatio = img.shape[0] / OPTIMAL_HEIGHT
    imgSmall = cv2.resize(img, (int(img.shape[1] / imgRatio), OPTIMAL_HEIGHT))
    cv2.imshow('front', imgSmall)


def process(img):
    global logs

    zoneCords = drawZone(img, CARD['width'], CARD['height'])

    zone = img[zoneCords[0][1]:zoneCords[1][1], zoneCords[0][0]:zoneCords[1][0]]
    cords = findCorners(zone)
    if cords == None:
        logs[0] = 'No cords!'
        showImage(drawLogs(img, FONT_SRC, logs))
        return

    templateCords, boxCords = cords
    zoneBoxCords = list(map(lambda cord: addZoneToCords(zoneCords, cord), boxCords))

    cv2.polylines(img, np.array([zoneBoxCords], dtype=np.int32), True, (0, 255, 0), 6, 8)

    for cord in templateCords:
        cv2.rectangle(img, addZoneToCords(zoneCords, cord[0]), addZoneToCords(zoneCords, cord[1]), (255, 0, 0), 6)

    showImage(drawLogs(img, FONT_SRC, logs))
    cv2.waitKey(1)

    engCords = getContentCorners(zoneBoxCords,
                                 (CARD['front']['ownerLineEng']['left'], CARD['front']['ownerLineEng']['top']),
                                 CARD['front']['ownerLineEng']['width'], CARD['front']['ownerLineEng']['height'],
                                 CARD['width'], CARD['height'])
    engName = parseEng(img, engCords, True)

    imgWithField = img.copy()

    if not (re.match(NAME_EN_REGEXR, engName) is None):
        del logs[1:]
        logs[0] = ''
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['ownerLineArm'], parseArm))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['ownerLineEng'], parseEng))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineArm1'], parseArm))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineArm2'], parseArm))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineArm3'], parseArm))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineEng1'], parseEng))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineEng2'], parseEng))
        logs.append(addField(img, imgWithField, zoneBoxCords, CARD['front']['addressLineEng3'], parseEng))

    imgWithField = drawLogs(imgWithField, FONT_SRC, logs)

    showImage(imgWithField)


if usePhoneCamera:
    while True:
        req = urllib.request.urlopen('http://192.168.2.104:8080/shot.jpg')
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        process(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

elif useVideoCamera:
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()

        process(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
else:
    img = cv2.imread('images/main-test.jpg', -1)
    process(img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
