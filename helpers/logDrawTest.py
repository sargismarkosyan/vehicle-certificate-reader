import cv2
from helpers.logDraw import drawLogs

img = cv2.imread('../images/3.jpg')

imgWithLogs = drawLogs(img, '../fonts/ARIALUNI.TTF', ['Name: James', 'Name Arm: Սարգիս', 'Age: 25'])

cv2.imshow('image with logs', cv2.resize(imgWithLogs, (1016, 641)))
cv2.waitKey(0)
cv2.destroyAllWindows()
