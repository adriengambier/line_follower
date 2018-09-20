import RPi.GPIO as GPIO
import time

class Initio():
    def init(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        
        self.R1 = 11
        self.R2 = 12
        self.L1 = 13
        self.L2 = 15
        
        GPIO.setup(self.L1, GPIO.OUT)
        self.RF = GPIO.PWM(self.L1, 50)
        self.RF.start(0)

        GPIO.setup(self.L2, GPIO.OUT)
        self.RB = GPIO.PWM(self.L2, 50)
        self.RB.start(0)

        GPIO.setup(self.R1, GPIO.OUT)
        self.LF = GPIO.PWM(self.R1, 50)
        self.LF.start(0)

        GPIO.setup(self.R2, GPIO.OUT)
        self.LB = GPIO.PWM(self.R2, 50)
        self.LB.start(0)

    def cleanup(self):
        self.stop()
        GPIO.cleanup()

    def version(self):
        return 1

    def forward(self, speedL, speedR):
        self.LB.ChangeDutyCycle(0)
        self.RB.ChangeDutyCycle(0)
        self.LF.ChangeDutyCycle(speedL)
        self.RF.ChangeDutyCycle(speedR)
        
    def stop(self):
        self.LF.ChangeDutyCycle(0)
        self.RF.ChangeDutyCycle(0)
        self.LB.ChangeDutyCycle(0)
        self.RB.ChangeDutyCycle(0)

if __name__ == '__main__':
    initio = Initio()
    initio.init()
    initio.forward(80,80)
    time.sleep(2)
    initio.stop()
    
    
