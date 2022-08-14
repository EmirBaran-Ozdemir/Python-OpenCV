import cv2
import handTrackingModule as htm
import numpy as np
import time

######################
wCam, hCam = 1280, 720
xr, yr = 0, 0
textCounter = 0
text = "Game Starting"
whiteColor = (255, 255, 255)
blackColor = (0, 0, 0)
difficultyDefinition = True
######################


def createMovingBox(img, xr, yr, xSpeed, ySpeed, color, wCam, hCam):
    cv2.rectangle(img, (xr, yr), (xr + xSize, yr + ySize), color, cv2.FILLED)
    xr = xr + xSpeed
    yr = yr + ySpeed
    if xr >= wCam - xSize or xr == 0:
        xSpeed = xSpeed * -1
    if yr >= hCam - ySize or yr == 0:
        ySpeed = ySpeed * -1

    return xr, yr, xSpeed, ySpeed


# Video Capture
camera = cv2.VideoCapture(0)
camera.set(3, wCam)
camera.set(4, hCam)
pTime = 0
detector = htm.handDetector(modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9)
# imgCanvas = np.zeros((720, 1280, 3), np.uint8)
print("Choose difficulty\n Difficulty should be between 1 and 3")
difficulty = int(input())
# Check if difficulty is valid
while difficultyDefinition:
    if difficulty < 1 and difficulty > 3:
        print("Difficulty should be between 1 and 3")
        difficulty = int(input())
    else:
        difficultyDefinition = False
# Set difficulty and variables
if difficulty == 1:
    xSize, ySize = 40, 40
    xSpeed, ySpeed = 20, 20
elif difficulty == 2:
    xSize, ySize = 60, 60
    xSpeed, ySpeed = 30, 30
else:
    xSize, ySize = 80, 80
    xSpeed, ySpeed = 50, 50

while True:
    success, img = camera.read()
    img = detector.findHands(img, draw=True)
    lmList, bbox = detector.findPosition(img, draw=False)
    start = False

    # FLIP
    img = cv2.flip(img, 1)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        fingers = detector.fingersUp(img=img, draw=False)
        # Game start if index finger up and all other down
        if (
            fingers[0]
            and fingers[1]
            and not fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):
            start = True
        # Block moves you should try to escape from block
        if start == True:
            xr, yr, xSpeed, ySpeed = createMovingBox(
                img, xr, yr, xSpeed, ySpeed, whiteColor, wCam, hCam
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
    # cv2.imshow("canvas", imgCanvas)
    if cv2.waitKey(1) == ord("q"):
        break
