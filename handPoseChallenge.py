import cv2
import numpy as np
import os
import handTrackingModule as htm
import time
import random


def choosePicture(overlayList):
    randomInteger = random.randint(0, len(overlayList) - 1)
    return overlayList[randomInteger], randomInteger


def calculateScore(score):
    if score == 0:
        return score
    else:
        score -= 10
        return score


def comparePoses(poseIndex, fingers):
    # All fingers open
    if poseIndex == 0:
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            correctPose = True
            return correctPose
    # Index and middle finger open
    if poseIndex == 1:
        if (
            not fingers[0]
            and fingers[1]
            and fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):
            correctPose = True
            return correctPose
    # Index finger open
    if poseIndex == 2:
        if (
            not fingers[0]
            and fingers[1]
            and not fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):
            correctPose = True
            return correctPose
    # Little finger open
    if poseIndex == 3:
        if (
            not fingers[0]
            and not fingers[1]
            and not fingers[2]
            and not fingers[3]
            and fingers[4]
        ):
            correctPose = True
            return correctPose
    # Little and ring finger closed
    if poseIndex == 4:
        if (
            fingers[0]
            and fingers[1]
            and fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb closed
    if poseIndex == 5:
        if not fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            correctPose = True
            return correctPose
    # Thumb and index finger closed
    if poseIndex == 6:
        if (
            not fingers[0]
            and not fingers[1]
            and fingers[2]
            and fingers[3]
            and fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb and little finger closed
    if poseIndex == 7:
        if (
            not fingers[0]
            and fingers[1]
            and fingers[2]
            and fingers[3]
            and not fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb and little finger open
    if poseIndex == 8:
        if (
            fingers[0]
            and not fingers[1]
            and not fingers[2]
            and not fingers[3]
            and fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb and middle finger closed
    if poseIndex == 9:
        if (
            not fingers[0]
            and fingers[1]
            and not fingers[2]
            and fingers[3]
            and fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb open
    if poseIndex == 10:
        if (
            fingers[0]
            and not fingers[1]
            and not fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):
            correctPose = True
            return correctPose
    # Thumb and ring finger open
    if poseIndex == 11:
        if (
            not fingers[0]
            and fingers[1]
            and fingers[2]
            and not fingers[3]
            and fingers[4]
        ):
            correctPose = True
            return correctPose


def main():
    # VARIABLES
    ######################
    wCam, hCam = 1280, 720
    pTime = 0
    cTime = 0
    correctPose = True
    maxScore = 200
    score = 0
    start = True
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
        img = detector.findHands(img=img, draw=False)
        lmList, bbox = detector.findPosition(img=img, draw=False)

        if len(lmList) != 0:
            # FINGER INDEXES
            fingers = detector.fingersUp(img=img, draw=True)
            # If users pose incorrect
            if not correctPose:
                img[29:100, int(wCam / 2 - 35.5) : int(wCam / 2 + 35.5)] = posePicture
                correctPose = comparePoses(poseIndex, fingers)

            # New pose if users pose correct or
            else:
                if (
                    not fingers[0]
                    and not fingers[1]
                    and not fingers[2]
                    and not fingers[3]
                    and not fingers[4]
                ):
                    posePicture, poseIndex = choosePicture(overlayList)
                    correctPose = False
                    start = True
            if start:
                maxScore == calculateScore(maxScore)
                if correctPose:
                    score += maxScore
                    start == False
        # SCORE DISPLAY
        cv2.putText(
            img,
            f"Score:{score}",
            (10, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            2,
        )
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
