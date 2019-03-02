import cv2
import urllib.request
import numpy as np
from helpers.templateSearch import findTemplates

usePhoneCamera = False
templateSrc = ['../templates/title_am.jpg', '../templates/number_4_mutated.jpg']
templates = list(map(lambda src: cv2.imread(src, 0), templateSrc))


def validator(cords, meth):
    imageClone = img.copy()

    for idx, cord in enumerate(cords):
        color = [0, 0, 0]
        color[idx] = 255

        cv2.rectangle(imageClone, cord[0], cord[1], tuple(color), 2)

    cv2.imshow(meth, cv2.resize(imageClone, (1016, 641)))
    return False


if usePhoneCamera:
    cv2.waitKey(1)

    while True:
        req = urllib.request.urlopen('http://192.168.2.104:8080/shot.jpg')
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        findTemplates(img, templates, validator)
else:
    img = cv2.imread('../images/3.jpg', -1)
    findTemplates(img, templates, validator)
    cv2.waitKey(0)

cv2.destroyAllWindows()
