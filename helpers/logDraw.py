import numpy as np
from PIL import ImageFont, ImageDraw, Image

FONT_SIZE = 0.025
LINE_SPACE = FONT_SIZE / 2


def drawLogs(img, fontPath, logs):
    top = 10
    left = 10
    fontSizeLocal = int(img.shape[0] * FONT_SIZE)
    lineSpaceLocal = int(img.shape[0] * LINE_SPACE)
    imgPil = Image.fromarray(img)
    draw = ImageDraw.Draw(imgPil)
    font = ImageFont.truetype(fontPath, fontSizeLocal)

    for index, log in enumerate(logs):
        lineTop = top + (index * (fontSizeLocal + lineSpaceLocal))
        draw.text((left, lineTop), log.replace('\n', ' '), font=font, fill=(255, 255, 255))

    return np.array(imgPil)
