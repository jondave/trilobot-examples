# Trilobot-examples
Example python scripts for the trilobot robot.

Clone this repository into the home directory of the trilobot ```git clone https://github.com/jondave/trilobot-examples.git```.

Change the directory to the scripts folder ```cd trilobot-examples/scripts```.

To run a python script enter the command ```python3 scriptname.py```, change "scriptname" to the name of python file.

E.g. flash the lights ```python3 flash_underlights.py```.

Or control the robot with the keyboard ```python3 keyboard_movements.py```.

# Trilobot Instructions
https://learn.pimoroni.com/article/assembling-trilobot

# Raspberry Pi Setup
Micro SD card should already have Pi OS installed connect a mini HDMI cable to a monitor and setup username, password wifi network etc.
 
If setting up headless (no monitor) it is better to reimage Pi OS on the SD card using the Raspberry Pi Imager https://www.raspberrypi.com/software/, https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2. Make sure to set a username, password and wifi network and  enable SSH.

Once the Pi is setup and running install the Trilobot software packages, in the Home directory;
!!DO NOT RUN THIS!!
Download v0.0.2 zip from GitHub don't git clone this. 
~~```git clone https://github.com/pimoroni/trilobot-python
cd trilobot-python
sudo ./install.sh```~~

```
wget https://github.com/pimoroni/trilobot-python/archive/refs/tags/v0.0.2.zip
unzip v0.0.2.zip
cd trilobot-python-0.0.2/
sudo ./install.sh
```

Then remove folder ```sudo rm -r ~/trilobot-python/```.

Make sure everything works run one of the example scripts
```
cd ~/Pimoroni/trilobot/examples
python3 flash_underlights.py
```

# VNC not showing desktop
```
sudo nano /boot/config.txt
```

Uncomment:
```
hdmi_force_hotplug=1
```

# Add Pi Camera V2 
If the camera not working gently push the black connector above the camera into the board, then reboot.

If still not working try:
```
sudo nano /boot/config.txt
```
Add at bottom:
```
dtoverlay=imx219
```
Use this for python code for camera.
https://raspberrytips.com/picamera2-raspberry-pi/
https://github.com/raspberrypi/picamera2/tree/main
https://github.com/raspberrypi/picamera2/tree/main/examples

When installed opencv ont use pip use:
```
sudo apt-get install python-opencv
```
