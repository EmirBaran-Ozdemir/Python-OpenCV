import cv2
import time

######################
wCam, hCam = 1500, 1200
######################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    success, img = cap.read()
    # FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # DISPLAY
    img = cv2.flip(img, 1)
    cv2.putText(
        img, f"FPS:{int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )
    cv2.imshow("Test", img)
    if cv2.waitKey(1) == ord("q"):
        break
