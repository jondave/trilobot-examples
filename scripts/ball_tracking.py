# This script uses the camera mounted on the trilobot to detect and locate balls of different colors in the image. 
# The location of the ball with a specific color (defined by the user) in the image is used to make 
# the robot rotate in a way that the ball stays detected in the center of the image.
# When the robot detects a ball with a specific color wanted, the LEDs are activated in that color, otherwise they are turned off.

import picamera
import cv2
import numpy
from trilobot import *

# create the robot object
tbot = Trilobot()

# RGB Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Color wanted to be tracked
color_wanted="RED" # it can be "RED", "YELLOW", "GREEN", "BLUE"

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        image = numpy.empty((240 * 320 * 3,), dtype=numpy.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((240, 320, 3))
    
    return image
  
def circle_detection(image):  
    # Convert to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 30,
                   param2 = 80, minRadius = 0, maxRadius = 0)
    # Count and locate the circles that are detected.
    x=[] # list with x component of the circles detected
    y=[] # list with y component of the circles detected
    r=[] # list with the radius of the circles detected
    if detected_circles is not None:
        num_circles=len(detected_circles[0,:,0])  
        # Convert the circle parameters x, y and r to integers.
        detected_circles = numpy.uint16(numpy.around(detected_circles))
        for pt in detected_circles[0,:]:
            x.append(pt[0])
            y.append(pt[1])
            r.append(pt[2])
    else:
        num_circles=0
    return num_circles,x,y,r

def check_color(mask,h,w,x,y,r):
    
    search_top = int(y - r)
    search_bot = int(y + r)
    search_left = int(x - r)
    search_right = int(x + r)
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask[0:h, 0:search_left] = 0
    mask[0:h, search_right:w] = 0
    
    M = cv2.moments(mask)
    if M['m00'] > 0:
        color_det=True
    else:
        color_det=False
    return color_det,[M['m00'],M['m10'],M['m01']]

def color_detection(image,color_wanted,x,y,r):
    ## convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    if color_wanted=="RED":
        ## mask of red 
        mask_r_lower = cv2.inRange(hsv, (0,0,0), (10, 255, 255))
        mask_r_upper = cv2.inRange(hsv, (170,0,0), (180, 255, 255))
        mask=cv2.bitwise_or(mask_r_lower, mask_r_upper)
    elif color_wanted=="YELLOW":
        ## mask of yellow 
        mask = cv2.inRange(hsv, (15,0,0), (36, 255, 255))
    elif color_wanted=="GREEN":
        ## mask of green 
        mask = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
    elif color_wanted=="BLUE":
        ## mask of blue 
        mask = cv2.inRange(hsv, (100,0,0), (135, 255, 255))
    
    ## Masking
    h, w, d = image.shape
    color_detected=False
    index=[]
    for i in range(len(x)):
        [color_detected,M]=check_color(mask,h,w,x[i],y[i],r[i])
        print(color_detected,i)
        if color_detected==True:
            index=i
            break
    return color_detected,index,w

def activate_leds(color_wanted):
    if color_wanted=="RED":
        tbot.fill_underlighting(RED)
    elif color_wanted=="YELLOW":
        tbot.fill_underlighting(YELLOW)
    elif color_wanted=="GREEN":
        tbot.fill_underlighting(GREEN)
    elif color_wanted=="BLUE":
        tbot.fill_underlighting(BLUE)   

def ball_tracking(x,w):
    err_x = x - w/2
    vel = 0.5*(-float(err_x) / 100)
    print("VELOCITY",vel)
    if vel<0.2:
        tbot.disable_motors()
    else:
        tbot.set_motor_speeds(-vel, vel)
              
while True or KeyboardInterrupt:
    image=capture_image()
    [num_balls,x,y,r]=circle_detection(image)
    if num_balls>0:
        [color_detected,ball_index,w]=color_detection(image,color_wanted,x,y,r)
        if color_detected==True:
            print("NUMBER OF BALLS:",num_balls,"TRACKING ",color_wanted)
            ball_tracking(x[ball_index],w) 
            activate_leds(color_wanted)            
        else:
            print("NUMBER OF BALLS:",num_balls)
            tbot.fill_underlighting(BLACK)  
            tbot.disable_motors()
    else:
        print("NUMBER OF BALLS:",num_balls)
        tbot.fill_underlighting(BLACK)  
        tbot.disable_motors()
