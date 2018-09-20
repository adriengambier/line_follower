import cv2
import json
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reverse dataset')
    parser.add_argument('-i', '--input', help='input folder', type=str, required = True)
    parser.add_argument('-a', '--add', help='additional folder', type=str, required = True)
    parser.add_argument('-o', '--output', help='output folder', type=str, required = True)
    args = parser.parse_args()

    in_dir = args.input
    add_dir = args.add
    out_dir = args.output
    data = {}

    samples1 = json.load(open(in_dir + 'labels.json')) 
    samples2 = json.load(open(add_dir + 'labels.json'))
    labels1 = list(samples1.keys())
    labels2 = list(samples2.keys())

    #Load first dataset
    for label in labels1:
	data[label] = []	
	
	#Copy image
	img = cv2.imread(in_dir+label)
	cv2.imwrite(out_dir+label, img)

	for i in range(len(samples1[label])):
	    x = samples1[label][i][0]
	    y = samples1[label][i][1]
	    data[label].append([x, y])

    #Load second dataset
    for label in labels2:
	data[label] = []

	#Copy image
	img = cv2.imread(add_dir+label)
	cv2.imwrite(out_dir+label, img)

	for i in range(len(samples2[label])):
	    x = samples2[label][i][0]
	    y = samples2[label][i][1]
	    data[label].append([x, y])

    #Save new dataset
    with open(out_dir + 'labels.json', 'w') as outfile:
        json.dump(data, outfile)
