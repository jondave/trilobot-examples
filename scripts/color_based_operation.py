# This script uses the camera mounted on the trilobot to detect and locate and determine the color of circles/balls in the image. 
# The color of the circle/ball defines what action the robot must do including 1) moving forwards for 3 seconds 2) moving while creating a 
# square shape path 3) moving while creating a circular shape path 4) adjusting the robot orientation to keep the circle/ball always detected 
# in the center of the image.
# When the robot detects a circle/ball with a specific color, the LEDs keep activated in that color while the robot performs the specific action
# otherwise they are turned off.

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

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        image = numpy.empty((240 * 320 * 3,), dtype=numpy.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((240, 320, 3))
        #image = cv2.imdecode(numpy.fromfile('/home/pi/trilobot-examples/images/red_circle.PNG', dtype=numpy.uint8), cv2.IMREAD_UNCHANGED)
        
        h, w, d = image.shape
        
    return image,w
  
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

def color_detection(image,x,y,r):
            
    ## convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ## mask of red 
    mask_r_lower = cv2.inRange(hsv, (0,0,0), (10, 255, 255))
    mask_r_upper = cv2.inRange(hsv, (170,0,0), (180, 255, 255))
    mask_r=cv2.bitwise_or(mask_r_lower, mask_r_upper)
    ## mask of yellow 
    mask_y = cv2.inRange(hsv, (15,0,0), (36, 255, 255))
    ## mask of green 
    mask_g = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
    ## mask of blue 
    mask_b = cv2.inRange(hsv, (100,0,0), (135, 255, 255))

    h, w, d = image.shape
    
    ## Selecting the biggest ball detected
    circle_index=0
    for i in range(len(x)):
        if r[i]>=r[circle_index]:
            circle_index=i
    print("H",h,"W",w,"Y",y[circle_index],"X",x[circle_index],"R",r[circle_index])
    ## Masking
    [color_det_r,M_r]=check_color(mask_r,h,w,x[circle_index],y[circle_index],r[circle_index])
    [color_det_y,M_y]=check_color(mask_y,h,w,x[circle_index],y[circle_index],r[circle_index])
    [color_det_g,M_g]=check_color(mask_g,h,w,x[circle_index],y[circle_index],r[circle_index])
    [color_det_b,M_b]=check_color(mask_b,h,w,x[circle_index],y[circle_index],r[circle_index])       
    
    ## Detecting the color (R,Y,G,B) of the ball             
    color_det=[color_det_r,color_det_y,color_det_g,color_det_b]
    M=[M_r,M_y,M_g,M_b]
    print(color_det)
    unknown_color=True
    for j in range(4):
        # Is the ball of a known color?
        if color_det[j]==True:
            if unknown_color==True:
                color_index=j
                unknown_color=False
            # To prioritize the color detected with smaller M
            if M[j]<M[color_index]:
                color_index=j
    if unknown_color==False:
        if color_index==0:
            object_color="RED"
        elif color_index==1:
            object_color="YELLOW"
        elif color_index==2:
            object_color="GREEN"
        elif color_index==3:
            object_color="BLUE"
    else:
        object_color="UNKNOWN"
    return object_color,x[circle_index]

############################################################################################################## 
#### TO BE COMPLETED #########################################################################################
def action_planner(color,x_pos,width):
    # This function needs to return the string variable named "robot_action" as follows:
    # if color="RED" then robot_action="MOVING FORWARD FOR 3 SECONDS"
    # if color="YELLOW then robot_action="FOLLOWING A SQUARE PATH"
    # if color="GREEN" then robot_action="FOLLOWING A CIRCULAR PATH"
    # if color="BLUE" then robot_action="TRACKING THE BALL", this will require to use variables "width" and "x_pos" 
    # Remember to activate the LEDs with the corresponding color while the robot is performing an action.
    activate_leds(color)
    if color=="RED":
        #Something here .......
        robot_action="MOVING FORWARD FOR 3 SECONDS"      
    elif color=="YELLOW":
        #Something here .......
        robot_action="FOLLOWING A SQUARE PATH"
    elif color=="GREEN":
        #Something here .......
        robot_action="FOLLOWING A CIRCULAR PATH"
    elif color=="BLUE":
        #Something here .......
        #This will require to use variables "width" and "x_pos" 
        robot_action="TRACKING THE BALL"
        
    return robot_action

def activate_leds(color):
    if color=="RED":
        tbot.fill_underlighting(RED)
    elif color=="YELLOW":
        tbot.fill_underlighting(YELLOW)
    elif color=="GREEN":
        tbot.fill_underlighting(GREEN)
    elif color=="BLUE":
        tbot.fill_underlighting(BLUE)   
##############################################################################################################    
##############################################################################################################

while True or KeyboardInterrupt:
    [image,width]=capture_image()
    [num_balls,x_pos,y_pos,radius]=circle_detection(image)
    if num_balls>0:
        [ball_color,ball_pos_x]=color_detection(image,x_pos,y_pos,radius)
        if ball_color!="UNKNOWN":
            #######################################################################################################################
            #### TO BE COMPLETED ##################################################################################################
            robot_action=action_planner(ball_color,ball_pos_x,width)            
            #######################################################################################################################
            #######################################################################################################################
            print("ACTION: ",robot_action)                         
        else:
            print("ACTION: ",ball_color) 
            tbot.fill_underlighting(BLACK)  
            tbot.disable_motors()
    else:
        print("NO BALLS DETECTED")
        tbot.fill_underlighting(BLACK)  
        tbot.disable_motors()
