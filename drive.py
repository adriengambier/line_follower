from time import sleep, time
import car
from imutils.video.pivideostream import PiVideoStream
import util
import numpy as np
from keras.models import load_model

MAX_R = 100 #[0,100] Max right speed when going straight
MAX_L = 100 #[0,100] Max left speed when going straight
MAX_R_TURN = 100 #[0,100] Max right speed when turning left
MAX_L_TURN = 100 #[0,100] Max left speed when turning right
MAX_ANGLE = 90 #Max threshold for the angle, reducing it will make the car more reactive to the angle
MAX_SHIFT = 160 #Max threshold for the shift, reducing it will make the car more reactive to the shift
THRESHOLD = 0.2 #Threshold at which the car turns
FREQ = 13 #Frequency at which we update the car 
RES = (320,240) #Resolution of the camera

update = True
img = None

print("Loading ...")

#Loading NN
network = '4out.h5'
model = load_model(NETWORK)

#Setting up car and video stream
initio = car.Initio()
initio.init()
vs = PiVideoStream(resolution=RES,framerate=5).start()

sleep(2.0)

print("Ready !")

t = time()
##Main loop
while True:
    if time() - t > 1/FREQ or img == None:
        #Take picture
        update = True
        img = util.takePicture(vs)
        t = time()
        
    #Prediction of the NN
    x0, y0, x1, y1 = util.predict(img, model)
    
    #Compute angle of the road lane
    theta = util.computeAngle(x0, y0, x1, y1) / MAX_ANGLE
    theta = max(min(1, theta), -1) # [-1; 1]
    
    #Compute the current shift with middle line
    delta_x = (x0 - RES[0]/2)/MAX_SHIFT 
    delta_x = max(min(1, delta_x), -1) # [-1; 1]
    
    #Averaging the 2 errors
    K = (theta + delta_x) / 2 #K=[-1,1] | K=0 : no changes
    
    if K < -THRESHOLD :
        power_l = 0
        power_r = MAX_R_TURN
    elif K > THRESHOLD :
        power_r = 0
        power_l = MAX_L_TURN
    else:
        power_r = MAX_R 
        power_l = MAX_L
        
    #If there is an update, update speed and print parameters
    if update:
        update = False
        print('L :' + str(power_l) + ' R :' + str(power_r), 'K :' + str(np.round(K, 2)) + ' T :' + str(np.round(theta, 2)) + ' X :' + str(np.round(delta_x,2)))
        initio.forward(power_l, power_r)

