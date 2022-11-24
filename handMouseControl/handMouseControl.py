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
    y = y / SCREEN_HEIGHT * 65535.0
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
    htm = importlib.import_module("Python-OpenCV.HTM.handTrackingModule")

    ##############VARIABLES#######################
    CAM_WIDTH, CAM_HEIGHT = 1280, 720
    SCREEN_WIDTH = win32api.GetSystemMetrics(0)
    SCREEN_HEIGHT = win32api.GetSystemMetrics(1)
    pTime = 0
    cTime = 0
    currLocationx, currLocationy = 0, 0
    prevLocationx, prevLocationy = 0, 0
    SMOOTHNESS = 6.5
    clicked = False
    # Getting 70 percent of height so hand won't be out
    WIDTH_RATIO = SCREEN_WIDTH / ((CAM_WIDTH - (CAM_WIDTH * 0.03)) * 0.35)
    # Getting 70 percent of height so hand won't be out
    HEIGHT_RATIO = SCREEN_HEIGHT / ((CAM_HEIGHT - (CAM_HEIGHT * 0.3)) * 0.35)
    ##############################################
    # Hand detection
    detector = htm.handDetector(
        modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9
    )
    # Video capture and set display
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    while True:
        succes, img = cap.read()
        # Flip and correct camera
        img = cv2.flip(img, 1)
        # Adding detected hands to the img
        img = detector.findHands(img=img, draw=False)
        lmList, _ = detector.findPosition(img=img, draw=False)
        # Game continues while raund greater than zero
        if len(lmList) != 0:
            # Index finger position
            # x = width, y = height
            x1, y1 = lmList[8][1], lmList[8][2]
            # Stopping shaking
            currLocationx = int(prevLocationx + (x1 - prevLocationx) / SMOOTHNESS)
            currLocationy = int(prevLocationy + (y1 - prevLocationy) / SMOOTHNESS)
            # Define finger indexes
            fingers = detector.fingersUp(
                img=img, draw=False, circleRadius=10, circleColor=(0, 0, 0)
            )
            if fingers[1]:
                # Adjusting pointer cam size to full screen size
                # Setting middle as origin
                move(
                    (currLocationx - (CAM_WIDTH - (CAM_WIDTH * 0.03)) / 2)
                    * WIDTH_RATIO,
                    (currLocationy - (CAM_HEIGHT - (CAM_HEIGHT * 0.3)) / 2)
                    * HEIGHT_RATIO,
                )
                prevLocationx, prevLocationy = currLocationx, currLocationy
                if fingers[0] and not fingers[2] and not fingers[3] and not fingers[4]:
                    if clicked:
                        release(currLocationx, currLocationy)
                        clicked = False

                elif (
                    not fingers[0]
                    and not fingers[2]
                    and not fingers[3]
                    and not fingers[4]
                ):
                    if not clicked:
                        click(currLocationx, currLocationy)
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
