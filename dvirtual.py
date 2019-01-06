## @Author: Dishant Varshney
""" Finger Tracking: This pyhton program tracks the finger """

## Importing Libraries
import numpy as np 
import cv2 as cv 
import math

## Defining Constants
lwr = np.array([0,50,70], np.uint8)
upr = np.array([100,230,230], np.uint8)
kernel = np.ones((5,5), np.uint8)
fingerP = []
fingerT = []
st = False
p = False

## HSV function to separate hand(skin color) from background(color)
def hsvF(focusF):
    hsv = cv.cvtColor(focusF, cv.COLOR_BGR2HSV_FULL)
    mask = cv.inRange(hsv, lwr, upr)
    mask = cv.dilate(mask, kernel, iterations = 3)
    mask = cv.GaussianBlur(mask, (5,5), 100)
    return mask

## Function to mark the centroid of contour
def centroidF(cnt):
    M = cv.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx, cy
    else:
        pass

## Function to display the topmost point of the contour
def points(focusF, finger):
    for i in range(len(finger)):
        cv.circle(focusF, finger[i], 5, [182,31,102], -1)

## Function to pause/start the tracking of the finger
# Press 'p' to pause/start the tracking
# Press 'c' to clear the screen
def pauseT(focusF, fingerT, ftop):
    if len(fingerT) < 20:
        fingerT.append(ftop)
    else:
        fingerT.pop(0)
        fingerT.append(ftop)
    points(focusF, fingerT)

## Main function
cap = cv.VideoCapture(0)  # capture the frames from the web camera

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        frame = cv.flip(frame, 1)
        focusF = frame[55:445, 305:595]

        cv.putText(frame, 'DV', (10,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv.rectangle(frame, (300, 50), (600, 450), (0,0,255), 0)

        noise = hsvF(focusF)

        r,thresh = cv.threshold(noise, 100, 255, cv.THRESH_BINARY)
        img, cont, hie = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        try:
            cnt = max(cont, key = cv.contourArea)

            epsilon = 0.001*cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)

            hull = cv.convexHull(approx, returnPoints=False)
            area_cnt = cv.contourArea(approx)
            defects = cv.convexityDefects(approx, hull)

            centroid = centroidF(cnt)
            
            if defects is not None:
                if st == True:
                    if area_cnt > 6000:
                        for i in range(defects.shape[0]):
                            s,e,f,d = defects[i,0]
                            start = tuple(approx[s][0])
                            end = tuple(approx[e][0])
                            far = tuple(approx[f][0])
                            ftop = tuple(cnt[cnt[:,:,1].argmin()][0])

                            cv.circle(focusF, ftop, 5, (0,0,255), -1)
                            cv.line(focusF, start, end, (0,255,0), 2)
                            cv.circle(focusF, centroid, 3, (0,255,255), -1)

                            pauseT(focusF, fingerT, ftop)
                            if p == True:
                                fingerP.append(ftop)
                                cv.putText(frame, "Tracking ON", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5, (182,31,102), 2)
                            else:
                                cv.putText(frame, "Tracking OFF", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5, (182,31,102), 2)
                    else:
                       cv.putText(frame, "Can't detect anything", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,150), 2) 
                else:
                    cv.putText(frame, "Press 's' to start", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,150), 2)
        except:
            cv.putText(frame, "Put your hand in the frame", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        
        points(focusF, fingerP)
        cv.imshow('Finger Detection', frame)

        k = cv.waitKey(1) & 0xff
        if k  == ord('s'):
            st = not st
        elif k == ord('p'):
            p = not p
        elif k == ord('c'):
            fingerP.clear()
        elif k == ord('q'):
            break

cap.release()
cv.destroyAllWindows()