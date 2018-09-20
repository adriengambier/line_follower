from picamera import PiCamera
import cv2
import car
import util
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Label Images')
    parser.add_argument('-f', '--folder', help='folder', type=str, required = True)
    args = parser.parse_args()
    
    print('##Init##')
    FOLDER = args.folder
    record = False
    num_video=1
    
    #Setting up car
    initio = car.Initio()
    initio.init()
    
    #Setting up camera
    camera = PiCamera()
    camera.rotation = 180
    camera.framerate = 10
    camera.resolution = (320,240)
    
    print('##Ready##')
    
    while True:
        k = util.readkey()
        if k == 'z': #Go forward if manual mode
            print('[MANUAL] Forward')
            initio.forward(100,100)
        elif k == 'q': #Go left if manual mode
            print('[MANUAL] Left')
            initio.forward(0,100)
        elif k == 'd': #Go right if manual mode
            print('[MANUAL] Right')
            initio.forward(100,0)
        elif k == ' ': #Stop if manual mode
            print('[MANUAL] Stop')
            initio.stop()
        elif k == 'e': #Stop if manual mode
            print('[MANUAL] End')
            break
        elif k == 'r':
            if not record:
                print('##Start Record##')
                camera.start_recording(Folder + 'video' + str(num_video) + '.h264')
                record = True
                num_video+=1
            else:
                print('##Stop Record##')
                camera.stop_recording()
                record = False
        
        
        

        
        
        
        
        
