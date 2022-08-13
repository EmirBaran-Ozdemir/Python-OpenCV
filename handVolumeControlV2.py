import cv2
import numpy as np
import sys
import os
import handTrackingModule as htm
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
 
######################
wCam, hCam = 1080, 960
pTime = 0
cTime = 0
volBar = 400
volPer = 0
area = 0
######################

# PYCAW TEMPLATE
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

detector = htm.handDetector(modelComplex=0, maxHands=1, detectionCon=0.8, trackCon=0.8)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# Function Start
while True:
    succes, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        if 200 < area < 1500:
            fingers = detector.fingersUp(img=img, draw=False)
            if not fingers[4]:
                lenght, img, lineInfo = detector.findDistance(
                    p1=4, p2=8, img=img, draw=False
                )
                volBar = np.interp(lenght, [50, 250], [400, 150])
                volPer = np.interp(lenght, [50, 250], [0, 100])
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)

    # FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = cv2.flip(img, 1)
    # VOLUME BAR
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(
        img, f"%:{int(cVol)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2
    )
    # FPS COUNTER
    cv2.putText(
        img, f"FPS:{int(fps)}", (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2
    )
    # DISPLAY
    cv2.imshow("Windw", img)
    if cv2.waitKey(1) == ord("q"):
        break
