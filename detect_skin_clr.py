import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while 1:
    # Take each frame
    # _, frame = cap.read()
    frame = cv2.imread("./palm.jpg")
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    # lower = np.array([110,50,50])     # doesn't work in day
    # upper = np.array([130,255,255])

    # lower = np.array([2, 50, 0])             # testing-color
    # upper = np.array([20, 255, 255])

    lower = np.array([0, 48, 80])  # this color range works at dark for gd
    upper = np.array([20, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    res = cv2.GaussianBlur(res, (5, 5), 0)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    # cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
