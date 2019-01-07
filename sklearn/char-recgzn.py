import requests
import cv2
import numpy as np
import urllib.request  # for reading image from URL
import imutils
# from sklearn.externals import joblib
# from skimage.feature import hog
# import argparse as ap

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

        # im is croppedImage passing for character recognition
        im = frame[int(y - radius -40):int(y - radius -00)  ,int(x - 25):int(x + 25)]
        cv2.imshow("Cropped-image", im)
        
        # print("x =" +str(x))
        # print("y =" +str(y))
        # print("radius =" +str(radius))

    else:
        print("No any Contour Detected.")
        # else print blank image
        im = np.zeros([100,100,3],dtype=np.uint8)
        im.fill(255) # or img[:] = 255

# **********************    HCR-Part     **********************************************

        # Read the input image 
        # im = cv2.imread()

        # Convert to grayscale and apply Gaussian filtering
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

        # Threshold the image
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the image
        ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get rectangles contains each contour
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]

        # For each rectangular region, calculate HOG features and predict
        # the digit using Linear SVM.
        for rect in rects:
            # Draw the rectangles
            cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
            # Make the rectangular region around the digit
            leng = int(rect[3] * 1.6)
            pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
            # Resize the image
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            roi_hog_fd = pp.transform(np.array([roi_hog_fd], 'float64'))
            nbr = clf.predict(roi_hog_fd)
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)


#*****************************   printing and writing on image ************************#

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
