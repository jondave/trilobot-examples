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

def detect_faces():
    stream = io.BytesIO()

    # capture an image
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    # create an image buffer
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)

    # assign the image from the cv2 buffer
    image = cv2.imdecode(buff, 1)

    # import the cascade file - needs to be in the same folder
    face_cascade = cv2.CascadeClassifier('~/trilobot-examples/config/haarcascade_frontalface_default.xml')

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print("Found " + str(len(faces)) + " face(s)")
    if len(faces) > 0:
        green_light()
    else:
        blue_light()
    return faces, image
   
def write_file(faces, image, filename):
    # write file
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+w,y+h),(255,255,0),4)

    cv2.imwrite(filename, image)

while True or KeyboardInterrupt:
    faces, image = detect_faces()
    # write_file(faces, image, filaneme='result.jpg')
