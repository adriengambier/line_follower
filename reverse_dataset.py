import cv2
import json
import argparse

def flip_x(x, width): #For a (320,240) picture
    if x >= (width/2):
        x = x - (x % (width/2))*2 + 1
    else:
        x = x + width - 1 - (x%((width/2)-1))*2
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reverse dataset')
    parser.add_argument('-i', '--input', help='input folder', type=str, required = True)
    parser.add_argument('-o', '--output', help='output folder', type=str, required = True)
    args = parser.parse_args()

    in_dir = args.input
    out_dir = args.output
    data = {}
    #Load json file
    samples = json.load(open(in_dir+'labels.json'))
    labels = list(samples.keys())
    #Copy json file to data
    for label in labels:
	new_label = str(int(label.split('.')[0]) + len(samples)) + '.jpg'

	#Copy image
	img = cv2.imread(in_dir+label)
	cv2.imwrite(out_dir+label, img)
        cv2.imwrite(out_dir+new_label, cv2.flip(img,1))

	#Copy data
	data[label] = []
	data[new_label] = []
	for i in range(len(samples[label])):
	    x = samples[label][i][0]
	    y = samples[label][i][1]
	    data[label].append([x, y])
	    data[new_label].append([flip_x(x, img.shape[1]), y])

    with open(out_dir + 'labels.json', 'w') as outfile:
        json.dump(data, outfile)
