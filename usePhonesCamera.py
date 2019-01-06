import requests
import cv2
import numpy as np 

url = "http://192.168.43.1:8080/shot.jpg"

while True:
	img_resp = requests.get(url)
	img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
	img = cv2.imdecode(img_arr, -1)

	cv2.namedWindow('Window-name',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Window-name', 600,600)
	cv2.imshow('Window-name',img)


	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()