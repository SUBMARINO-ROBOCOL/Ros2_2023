import cv2
from PIL import Image
import numpy as np


#def get_limits(color):
#
#    c = np.uint8([[color]])
#    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
#
#    lowerLimit = hsvC[0][0][0] - 10, 100, 100
#    upperLimit = hsvC[0][0][0] + 10, 255, 255
#
#    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
#    upperLimit = np.array(upperLimit, dtype=np.uint8)
#
#    return lowerLimit, upperLimit


def red_box(img):
	bbox = (0,0,0,0)
	
	hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	lower1 = np.array([0, 100, 20])
	upper1 = np.array([10, 255, 255])
	lower2 = np.array([160,100,20])
	upper2 = np.array([179,255,255])

	lower_mask = cv2.inRange(hsvImage, lower1, upper1)
	upper_mask = cv2.inRange(hsvImage, lower2, upper2)

	mask = lower_mask + upper_mask

	mask_ = Image.fromarray(mask)
	bbox = mask_.getbbox()
	if bbox is not None:
		x1, y1, x2, y2 = bbox
		img = cv2.rectangle(img, (x1,y1), (x2,y2), (50,50,250), 5)
	
	while True:
		cv2.imshow ("frame", img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
