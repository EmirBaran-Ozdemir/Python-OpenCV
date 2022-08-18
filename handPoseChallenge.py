import cv2
import numpy as np
import os
import handTrackingModule as htm
import time
import random


def choosePicture(overlayList):
    randomInteger = random.randint(0, len(overlayList) - 1)
    return overlayList[randomInteger]

def main():
    # VARIABLES
    ######################
    wCam, hCam = 1280, 720
    xp, yp = 0, 0
    pTime = 0
    cTime = 0
    ######################
    # Reading the images
    folderPath = "assets\\assetsHandPoseChallenge"
    myList = os.listdir(folderPath)
    overlayList = []
    for imgPath in myList:
        img = cv2.imread(f"{folderPath}/{imgPath}")
        overlayList.append(img)

    # DETECTOR
    detector = htm.handDetector(
        modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9
    )
    # VIDEO CAPTURE
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    imgCanvas = np.zeros((hCam, wCam, 3), np.uint8)

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
            #If pose not true
            if not correctPose:
                if choosePicture(1):
                    if (not fingers[0] 
                    and fingers[1] 
                    and fingers[2] 
                    and fingers[3] 
                    and fingers[4]):
                        correctPose = True
            #If user poses true
            else:
                if (fingers[0] 
                and not fingers[1] 
                and not fingers[2] 
                and not fingers[3] 
                and not fingers[4]):
                    header = choosePicture(overlayList)
                    img[29:100, int(wCam / 2 - 35.5) : int(wCam / 2 + 35.5)] = header
                    correctPose =  False
                
                    
            

        # FRAME RATE
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # FPS COUNTER
        cv2.putText(
            img,
            f"FPS:{int(fps)}",
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            2,
        )
        # DISPLAY

        cv2.imshow("Hand Poses Challenge", img)

        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()
