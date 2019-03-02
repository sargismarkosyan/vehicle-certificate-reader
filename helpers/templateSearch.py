import cv2

# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
methods = ['cv2.TM_CCOEFF_NORMED']


def findSingleTeimplate(preparedImg, template, method):
    templateHeight, templateWidth = template.shape

    res = cv2.matchTemplate(preparedImg, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + templateWidth, top_left[1] + templateHeight)
    return top_left, bottom_right


def findTemplates(img, templates, validationFunc):
    preparedImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for meth in methods:
        method = eval(meth)
        cords = list(map(lambda template: findSingleTeimplate(preparedImg, template, method), templates))

        if validationFunc(cords, meth):
            return cords
