import io
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

def distance_detection():
    # Take 10 measurements rapidly
    for i in range(10):
        clock_check = time.perf_counter()
        distance = tbot.read_distance(timeout=25, samples=3)
        #print("Rapid:  Distance is {:.1f} cm (took {:.4f} sec)".format(distance, (time.perf_counter() - clock_check)))
        time.sleep(0.01)

    # Take 10 measurements allowing longer time for measuring greater distances
    for i in range(10):
        clock_check = time.perf_counter()
        distance = tbot.read_distance(timeout=200, samples=9)
        #print("Slower: Distance is {:.1f} cm (took {:.4f} sec)".format(distance, (time.perf_counter() - clock_check)))
        time.sleep(0.01)
    return distance

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
    
    search_top = int(h/2 - h/5)
    search_bot = int(h/2 + h/5)
    search_left = int(w/2 - w/5)
    search_right = int(w/2 + w/5)
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
    #print("ERROR",err)
    #result=cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
    #cv2.imwrite("result.png", result)
    
    #cv2.imshow("result",result)
    #cv2.waitKey(1)
    # CONTROL starts
    
    return [cx,cy,err]

def color_detection(image):
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

    ## final mask and masked
    #mask = cv2.bitwise_or(mask1, mask2)
    #target = cv2.bitwise_and(img,img, mask=mask)
    #cv2.imwrite("mask_g.png", mask_g)
    #cv2.imwrite("mask_y.png", mask_y)
    #cv2.imwrite("mask_r.png", mask_r)
    #cv2.imwrite("mask_b.png", mask_b)

    h, w, d = image.shape

    [color_det_r,M_r]=check_color(mask_r,h,w)
    [color_det_y,M_y]=check_color(mask_y,h,w)
    [color_det_g,M_g]=check_color(mask_g,h,w)
    [color_det_b,M_b]=check_color(mask_b,h,w)
    
    color_det=[color_det_r,color_det_y,color_det_g,color_det_b]
    M00=[M_r['m00'],M_y['m00'],M_g['m00'],M_b['m00']]
    print("color_det",color_det)
    print("M",M00)
    unknown_color=True
    for i in range(4):
        if color_det[i]==True:
            if unknown_color==True:
                index=i
                unknown_color=False
            if M00[i] < M00[index]:
                index=i
    if unknown_color==False:
        print("Index",index)
        if index==0:
            object_color="RED OBJECT"
            object_pos=locate_color(M_r,w,image)
            tbot.fill_underlighting(RED)
        elif index==1:
            object_color="YELLOW OBJECT"
            object_pos=locate_color(M_y,w,image)
            tbot.fill_underlighting(YELLOW)
        elif index==2:
            object_color="GREEN OBJECT"
            object_pos=locate_color(M_g,w,image)
            tbot.fill_underlighting(GREEN)
        elif index==3:
            object_color="BLUE OBJECT"
            object_pos=locate_color(M_b,w,image)
            tbot.fill_underlighting(BLUE)
    else:
        object_color="UNKNOWN COLOR"
        object_pos=[0,0,0]
        tbot.fill_underlighting(BLACK)    
        
    return object_color,object_pos
        
    '''
    if color_det_r==True:
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
                    tbot.fill_underlighting(BLACK)            
       '''                 
while True or KeyboardInterrupt:
    distance=distance_detection()
    if distance<30: #30cm threshold
        image=capture_image()
        [object_color,object_pos]=color_detection(image)
        print(object_color)
    else:
        print("NO OBJECT DETECTED")
        tbot.fill_underlighting(BLACK)   
