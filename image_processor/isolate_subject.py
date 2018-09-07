from PIL import Image
from numpy import *
import numpy as np 
import cv2
from imutils.video import VideoStream

fgbg = cv2.createBackgroundSubtractorMOG2()

#image = asarray(Image.open('images/004.jpg'))
vs = VideoStream().start()

#fgmask = fgbg.apply(image)
while(True) :
	image = vs.read()
	fgmask = fgbg.apply(image)
	cv2.imshow('image', fgmask)
	key = cv2.waitKey(1) & 0xFF
	if(key == ord("q")) : break

print("hello")
cv2.destroyAllWindows()
vs.stop()