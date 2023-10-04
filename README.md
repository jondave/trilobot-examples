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
```
git clone https://github.com/pimoroni/trilobot-python
cd trilobot-python
sudo ./install.sh
```

Then remove folder ```sudo rm -r ~/trilobot-python/```.

Make sure everything works run one of the example scripts
```
cd ~/Pimoroni/trilobot/examples
python3 flash_underlights.py
```

If there is an error about sn3218 package install the older version;
```
pip install sn3218==1.2.7 
pip3 install sn3218==1.2.7 
```

Also may need to install trilotbot python package;
```
pip install trilobot 
pip3 install trilobot
```

# VNC not showing desktop
```
sudo nano /boot/config.txt
```

Uncomment:
```
hdmi_force_hotplug=1
```
