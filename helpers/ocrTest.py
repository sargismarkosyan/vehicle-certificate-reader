import cv2
import numpy as np
from helpers.ocr import parseArm, parseEng

img = cv2.imread('../images/3.jpg')

ownerLineArm = ((804, 518), (3609, 530), (3608, 731), (803, 719))
ownerLineEng = ((584, 691), (2945, 702), (2944, 902), (583, 892))
addressLineArm1 = ((894, 871), (2944, 880), (2943, 1081), (893, 1071))
addressLineArm2 = ((320, 1039), (2943, 1050), (2942, 1251), (320, 1240))
addressLineArm3 = ((320, 1221), (2942, 1232), (2941, 1433), (319, 1421))
addressLineEng1 = ((580, 1400), (2942, 1410), (2941, 1611), (580, 1601))
addressLineEng2 = ((318, 1577), (2941, 1588), (2940, 1789), (317, 1778))
addressLineEng3 = ((317, 1751), (2940, 1763), (2939, 1964), (316, 1952))


def parse(name, parser, cords, quick=False):
    imgCopy = img.copy()
    ownerLineCordsA3 = np.array([cords], dtype=np.int32)
    cv2.polylines(imgCopy, ownerLineCordsA3, True, (0, 0, 255), 6, 8)
    cropImg = imgCopy[cords[0][1]:cords[2][1], cords[0][0]:cords[2][0]]
    cv2.imshow(name, cropImg)
    # cv2.imwrite('../test/' + name + '.png', cropImg)

    print(parser(img, cords, quick=quick))


parse('ownerLineEng', parseEng, ownerLineEng, True)

parse('ownerLineArm', parseArm, ownerLineArm)
parse('ownerLineEng', parseEng, ownerLineEng)
parse('addressLineArm1', parseArm, addressLineArm1)
parse('addressLineArm2', parseArm, addressLineArm2)
parse('addressLineArm3', parseArm, addressLineArm3)
parse('addressLineEng1', parseEng, addressLineEng1)
parse('addressLineEng2', parseEng, addressLineEng2)
parse('addressLineEng3', parseEng, addressLineEng3)

'''
imgHeight, imgWidth, channels = img.shape
cropX = 827
cropY = 563
cropW = 1900
cropH = 200
crop_img = img[cropY:cropY+cropH, cropX:cropX+cropW]

print(parseArm(img, [(cropX, cropY), (cropX + cropW, cropY), (cropX + cropW, cropY + cropH), (cropX, cropY + cropH)]))

crop2X = 547
crop2Y = 723
crop2W = 1500
crop2H = 200
crop2_img = img[crop2Y:crop2Y+crop2H, crop2X:crop2X+crop2W]

print(parseEng(img, [(crop2X, crop2Y), (crop2X + crop2W, crop2Y), (crop2X + crop2W, crop2Y + crop2H), (crop2X, crop2Y + crop2H)]))

cv2.imshow('ARM', crop_img)
cv2.imshow('ENG', crop2_img)
'''

cv2.waitKey(0)
cv2.destroyAllWindows()
