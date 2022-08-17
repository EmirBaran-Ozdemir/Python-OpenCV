# TechVidvan Object detection of similar color
import cv2
import numpy as np
import os

# Reading the image
folderPath = "assets"
myList = os.listdir(folderPath)
overlayList = []
for imgPath in myList:
    img = cv2.imread(f"{folderPath}/{imgPath}")
    overlayList.append(img)


# convert to hsv colorspace
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower bound and upper bound for Green color
lower_bound = np.array([50, 20, 20])
upper_bound = np.array([100, 255, 255])
# find the colors within the boundaries
mask = cv2.inRange(hsv, lower_bound, upper_bound)
# Showing the output
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
