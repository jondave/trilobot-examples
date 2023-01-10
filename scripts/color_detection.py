import io
import picamera
import cv2
import numpy
from trilobot import *

# create the robot object
tbot = Trilobot()

# Colors codes
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def capture_image():
    stream = io.BytesIO()
    # capture an image
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')
    # create an image buffer
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
    # assign the image from the cv2 buffer
    image = cv2.imdecode(buff, 1) 
    return image
  
def check_color(mask,h,w):
    
    search_top = int(h/2 - h/4)
    search_bot = int(h/2 + h/4)
    search_left = int(w/2 - w/4)
    search_right = int(w/2 + w/4)
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask[0:h, 0:search_left] = 0
    mask[0:h, search_right:w] = 0
    
    M = cv2.moments(mask)
    if M['m00'] > 0:
        color_det=True
    else:
        color_det=False
    return color_det,M

def locate_color(M,w,image):
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    err = cx - w/2
    print("ERROR",err)
    result=cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
    cv2.imwrite("result.png", result)
    
    #cv2.imshow("result",result)
    #cv2.waitKey(1)
    # CONTROL starts
    
    return cx,cy,err

def color_detection(image):
    ## convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    ## mask of red (15,0,0) ~ (36, 255, 255)
    mask_r = cv2.inRange(hsv, (2,0,0), (10, 255, 255))
    ## mask of yellow (15,0,0) ~ (36, 255, 255)
    mask_y = cv2.inRange(hsv, (15,0,0), (36, 255, 255))
    ## mask of green (36,0,0) ~ (70, 255,255)
    mask_g = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
    ## mask of blue (15,0,0) ~ (36, 255, 255)
    mask_b = cv2.inRange(hsv, (100,0,0), (135, 255, 255))

    ## final mask and masked
    #mask = cv2.bitwise_or(mask1, mask2)
    #target = cv2.bitwise_and(img,img, mask=mask)
    cv2.imwrite("mask_g.png", mask_g)
    cv2.imwrite("mask_y.png", mask_y)
    cv2.imwrite("mask_r.png", mask_r)
    cv2.imwrite("mask_b.png", mask_b)

    h, w, d = image.shape

    color_det=False
    mask=mask_r
    [color_det,M]=check_color(mask,h,w)
    if color_det==True:
        print("RED")
        locate_color(M,w,image)
        tbot.fill_underlighting(RED)
    else:
        mask=mask_y
        [color_det,M]=check_color(mask,h,w)
        if color_det==True:
            print("YELLOW")
            locate_color(M,w,image)
            tbot.fill_underlighting(YELLOW)
        else:
            mask=mask_g
            [color_det,M]=check_color(mask,h,w)
            if color_det==True:
                print("GREEN")
                locate_color(M,w,image)
                tbot.fill_underlighting(GREEN)
            else:
                mask=mask_b
                [color_det,M]=check_color(mask,h,w)
                if color_det==True:
                    print("BLUE")
                    locate_color(M,w,image)
                    tbot.fill_underlighting(BLUE)
                else: #no color
                    print("NO COLOR")
                    tbot.fill_underlighting(BLUE)            
                        
while True or KeyboardInterrupt:
    image=capture_image()
    color_detection(image)
