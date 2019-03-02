from helpers.sizeValidator import validateCords

screenWidth = 100
screenHeight = 50
maxAngleDiff = 10
maxDistance = 10
cords = ((0, 0), (100, 0), (100, 50), (0, 50))

print(validateCords(cords, screenWidth, screenHeight, maxAngleDiff, maxDistance))