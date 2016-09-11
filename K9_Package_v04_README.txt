#########################################################################
#AUTHOR: Richard Jones
#
#########################################################################

This is a verbose working proof of principle of a joystick controlling complex movement on an Ardunio through a pygame python programme and XBee communication
This version (03) includes the integration of servos being moved to do the next stage of the speed test

SETUP:
	- Follow instruction at the top of "K9_PyGameXBeeController.py" and "K9_ArdunioXBeeReceiver.ino"
	- Follow wiring diagram in image "K9_ArdunioXBee_Wiring.jpg"
	- BaudRate is no set at 115200 (Fastest the XBees can Manage) - Working ad solves lag
	- Now setting up to drive DC motors with precise speed control.


ISSUES:
	- None at this stage. Baudrate of 115,200 which needs to be adjusted on python, ardunio and Xbees has fixed the lag issue. 
	- As such the ardunio print statements are not the end of the world. So they have been left in for reporting to the monitor. 

DONE:
	- Tested the link and read out to a second computer to ensure that the setup is completely independent
	- Wired in the servos, so start moving servos to precise positions

TO DO:
	- Looking at code for motors and coding to get motors running at precise speeds
	


