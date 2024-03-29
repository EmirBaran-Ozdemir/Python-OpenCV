import sys

sys.path.append("../")
import cv2
import numpy as np
import time
import os
from collections import deque
import importlib

currentFolder = os.getcwd()
parentFolder = os.path.abspath(os.path.join(currentFolder, ".."))
htm = importlib.import_module("HTM.handTrackingModule")
# VARIABLES
######################
wCam, hCam = 1280, 720
color = (255, 255, 0)
brushTickness = 10
x1, y1 = 0, 0
xp, yp = 0, 0
pTime = 0
cTime = 0
######################

# PHOTO FOLDER
folderPath = f"{parentFolder}\\assets\\assetsHandPaint"
myList = os.listdir(folderPath)
overlayList = []
for imgPath in myList:
    image = cv2.imread(f"{folderPath}/{imgPath}")
    overlayList.append(image)

# DETECTOR
detector = htm.handDetector(modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9)
# VIDEO CAPTURE
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
while True:
    succes, img = cap.read()
    # FLIP
    img = cv2.flip(img, 1)
    # HAND FIND
    img = detector.findHands(img, draw=False)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # FINGER INDEXES
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]
        fingers = detector.fingersUp(img=img, draw=False)
        # If little finger and thumb is closed board activates
        if not fingers[0] and not fingers[4]:
            if fingers[1] and fingers[2] and fingers[3]:
                # PHOTO SET
                header = np.concatenate(
                    (overlayList[0], overlayList[2], overlayList[3]), axis=1
                )
                # PLACING PHOTOS
                img[0:150, 640 - 225 : 640 + 225] = header
                if y2 < 155:
                    if 415 < x2 < 565:
                        color = (255, 255, 0)
                    elif 565 < x2 < 715:
                        color = (0, 255, 0)
                    elif 715 < x2 < 865:
                        color = (0, 0, 255)
                xp, yp = 0, 0
            elif fingers[1] and fingers[2] and not fingers[3]:
                cv2.rectangle(
                    img, (x1, y1 + 30), (x2, y1 - 20), (255, 255, 255), cv2.FILLED
                )

                header = overlayList[1]
                xp, yp = 0, 0
                img[0:150, 640 - 75 : 640 + 75] = header

                cv2.rectangle(
                    imgCanvas, (x1, y1 + 30), (x2, y1 - 20), (0, 0, 0), cv2.FILLED
                )
            elif fingers[1] and not fingers[2] and not fingers[3]:
                if color == (255, 255, 0):  # BLUE
                    header = overlayList[0]
                elif color == (0, 255, 0):  # GREEN
                    header = overlayList[2]
                elif color == (0, 0, 255):  # RED
                    header = overlayList[3]
                img[0:150, 640 - 75 : 640 + 75] = header
                cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv2.line(img, (xp, yp), (x1, y1), color, brushTickness)

                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushTickness)
                xp, yp = x1, y1
            else:
                xp, yp = 0, 0
        else:
            xp, yp = 0, 0
    else:
        xp, yp = 0, 0

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    # Calculate the dimensions of imgCanvas
    canvasHeight, canvasWidth, _ = imgCanvas.shape

    # Resize img to match the dimensions of imgCanvas
    img = cv2.resize(img, (canvasWidth, canvasHeight))

    # Perform the bitwise AND operation
    img = cv2.bitwise_and(img, imgInv)

    img = cv2.bitwise_or(img, imgCanvas)
    # FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # FPS COUNTER
    cv2.putText(
        img, f"FPS:{int(fps)}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2
    )
    # DISPLAY
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("handPaint", img)
    # cv2.imshow("canvas",imgCanvas)
    if cv2.waitKey(1) == ord("q"):
        break
