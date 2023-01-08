import io
import picamera
import cv2
import numpy
import time
from trilobot import *

# create the robot object
tbot = Trilobot()

def green_light():
    # Make the lights green
    tbot.fill_underlighting(0,0,0)
    tbot.set_underlight(LIGHT_FRONT_LEFT, 0,255,0, show=False)
    tbot.set_underlight(LIGHT_MIDDLE_LEFT, 0,255,0, show=False)
    tbot.set_underlight(LIGHT_REAR_LEFT, 0,255,0, show=False)
    tbot.set_underlight(LIGHT_FRONT_RIGHT, 0,255,0, show=False)
    tbot.set_underlight(LIGHT_MIDDLE_RIGHT, 0,255,0, show=False)
    tbot.set_underlight(LIGHT_REAR_RIGHT, 0,255,0, show=False)
    tbot.show_underlighting()

def blue_light():
    # Make the lights blue
    tbot.fill_underlighting(0,0,0)
    tbot.set_underlight(LIGHT_FRONT_LEFT, 0,0,255, show=False)
    tbot.set_underlight(LIGHT_MIDDLE_LEFT, 0,0,255, show=False)
    tbot.set_underlight(LIGHT_REAR_LEFT, 0,0,255, show=False)
    tbot.set_underlight(LIGHT_FRONT_RIGHT, 0,0,255, show=False)
    tbot.set_underlight(LIGHT_MIDDLE_RIGHT, 0,0,255, show=False)
    tbot.set_underlight(LIGHT_REAR_RIGHT, 0,0,255, show=False)
    tbot.show_underlighting()
    
def line_following():
    # capture an image
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    # create an image buffer
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)

    # assign the image from the cv2 buffer
    image = cv2.imdecode(buff, 1)
    
    #image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    #hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) 
    # change below lines to map the color you wanted robot to follow
    lower_yellow = numpy.array([ 0,  150,  0]) #40,0,0  50,0,0
    upper_yellow = numpy.array([255, 200, 250]) #255,255,100   100,100,100
    mask = cv2.inRange(image, lower_yellow, upper_yellow)
    mask_image=mask
    vel=[0,0,0]
    #cv2.imshow("mask",mask)
    #cv2.waitKey(1)

    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = 3*h/4 + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask[0:h, 0:50] = 0
    mask[0:h, w-50:w] = 0
    M = cv2.moments(mask)
    #print(M)
    if M['m00'] > 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        result=cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
        #cv2.imshow("result",result)
        #cv2.waitKey(1)
        # CONTROL starts
        err = cx - w/2
        vel[0] = 0.1
        vel[2] = 0.15*(-float(err) / 100)
        print("ERROR",err)
        if err > 0:
            green_light()
        else:
            blue_light()
        
while True or KeyboardInterrupt:
    faces, image = line_following()
