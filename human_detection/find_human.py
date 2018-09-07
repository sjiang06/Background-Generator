import cv2
import glob
import math
import numpy as np
import dlib
import argparse
from imutils import face_utils
import imutils
from sklearn.externals import joblib

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

faceDet_1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faceDet_2 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
faceDet_3 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
faceDet_4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

def draw_rect(image) :
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Convert image to grayscale
	#Detect face using 4 different classifiers
	face = faceDet_1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	if len(face) < 1 :
		return None;
	#Cut and save face
	for (x, y, w, h) in face: #get coordinates and size of rectangle containing face
		gray = gray[y:y+h, x:x+w] #Cut the frame to size
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		cv2.circle(image, (int(x + w/2), int(y + h/2)), 5, (0, 255, 0), -1)
		return image
		   

image = cv2.imread(args["image"])
output = draw_rect(image)
if(output.any() == None) :
	print("No face detected")
else :
	cv2.imshow("output", image)
	cv2.waitKey(0)
