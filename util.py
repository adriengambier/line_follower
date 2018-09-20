import sys
import termios
import tty
import numpy as np
import math
import cv2
import glob
import json

#Used by readkey()
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

#Read input from console
def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

#Compute the angle between 2 vectors
def computeAngle(x1, y1, x2, y2):
    v1 = (x2 - x1, y2 - y1)
    v2 = (0, 1 - y1)	
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    deg = math.degrees(math.acos(sum([x * y for x, y in zip(v1, v2)]) / (norm1*norm2)))
    sign = np.sign(x2-x1)
    theta =  sign * deg
    return theta

#Compute the curvature of 3 points
def computeCurvature(x0,y0,x1,y1,x2,y2):
    m1 = (y1-y0)/(x1-x0)
    m2 = (y2-y1)/(x2-x1)
    slp = (m1+m2)/2
    x01 = (x0+x1)/2
    x12 = (x1+x2)/2
    derSlp = (m2-m1)/(x12-x01)
    r = (1+slp**2)**1.5/np.abs(derSlp)
    return r

#Load the image num_picture.jpg in folder
def loadImg(num_picture, folder):
    path = folder + str(num_picture) + '.jpg'
    img = cv2.imread(path)
    
    return img

#Take picture from vs(videostream) and return the opencv array of the image
def takePicture(vs, folder = None):
    num_picture = len(glob.glob1(FOLDER, '*.jpg')) + 1
    img = vs.read()
    if folder != None:
        cv2.imwrite(folder+str(num_picture)+'.jpg', img)
        return loadImg(num_picture, folder)
    else:
        return img

#Draw lines for the specified points 
def drawLines(img, x, y):
    cv2.circle(img,(x[0],y[0]),3,(0,255,0), -1)
    for i in range(len(x) - 1):
        cv2.line(img,(x[i], y[i]),(x[i+1],y[i+1]),(255,0,0),2)
        cv2.circle(img,(x[i+1],y[i+1]),3,(0,255,0), -1)

#Convert image to size (32,32) and normalize
def image_to_feature_vector(image, size=(32, 32)):
	image = image[95:240, 0:320]
	x = cv2.resize(image, size, interpolation = cv2.INTER_LINEAR)
	x = x / 255.
	x -= 0.5
	x *= 2
	return x

#Predict line from model and image
def predict(image, model):
        features = []
        features.append(image)
        return model.predict(np.array(features))[0]












