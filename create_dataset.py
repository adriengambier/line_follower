import argparse
import cv2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dataset')
    parser.add_argument('-v', '--video', help='mp4 video', type=str, required = True)
    parser.add_argument('-o', '--output', help='output folder', type=str, required = True)
    args = parser.parse_args()

    vidcap = cv2.VideoCapture(args.video)
    success, image = vidcap.read()
    out_dir = args.output
    count = 1
    while success:
        cv2.imwrite(out_dir + str(count)+'.jpg', image)
        success, image = vidcap.read()
        print('reading frame :', str(count))
        count += 1
 
