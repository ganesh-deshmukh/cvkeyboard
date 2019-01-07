import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # lower_blue = np.array([30, 150, 50])      # red color- but not accurate
    # upper_blue = np.array([255, 255, 180])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # arguments for writting on video-frame
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,50)
    fontScale              = 1
    fontColor              = (255,0,255)
    lineType               = 2
    text = "CV-KeyBoard"

    cv2.putText(frame,text, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)

    x, y, w, h = cv2.getWindowImageRect("Frame") 
    # cv2.putText(frame,("width =" + str(x) + "height =" + str(y)), (200, 300), font, fontScale,(255,0,255),lineType)

    cv2.imshow('Frame',frame)

    x, y, w, h = cv2.getWindowImageRect("Frame") 
    
    cv2.imshow('mask',mask)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()