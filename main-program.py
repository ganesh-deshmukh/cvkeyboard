# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while(1):

#     _, frame = cap.read()

#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     lower_blue = np.array([110,50,50])
#     upper_blue = np.array([130,255,255])

#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     res = cv2.bitwise_and(frame,frame, mask= mask)

#     cv2.imshow('frame',frame)
#     cv2.imshow('mask',mask)
#     # cv2.imshow('res',res)
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break

# cv2.destroyAllWindows()

import requests
import cv2
import numpy as np 

url = "http://192.168.43.1:8080/shot.jpg"

while True:
    img_resp = requests.get(url)
    img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)

    cv2.namedWindow('window',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('window', 600,400)
    # cv2.imshow('Window-name',img)

    # img = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('window',frame)
    cv2.imshow('mash',mask)
    cv2.imshow('res',res)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()