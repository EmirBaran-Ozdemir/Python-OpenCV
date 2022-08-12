import numpy as np 
import cv2

cap = cv2.VideoCapture(0)
while True:
     ret, frame = cap.read()
     width = int(cap.get(3))
     height = int(cap.get(4))
     
     image = np.zeros(frame.shape, np.uint8)
     image = cv2.resize(image, (1280,960))
     smallerFrame = cv2.resize(frame, (0,0), fx=0.2,fy=0.2)

     imageConc = np.concatenate((smallerFrame,smallerFrame),axis=1)
     for i in range(3):
          imageConc = np.concatenate((imageConc,imageConc),axis=1)
          imageConc = np.concatenate((imageConc,imageConc,imageConc),axis=0)
     imageConc = cv2.flip(imageConc, 1)
     cv2.imshow("frame", imageConc)

     if cv2.waitKey(1) == ord("q"):
          break

cap.release()
cv2.destroyAllWindows()