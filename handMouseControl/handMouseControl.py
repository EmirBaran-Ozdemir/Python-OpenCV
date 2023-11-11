import sys

sys.path.append("../")
import cv2
import numpy as np
import os

import time
import random
import importlib
import win32api, win32con


def move(x, y):
    SCREEN_WIDTH = win32api.GetSystemMetrics(0)
    SCREEN_HEIGHT = win32api.GetSystemMetrics(1)
    x += SCREEN_WIDTH / 2
    y += SCREEN_HEIGHT / 2
    x = x / SCREEN_WIDTH * 65535.0
    y = -(y / SCREEN_HEIGHT * 65535.0)
    # Pointer position
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
        int(x),
        int(y),
    )


def click(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)


def release(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def main():
    htm = importlib.import_module("HTM.handTrackingModule")

    ##############VARIABLES#######################
    CAM_WIDTH, CAM_HEIGHT = 1280, 720
    SCREEN_WIDTH = win32api.GetSystemMetrics(0)
    SCREEN_HEIGHT = win32api.GetSystemMetrics(1)
    pTime = 0
    cTime = 0
    currLocation_x, currLocation_y = 0, 0
    prevLocation_x, prevLocation_y = 0, 0
    SMOOTHNESS = 10
    clicked = False
    # Getting 70 percent of width so hand won't be out
    WIDTH_RATIO = SCREEN_WIDTH / (CAM_WIDTH * 0.23)
    # Getting 70 percent of height so hand won't be out
    HEIGHT_RATIO = SCREEN_HEIGHT / (CAM_HEIGHT * 0.23)
    ##############################################
    # Hand detection
    detector = htm.handDetector(
        modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9
    )
    # Video capture and set display
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)
    i = 0
    while True:
        succes, img = cap.read()
        # Flip and correct camera
        img = cv2.flip(img, 1)
        # Adding detected hands to the img
        img = detector.findHands(img=img, draw=True)
        lmList, _ = detector.findPosition(img=img, draw=False)
        # Hand tracking continues while hand detected
        if len(lmList) != 0:
            # Index finger position
            # x = width, y = height
            #! https://editor.analyticsvidhya.com/uploads/2410344.png
            hand_x, hand_y = lmList[9][1], lmList[9][2]
            indexTIP_x, indexTIP_y = lmList[8][1], lmList[8][2]
            indexMCP_x, indexMCP_y = lmList[5][1], lmList[5][2]
            wrist_x, wrist_y = lmList[0][1], lmList[0][2]
            pinkyMCP_x, pinkyMCP_y = lmList[14][1], lmList[14][2]

            # Preventing cursor shake
            currLocation_x = int(
                prevLocation_x + (hand_x - prevLocation_x) / SMOOTHNESS
            )
            currLocation_y = int(
                prevLocation_y + (hand_y - prevLocation_y) / SMOOTHNESS
            )
            # Define finger indexes
            # fingers = detector.fingersUp(
            #     img=img, draw=False, circleRadius=10, circleColor=(0, 0, 0)
            # )

            # Setting middle as origin
            move(
                (currLocation_x - (CAM_WIDTH * 0.35)) * WIDTH_RATIO,
                (currLocation_y - (CAM_HEIGHT * 0.5)) * HEIGHT_RATIO,
            )
            prevLocation_x, prevLocation_y = currLocation_x, currLocation_y
            i += 1
            if i % 100 == 0:
                print((indexTIP_y - indexMCP_y))
                #! (160, 210)
                print((wrist_y / pinkyMCP_y))
                #! (-0.062, 0.208)
            if indexTIP_y - indexMCP_y > 30:
                if clicked:
                    release(currLocation_x, currLocation_y)
                    clicked = False
            elif indexTIP_y - indexMCP_y <= 30:
                if not clicked:
                    click(currLocation_x, currLocation_y)
                    clicked = True
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
        cv2.imshow("Hand Mouse Control", img)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()
