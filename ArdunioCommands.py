
##A library of commands that can setup instructions for different purposes on the Ardunio
import serial
import math


#Class to record the appropirate pin number/ardunio identifier and then send messages via Serial (XBee) that the ardunio will be able to decode and send to pins to control devices
class MotorSpeedSend(object):
    def __init__(self, serial, motorNumber):
        self.motorNumber = motorNumber
        self.speedSeparation = 5
        self.currentSpeed = 128
        self.serial = serial

    def getAngleSeparation(self):
        return self.angleSeparation

    def setSpeedSeparation(self, aSeparation):
        self.angleSeparation = aSeparation

    def setSpeed(self, speed):
        '''Changes the required DC motor to the new speed.
        Arguments:
            speed
              the desired motor speed to change to an integer from 0 to 255'''
        finalSpeed = self.speedLimitCheck(speed)
        print "\nAbout to send 255"
        self.serial.write(chr(255))
        print "Sending Motor Number"
        self.serial.write(chr(self.motorNumber))
        print "Sending Motor speed"
        self.serial.write(chr(finalSpeed))
        return finalSpeed

    def sendSpeed(self, newSpeed):
        """Function to be called when a motro speed wants to be sent. First of all the function checks to see
        if there is enough difference in the new speed from the current speed"""
        if abs(self.currentSpeed - newSpeed) > self.speedSeparation:
            #Difference found, so send out the new speed, and then update the current speed
            self.currentSpeed = self.setSpeed(newSpeed)
	
    def speedLimitCheck(self, speed):
	    '''Function to check that the resulting speed after all turn adjustments lands between 0 and 255'''
	    finalSpeed = speed
	    if speed > 254:
	        finalSpeed =  254
	    elif speed < 0:
	        finalSpeed =  0
	    else:
	        finalSpeed = speed
	    return finalSpeed 