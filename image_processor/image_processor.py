from PIL import Image, ImageOps
from PIL import ImageFilter
import numpy as np
import cv2
import os.path
import os
import cmd

# Image processing demo for background generating project


# Prints the number of pixels in the image, not
# including transparent pixels
def getNumPixels(image) :
	#im = Image.open(imageName)
	image = image.convert("RGBA")
	datas = image.getdata()

	solidPixels = 0
	for item in datas:
		if(item[3]!= 0) :
			solidPixels+=1
	# image = cv2.imread(imageName)
	print('This image has ' + str(solidPixels) + ' pixels.')
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)
	# image.show()

def rotateImage(image, degrees) :
	#im = Image.open(imageName)
	image = image.rotate(degrees)
	return image

def resizeImage(im, width, height) :
	#im = Image.open(imageName)
	ims = im.resize((width, height))
	# ims.show()
	return ims

# Blends the array of given images 
def overlayImages(images, width, height) :
	result = Image.new("RGB", (width, height))
	alphaIndex = 1
	for i in range(len(images)) :
		image = resizeImage(images[i], width, height)
		result = Image.blend(image, result, 1 - 1/alphaIndex)
		alphaIndex+=1
	return result

# Applies the given filter on the image
def filterImage(im, filter) :
	#im = Image.open(image)
	imb = im.filter(filter)
	#imb.show()
	# #save the image to filtered_images folder
	# head, tail = os.path.split(image)
	# file, ext = os.path.splitext(tail)
	# imb.save("filtered_images/" + file + "_filtered.jpg", 'JPEG')
	return imb

def makeLinearRamp(white) :
	ramp = []
	r, g, b = white
	for i in range(255) :
		ramp.extend((r*i//255, g*i//255, b*i//255))
	return ramp

def makeSepia(im) :
	sepia = makeLinearRamp((255, 240, 192))
	#im = Image.open(imageName)
	im = im.convert("L")
	im.putpalette(sepia)
	im.convert("RGB")
	#im.show()
	return im

def applyPalette(im, ramp) :
    ramp = makeLinearRamp(ramp)
    #im = Image.open(imageName)
    im = im.convert("L")
    im.putpalette(ramp)
    im.convert("RGB")
    #im.show()
    return im

def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def shiftHue(img, hue):
    arr = np.array(img)
    hsv = rgb_to_hsv(arr)
    hsv[..., 0] = (hsv[..., 0] + hue) % 1
    rgb = hsv_to_rgb(hsv)
    imgh = Image.fromarray(rgb, 'RGB')
    return imgh

def getImage() : 
    imageName = input("Enter a filename: ")
    im = Image.new("RGB", (0, 0))
    while(True) :
        try: 
            im = Image.open(imageName)
            break
        except:
            print("Invalid file name")
        imageName = input("Enter a filename: ")
    return im

sharpenFilter = ImageFilter.Kernel((3,3), [0, -1, 0, -1, 5, -1, 0, -1, 0])
blurFilter = ImageFilter.Kernel((3, 3), [1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9])
laplaceFilter = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0])
edgeFilter = ImageFilter.Kernel((3,3), [-1, -1, -1, -1, 8, -1, -1, -1, -1])
randomFilter = ImageFilter.Kernel((3, 3), [1, 1, 1, 1, 0.7, -1, -1, -1, -1])
filters = [ImageFilter.BLUR, sharpenFilter, blurFilter, ImageFilter.FIND_EDGES, randomFilter]

# getNumPixels("images/001.jpeg")
# rotateImage("images/001.jpeg", 45)
# getNumPixels("images/002.png")
# rotateImage("images/002.png", 90)
# resizeImage("images/001.jpeg", 200, 200)
# overlayImages("images/001.jpeg", "images/006.jpg", 200, 200, 0.5)
# filterImage("images/006.jpg", filters[0])
# filterImage("images/006.jpg", filters[2])
# filterImage("images/006.jpg", filters[3])
# filterImage("images/025.jpg", filters[3])
# filterImage("images/021.jpg", ImageFilter.FIND_EDGES)
# im = makeSepia(Image.open("images/006.jpg"))
# im.convert("RGBA")
# im1 = Image.open("images/006.jpg")
# im2 = Image.open("images/001.jpeg")
# im3 = Image.open("images/021.jpg")
# overlayImages([im1, im2, im3], im1.width, im1.height).show()
# shiftHue(im3, 0.75)
print("Welcome to Python image processor!")
print("n - get number of pixels in image")
print("r - rotate image")
print("re - resize image")
print("o - overlay images")
print("f - apply image filter")
print("s - make image sepia")
print("h - adjust hue")
print('c - change photo')
print('sh - show photo')
print("q - quit")

im = getImage()

while(True) :
    command = input("Enter a command: ")
    if(command.lower() == 'n') :
        getNumPixels(im)
    elif(command.lower() == 'r') :
        degrees = input("Enter number of degrees to rotate: ")
        imr = rotateImage(im, float(degrees))
        imr.show()
    elif(command.lower() == 're') :
        width = input("Enter width: ")
        height  = input("Enter height: ")
        imre = resizeImage(im, int(width), int(height))
        imre.show()
    elif(command.lower() == 'o') :
        images = [im]
        while(True) :
            c = input("Press 'q' if done entering photos, or press any key to continue: ")
            if(c.lower() == 'q') :
                break
            imc = getImage()
            images.append(imc)
        imo = overlayImages(images, im.width, im.height)
        imo.show()
    elif(command.lower() == 'f') :
        i = input("Enter a number between 1-5, inclusive: ")
        while(True) :
            if(int(i) > 5 or int(i) < 1) :
                i = input("Enter a number between 1-5, inclusive: ")
            else :
                break
        imf = filterImage(im, filters[int(i) - 1])
        imf.show()
    elif(command.lower() == 's') :
        ims = makeSepia(im) 
        ims. show()
    elif(command.lower() == 'p') :
        r = input("red: ")
        g = input("green: ")
        b = input("blue: ")
        imp = applyPalette(im, (int(r), int(g), int(b)))
        imp.show()
    elif(command.lower() == 'h') :
        c = input("Enter a value between 0-1, or 'q' to quit: ")
        while(True) :
            if(c.lower() == 'q') :
                break
            imh = shiftHue(im, float(c))
            imh.show()
            c = input("Enter a value between 0-1, or 'q' to quit: ")
    elif(command.lower() == 'c') :
        im = getImage()
    elif(command.lower() == 'sh') :
        im.show()
    elif(command.lower() == 'q') :
        break
print("Have a nice day!")