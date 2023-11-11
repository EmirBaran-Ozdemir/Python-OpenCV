import sys

sys.path.append("../")
import cv2
import numpy as np
import os
import time
import random
import importlib

currentFolder = os.getcwd()
parentFolder = os.path.abspath(os.path.join(currentFolder, ".."))
htm = importlib.import_module("HTM.handTrackingModule")


def choosePicture(overlayList):
    randomInteger = random.randint(0, len(overlayList) - 2)
    return overlayList[randomInteger], randomInteger


def calculateScore(maxScore):
    if maxScore == 0:
        return maxScore
    else:
        maxScore -= 10
        return maxScore


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
    maxScore = 2000
    score = 0
    start = False
    raund = 10
    ######################
    # Reading the images
    folderPath = f"{parentFolder}\\assets\\assetsHandPoses"
    myList = os.listdir(folderPath)
    overlayList = []
    for imgPath in myList:
        img = cv2.imread(f"{folderPath}/{imgPath}")
        overlayList.append(img)

    # Hand detection
    detector = htm.handDetector(
        modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9
    )
    # Video capture and set display
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        succes, img = cap.read()
        # Flip and correct camera
        img = cv2.flip(img, 1)
        # Adding detected hands to the img
        img = detector.findHands(img=img, draw=False)
        lmList, _ = detector.findPosition(img=img, draw=False)
        # Game continues while raund greater than zero
        if raund > 0:
            cv2.putText(
                img,
                f"Raund left {raund}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            if len(lmList) != 0:
                # Define finger indexes
                fingers = detector.fingersUp(
                    img=img, draw=False, circleRadius=10, circleColor=(0, 0, 0)
                )
                # Pose display and user pose check if new pose generated
                if not correctPose:
                    img[29:129, int(wCam / 2 - 50) : int(wCam / 2 + 50)] = posePicture
                    correctPose = comparePoses(poseIndex, fingers)
                # Generate new pose if users pose correct or this is first raund
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
                        raund -= 1
                # If pose generated timer starts
                if start:
                    maxScore = calculateScore(maxScore)
                    # Current pose score
                    cv2.putText(
                        img,
                        f"Pose Score:{maxScore}",
                        (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                    # Calculate score if user poses correctly
                    if correctPose:
                        score += maxScore
                        start = False
                        maxScore = 2000
                else:
                    cv2.putText(
                        img,
                        f"To Start Raund:",
                        (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                    img[180:280, 10:110] = overlayList[len(overlayList) - 1]
        else:
            cv2.putText(
                img,
                f"Game Over",
                (int(wCam / 2 - 300), int(hCam / 2 - 40)),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                5,
            )
            # SCORE DISPLAY
            cv2.putText(
                img,
                f"Total Score:{score}",
                (int(wCam / 2 - 200), int(hCam / 2 + 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
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
            (1150, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 0),
            2,
        )
        # DISPLAY
        cv2.imshow("Hand Poses Challenge", img)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()
