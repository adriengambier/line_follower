from keras.models import load_model
import cv2
import numpy as np
import util
import argparse
import glob

MAX_ANGLE = 90
MAX_SHIFT = 160

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Label Images')
    parser.add_argument('-f', '--folder', help='dataset folder', type=str, required = True)
    parser.add_argument('-i', '--index', help='starting index', type=int, default = 1)
    parser.add_argument('-m', '--model', help='model to use', type=str, default = '4out.h5')
    parser.add_argument('-w', '--width', help='width of images', type=int, default = 320)
    parser.add_argument('-e', '--height', help='height of images', type=int, default = 240)
    args = parser.parse_args()

    FOLDER = args.folder
    NETWORK = args.model
    START_INDEX = args.index
    WIDTH = args.width
    HEIGHT = args.height
        
    #Load model
    model = load_model(NETWORK)
    
    
    SIZE_FOLDER = len(glob.glob1(FOLDER, '*.jpg'))
    print('Images in the directory : ' + str(SIZE_FOLDER))

    index = START_INDEX
    step = 1

    #Loop through the folder
    while(index < START_INDEX+SIZE_FOLDER):
	#Load and resize image
        img = util.loadImg(index, FOLDER)
        if img is None:
            index+=1
            continue

        imgOrig = cv2.resize(img,(WIDTH,HEIGHT), interpolation = cv2.INTER_LINEAR)
        img = util.image_to_feature_vector(imgOrig)

	#NN Prediction
        x0, y0, x1, y1 = util.predict(img, model)

	#Increase size of image
        imgOrig = cv2.resize(imgOrig,(640,480), interpolation = cv2.INTER_LINEAR)
        util.drawLines(imgOrig, (int(x0*2),int(x1*2)), (int(y0*2), int(y1*2)))

	#Compute parameters
        theta = util.computeAngle(x0, y0, x1, y1) / MAX_ANGLE
        delta_x = (x0 - MAX_SHIFT) / MAX_SHIFT
        K = (theta + delta_x) / 2

        print('T :' + str(np.round(theta,2)) + ' X :' + str(np.round(delta_x, 2)) + ' K :' + str(np.round(K,2)))
	
	#Show image
        cv2.imshow('Image', imgOrig)
        k = cv2.waitKey(0) & 0xFF

        if k == ord('d'):
            break
        elif k == ord('n'):
            index += step
        elif k == ord('b'):
            index = max(1, index - step)
        elif k == ord('>'):
            step = step + 1
            print('Increase step : ' + str(step))
        elif k == ord('<'):
            if step > 1:
                step = step - 1
                print('Decrease step : ' + str(step))
