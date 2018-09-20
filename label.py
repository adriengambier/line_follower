import cv2
import numpy as np
import json
import argparse
import glob

#Define action when mouse button pressed
def drawback(event, x, y, flags, param):
    global mouse_x, mouse_y
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),3,(255,0,0), -1)
        mouse_x = np.append(mouse_x, x)
        mouse_y = np.append(mouse_y, y)
        print(x, y)
        if mouse_x.size == NUM_POINTS:
            next_image()
            
#Save points and reset coordinates
def next_image(save = True):
    global index, mouse_x, mouse_y, new_img
    if save:
        data[str(index)+ '.jpg'] = []
	for i in range(NUM_POINTS):
            data[str(index)+ '.jpg'].append([int(mouse_x[i]), int(mouse_y[i])])
    mouse_x = np.empty((0))
    mouse_y = np.empty((0))
    new_img = True

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Label Images')
    parser.add_argument('-f', '--folder', help='folder', type=str, required = True)
    parser.add_argument('-i', '--index', help='start index', type=int, default = 1)
    parser.add_argument('-p', '--points', help='number of points', type=int, default = 3)
    args = parser.parse_args()

    FOLDER = args.folder
    START_INDEX = args.index
    NUM_POINTS = args.points

    cv2.namedWindow('image')

    #Init mouse callback
    cv2.setMouseCallback('image', drawback)

    #Load size of the directory
    SIZE_FOLDER = len(glob.glob1(FOLDER, '*.jpg'))
    print('Images in the directory : ' + str(SIZE_FOLDER))

    #Init variables
    index = START_INDEX
    img = cv2.imread(FOLDER + str(index) + '.jpg')
    data = {}
    mouse_x = np.empty((0))
    mouse_y = np.empty((0))
    new_img = False

    print('Image ' + str(index))
    #main loop
    try :
        while(index < SIZE_FOLDER+START_INDEX):
	    #Update image
	    if new_img:
		index += 1
    		print('Image ' + str(index))
    		img = cv2.imread(FOLDER + str(index)+ '.jpg')
		new_img = False

	    #Show picture
	    cv2.imshow('image', img)
	    k = cv2.waitKey(20) & 0xFF
		
	    #Skip image
	    if k == ord('s'):
	        next_image(False)
	    #Quit
	    elif k == ord('q'):
	        break
    except KeyboardInterrupt:
	print("User cancelled")

    finally:
	print('Saving data in labels.json')
	with open(FOLDER + 'labels.json', 'w') as outfile:
	    json.dump(data, outfile)
	    cv2.destroyAllWindows()




