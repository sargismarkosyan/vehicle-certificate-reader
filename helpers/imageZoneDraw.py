import cv2

BORDER_SIZE = 15


def findZone(img, boxRatio):
    imgHeight, imgWidth, _ = img.shape
    imgRatio = imgWidth / imgHeight
    smallSide = min(imgWidth, imgHeight)
    border = smallSide * BORDER_SIZE / 100

    if imgRatio > boxRatio:
        boxHeight = imgHeight - (2 * border)
        boxWidth = boxHeight * boxRatio
    else:
        boxWidth = imgWidth - (2 * border)
        boxHeight = boxWidth / boxRatio

    top = int((imgHeight - boxHeight) / 2)
    left = int((imgWidth - boxWidth) / 2)
    right = int(boxWidth + left)
    bottom = int(boxHeight + top)

    return (left, top), (right, bottom)


def drawZone(img, boxWidth, boxHeight):
    ratio = boxWidth / boxHeight
    corners = findZone(img, ratio)

    cv2.rectangle(img, corners[0], corners[1], (255, 255, 255), 10)
    return corners
