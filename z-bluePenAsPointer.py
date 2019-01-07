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
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # h, w, channels = np.shape(frame)
    # print image properties.
    # print("width: " + str(w))
    # print("height: " + str(h))
    # print("channels: " + str(channels))

    # define range of blue color in HSV
    lower = np.array([110, 50, 50])
    upper = np.array([130, 255, 255])

    # lower = np.array([30, 150, 50])      # red color- but not accurate
    # upper = np.array([255, 255, 180])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image  			# To show filtered images.
    # res = cv2.bitwise_and(frame, frame, mask=mask)

    # find contours and draw border and calculate points

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # cv2.drawContours(frame, c, -1, (255, 0, 0), 2)        
        # cv2.circle(frame, (int(x),int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame,(int(x),int(y)),3,(255,255,0),3)               # this is center
        
        #*************** crop that image **************

    # crop_img = img[y:y+h, x:x+w]
    # cv2.imshow("cropped", crop_img)
        pt1 = (int(x - 25),int(y - radius -40))
        pt2 = (int(x + 25),int(y - radius -00))
        cv2.rectangle(frame, pt1, pt2 , (255,255,0),3)
        print("x =" +str(x))
        print("y =" +str(y))
        print("radius =" +str(radius))

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

    cv2.imshow("Frame", frame)
    cv2.imshow("mask", mask)
    # cv2.imshow("res", res)

    # **************** boilerplate-code => same for all ************************#
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
