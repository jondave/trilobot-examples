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
    '''
    for i in range(10):
        clock_check = time.perf_counter()
        distance = tbot.read_distance(timeout=200, samples=9)
        #print("Slower: Distance is {:.1f} cm (took {:.4f} sec)".format(distance, (time.perf_counter() - clock_check)))
        time.sleep(0.01)
    '''
    return distance

def capture_image():
    # stream = io.BytesIO()
    # capture an image
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 24
        time.sleep(2)
        image = numpy.empty((240 * 320 * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((240, 320, 3))
    '''
        camera.resolution = (320, 240)
        camera.framerate = 24
        camera.capture(stream, format='jpeg')
    # create an image buffer
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
    # assign the image from the cv2 buffer
    image = cv2.imdecode(buff, 1) 
    '''
    return image
  
def circle_detection(image):  
    # Convert to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 100,
                   param2 = 50, minRadius = 0, maxRadius = 0)
    # Count and locate the circles that are detected.
    x=[] # list with x component of the circles detected
    y=[] # list with y component of the circles detected
    r=[] # list with the radius of the circles detected
    if detected_circles is not None:
        tbot.fill_underlighting(RED)
        num_circles=len(detected_circles[0,:,0])  
        # Convert the circle parameters x, y and r to integers.
        detected_circles = numpy.uint16(numpy.around(detected_circles))
        for pt in detected_circles[0,:]:
            x.append(pt[0])
            y.append(pt[1])
            r.append(pt[2])
    else:
        num_circles=0
        tbot.fill_underlighting(BLACK)
    return num_circles,x,y,r
        
while True or KeyboardInterrupt:
    distance=distance_detection()
    if distance<50: #50cm threshold
        image=capture_image()
        num_balls=circle_detection(image)
        print("NUMBER OF BALLS:",num_balls)
    else:
        print("NO BALLS DETECTED")
        tbot.fill_underlighting(BLACK) 
