import cv2
import numpy as np
import pytesseract

OPTIMAL_HEIGHT = 106
MIN_SIZE_DIFF = 0.3
MAX_SIZE_DIFF = 0.9


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def catPoly(img, cords, withThreshold=True):
    wraped = four_point_transform(img, np.array(cords, dtype=np.int32))
    wrapedHeight, wrapedWidth, _ = wraped.shape
    ratio = wrapedHeight / OPTIMAL_HEIGHT
    if ratio == 0:
        ratio = 1

    wrapedSmall = cv2.resize(wraped, (int(wrapedWidth / ratio), OPTIMAL_HEIGHT))

    if not withThreshold:
        return wrapedSmall

    reduceNoise = cv2.fastNlMeansDenoisingColored(wrapedSmall, None, 10, 10, 7, 21)
    # cv2.imshow('dst', reduceNoise)

    gray = cv2.cvtColor(reduceNoise, cv2.COLOR_BGR2GRAY)

    blured = cv2.medianBlur(gray, 11)
    th = cv2.adaptiveThreshold(blured, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 39, 5)
    # cv2.imshow('th', th)

    return th


def ocrRowValidator(ocrData, index):
    if ocrData['conf'][index] == '-1':
        return False

    if ocrData['height'][index] < OPTIMAL_HEIGHT * MIN_SIZE_DIFF or ocrData['height'][
        index] > OPTIMAL_HEIGHT * MAX_SIZE_DIFF:
        return False

    return True


def filterOCR(ocrData):
    validText = []

    # print((ocrData['text'], ocrData['height']))

    for index, text in enumerate(ocrData['text']):
        if ocrRowValidator(ocrData, index):
            validText.append(text)

    return validText


def parseArm(img, cords, quick=False, psm=6):
    crop = catPoly(img, cords, withThreshold=not quick)

    ocrData = pytesseract.image_to_data(crop, lang='script/Armenian', config='--psm ' + str(psm),
                                        output_type=pytesseract.Output.DICT)
    filteredData = filterOCR(ocrData)
    return ' '.join(filteredData)


def parseEng(img, cords, quick=False, psm=6):
    crop = catPoly(img, cords, withThreshold=not quick)

    '''
    for i in range(3, 13):
        print('----------' + str(i) + '\n')
        print(pytesseract.image_to_string(crop, lang='eng', config='--psm ' + str(i)))
    '''

    ocrData = pytesseract.image_to_data(crop, lang='eng', config='--psm ' + str(psm),
                                        output_type=pytesseract.Output.DICT)
    filteredData = filterOCR(ocrData)
    return ' '.join(filteredData)
