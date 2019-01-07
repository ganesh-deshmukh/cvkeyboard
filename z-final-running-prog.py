import requests
import cv2
import numpy as np
import urllib.request  # for reading image from URL
import imutils

while True:
    # *************************IP webcam image stream ************************************
    URL = "http://192.168.43.1:8080/shot.jpg"
    urllib.request.urlretrieve(URL, "shot1.jpg")
    frame = cv2.imread("shot1.jpg")

    # resize the frame, blur it, and convert it to the HSV
    frame = imutils.resize(frame, width=640, height=480)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower = np.array([110, 50, 50])
    upper = np.array([130, 255, 255])

    # lower = np.array([30, 150, 50])      # red color- but not accurate
    # upper = np.array([255, 255, 180])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # arguments for writting on video-frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 50)
    fontScale = 1
    fontColor = (255, 0, 255)
    lineType = 2
    text = "CV-KeyBoard"

    cv2.putText(
        frame, text, bottomLeftCornerOfText, font, fontScale, fontColor, lineType
    )

    # x, y, w, h = cv2.getWindowImageRect("Frame")

    cv2.imshow("Frame", frame)

    cv2.imshow("mask", mask)

    # cv2.imshow('Window-name',frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()
