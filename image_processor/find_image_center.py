from PIL import Image
import sys
import cv2 as cv

def getWidth(image):
	rgb_im = image.convert('RGB')
	startW = -1
	endW = -1
	for w in range(image.width):
		colorPixelInCol = 0
		for h in range(image.height):
			r, g, b = rgb_im.getpixel((w, h))
			if r != 0 or g != 0 or b != 0:
				colorPixelInCol = 1
				if startW == -1:
					startW = w
				else:
					endW = w
		# if(colorPixelInCol == 0 and startW != -1):
		# 	endW = w - 1
		# 	return (startW, endW)
	return (startW, endW)

def getHeight(image):
	rgb_im = image.convert('RGB')
	startH = -1
	endH = -1
	for h in range(image.height):
		colorPixelInRow = 0
		for w in range(image.width):
			r, g, b = rgb_im.getpixel((w, h))
			if r != 0 or g != 0 or b != 0:
				colorPixelInRow = 1
				if startH == -1:
					startH = h
				else: 
					endH = h
		# if colorPixelInRow == 0 and startH != -1:
		# 	endH = h - 1
		# 	return (startH, endH)
	return (startH, endH)



# if len(sys.argv) == 2:
# 	filename = sys.argv[1]
# else :
# 	print("No filename given, so using default image")
# 	filename = "grabcut_results/ex_3.png"

# im = Image.open(filename)
# im_cv = cv.imread(filename)
# cv.imshow("image", im_cv)

# while(1):
# 	key = cv.waitKey(1)

# 	if key == 27:
# 		break
# 	elif key == ord('w'):
# 		startW, endW = getWidth(im)
# 		print("startW: " + str(startW))
# 		print("endW: " + str(endW))
# 		print(str(endW - startW + 1) + ' pixels wide')
# 	elif key == ord('h'):
# 		startH, endH = getHeight(im)
# 		print("startH: " + str(startH))
# 		print("endH: " + str(endH))
# 		print(str(endH - startH + 1) + ' pixels high')
# 	elif key == ord('b'):
# 		startW, endW = getWidth(im)
# 		startH, endH = getHeight(im)
# 		cv.rectangle(im_cv, (startW, startH), (endW, endH),
# 			(0, 255, 0), 2)
# 		cv.circle(im_cv, (startW + int((endW - startW)/2), startH + int((endH - startH)/2)), 5, (0, 255, 0), -1)
# 		cv.imshow("image_update", im_cv)

# cv.destroyAllWindows()