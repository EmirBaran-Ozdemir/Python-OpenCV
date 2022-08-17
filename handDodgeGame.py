import cv2
import handTrackingModule as htm
import numpy as np
import time

######################
wCam, hCam = 1280, 720
xr, yr = 0, 0
textCounter = 0
text = "Game Starting"
whiteColor, blackColor, redColor, greenColor, blueColor = (
    (255, 255, 255),
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
)

chooseDifficulty = False
playerLose = False
score = 0
difficulty = 0
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


def checkCircleBoxOverlap():
    xN = max(xr, min(x1, xr + xSize))
    yN = max(yr, min(y1, yr + ySize))
    dx = xN - x1
    dy = yN - y1
    return (dx**2 + dy**2) <= playerSize**2


def difficultySettings(difficulty):
    if difficulty == 1:
        scoreAddition = 10
        playerSize = 30
        xSize, ySize = 70, 70
        xSpeed, ySpeed = 10, 10
    elif difficulty == 2:
        scoreAddition = 20
        playerSize = 40
        xSize, ySize = 60, 60
        xSpeed, ySpeed = 30, 30
    else:
        scoreAddition = 30
        playerSize = 50
        xSize, ySize = 80, 80
        xSpeed, ySpeed = 50, 50
    return xSpeed, ySpeed, xSize, ySize, scoreAddition, playerSize


# Video Capture
camera = cv2.VideoCapture(0)
camera.set(3, wCam)
camera.set(4, hCam)
pTime = 0
detector = htm.handDetector(modelComplex=0, maxHands=1, detectionCon=0.9, trackCon=0.9)

# Set difficulty variables


while True:
    success, img = camera.read()
    img = detector.findHands(img, draw=False)
    lmList, bbox = detector.findPosition(img, draw=False)
    start = False

    # FLIP
    img = cv2.flip(img, 1)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        x1 = wCam - x1
        fingers = detector.fingersUp(img=img, draw=False)
        # Difficulty choose
        if chooseDifficulty == False:
            # Little finger up == easy mode
            if (
                fingers[0]
                and not fingers[1]
                and not fingers[2]
                and not fingers[3]
                and fingers[4]
            ):
                difficulty = 1
                (
                    xSpeed,
                    ySpeed,
                    xSize,
                    ySize,
                    scoreAddition,
                    playerSize,
                ) = difficultySettings(difficulty)
                chooseDifficulty = True

            # Little and index finger up = medium mode
            elif (
                fingers[0]
                and fingers[1]
                and not fingers[2]
                and not fingers[3]
                and fingers[4]
            ):
                difficulty = 2
                (
                    xSpeed,
                    ySpeed,
                    xSize,
                    ySize,
                    scoreAddition,
                    playerSize,
                ) = difficultySettings(difficulty)
                chooseDifficulty = True
            # Little, ring and middle finger up = hard mode
            elif (
                fingers[0]
                and not fingers[1]
                and fingers[2]
                and fingers[3]
                and fingers[4]
            ):
                difficulty = 3
                (
                    xSpeed,
                    ySpeed,
                    xSize,
                    ySize,
                    scoreAddition,
                    playerSize,
                ) = difficultySettings(difficulty)
                chooseDifficulty = True

        # Game start if index finger up and all others down
        if (
            fingers[0]
            and fingers[1]
            and not fingers[2]
            and not fingers[3]
            and not fingers[4]
            and chooseDifficulty == True
        ):
            start = True
        elif (
            fingers[0]
            and fingers[1]
            and not fingers[2]
            and not fingers[3]
            and not fingers[4]
            and chooseDifficulty == False
        ):
            cv2.putText(
                img,
                "You should choose difficulty first",
                (100, 360),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                greenColor,
                4,
            )
        # Game restart if index and middle finger up and all others down
        if (
            fingers[0]
            and fingers[1]
            and fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):

            playerLose = False
            start = False
            score = 0
            xr, yr = 0, 0
            (
                xSpeed,
                ySpeed,
                xSize,
                ySize,
                scoreAddition,
                playerSize,
            ) = difficultySettings(difficulty)
        # Difficulty reset if thumb and little finger up
        if (
            not fingers[0]
            and not fingers[1]
            and not fingers[2]
            and not fingers[3]
            and fingers[4]
        ):

            difficulty = 0
            chooseDifficulty = False
        # GAME TIME
        # Box moves and player should try to escape
        if start == True and playerLose == False:
            cv2.circle(img, (x1, y1), playerSize, redColor, cv2.FILLED)
            xr, yr, xSpeed, ySpeed = createMovingBox(
                img, xr, yr, xSpeed, ySpeed, whiteColor, wCam, hCam
            )
            score += scoreAddition
            if checkCircleBoxOverlap():
                playerLose = True
        # Game over screen and player score
        elif playerLose == True:
            cv2.putText(
                img,
                "GAME OVER",
                (400, 360),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                greenColor,
                4,
            )
            cv2.putText(
                img,
                f"YOUR SCORE IS {score}",
                (250, 420),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                redColor,
                4,
            )

    # FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # DISPLAY FPS
    cv2.putText(
        img, f"FPS:{int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )
    # DISPLAY difficulty
    cv2.putText(
        img,
        f"difficulty = {difficulty}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.imshow("Hand Dodge Game", img)
    # EXIT
    if cv2.waitKey(1) == ord("q"):
        break
