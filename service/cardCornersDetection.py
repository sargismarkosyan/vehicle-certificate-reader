import cv2
from config import CARD
from helpers.getCornersFrom2Points import getCorners
from helpers.sizeValidator import validateCords
from helpers.templateSearch import findTemplates

templateSrc = ['templates/front/title_am.jpg', 'templates/front/armenia.jpg']


def smartTemplateLoader(src):
    img = cv2.imread(src, 0)
    if img is None:
        return cv2.imread('../' + src, 0)

    return img


templates = list(map(lambda src: smartTemplateLoader(src), templateSrc))


def getCenter(topLeft, bottomRight):
    midX = (bottomRight[0] + topLeft[0]) / 2
    midY = (bottomRight[1] + topLeft[1]) / 2
    return midX, midY


titleAmCenter = (CARD['front']['titleAM']['left'], CARD['front']['titleAM']['top'])
armeniaCenter = (CARD['front']['armenia']['left'], CARD['front']['armenia']['top'])


def getCornersFromTemplates(templateCords):
    return getCorners(templateCords[0][0], templateCords[1][0], titleAmCenter, armeniaCenter, CARD['width'],
                      CARD['height'])


def cornersValidator(templateCords, meth, screenWidth, screenHeight):
    maxDist = 10 * max(screenWidth, screenHeight) / 100

    cords = getCornersFromTemplates(templateCords)
    return validateCords(cords, screenWidth, screenHeight, 10, maxDist)


def resizeTemplate(template, templateWidthRatio, templateHeightRatio):
    templateHeight, templateWidth = template.shape
    return cv2.resize(template, (int(templateWidthRatio * templateWidth), int(templateHeightRatio * templateHeight)))


def findCorners(img):
    screenHeight, screenWidth, channels = img.shape
    templateWidthRatio = screenWidth / CARD['width']
    templateHeightRatio = screenHeight / CARD['height']

    resizedTemplates = list(
        map(lambda template: resizeTemplate(template, templateWidthRatio, templateHeightRatio), templates))

    templateCords = findTemplates(img, resizedTemplates,
                                  lambda cords, meth: cornersValidator(cords, meth, screenWidth, screenHeight))
    if templateCords == None:
        return templateCords

    boxCords = getCornersFromTemplates(templateCords)
    if boxCords == None:
        return boxCords

    return templateCords, boxCords
