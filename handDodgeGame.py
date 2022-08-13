import cv2
import handTrackingModule as htm
import numpy as np
import time

######################
wCam, hCam = 1500, 1200
xr, yr = 0, 0
textCounter = 0
text = "Game Starting"
blockSize = 100
######################

# Video Capture
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    start = False

    # FLIP
    img = cv2.flip(img, 1)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        fingers = detector.fingersUp(img=img, draw=False)
        # Game start
        if fingers[0] and fingers[1]:
            start = True
        # Block moves and game
        if start == True:
            if xr < 1000 and yr < 1000:
                xr += 10
                yr += 10
            elif xr < 1000 and yr < 1000:
                if textCounter < 30:
                    cv2.putText(
                        img,
                        text,
                        (470, 380),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )

            cv2.rectangle(
                img, (xr, yr), (xr + 20, yr - 20), (255, 255, 255), cv2.FILLED
            )

    # FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # DISPLAY
    cv2.putText(
        img, f"FPS:{int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )
    cv2.imshow("Test", img)
    if cv2.waitKey(1) == ord("q"):
        break
