##TEST CODE
# When using X Box controller the buttons can be pressed to send data:
# Press A - Sends chr(255), chr(47) (servo number), chr(80) (angle)
# Press B - Sends chr(255), chr(47) (servo number), chr(120) (angle)

#Use extended asci tables to convert data

#This setup is verbose, but the print statements at the python end do not really result in a lag to the system.
#From this template create as many instances of "ServoSend(1,8)" as needed and map them out the servos required at the ardunio end

###############################################################################
##Receiver Ardunio should be running the "K9_ArdunioXBeeReceiver.ino" sketch.

##########################################################################
##TO DO:
##      - Currently reporting ardunio number in servo send which is not needed. Just use the servo number with if statements at the Ardunio end to map commands out to the write pins/operations
##      - Clean up this code to remove a lot of the joystick testing statements - However, currently speed issues are not down to this code

#################################################
##SETUP
##      - Current Baudrate is 115,200 - maximum baudrate is working really well
##      - 'xBeeCoordinator' - refers to the com port that the PC attached XBee is connected to. The one that should send out all the signals
##      - We want to send as little data as possible, so lets work out motor speeds here, and just send the two motor speeds, so the ardunio does not have to do many calculations
##  


import pygame
import serial
import math

#Define Serial Setup
xBeeCoordinator = 'COM9' #Comport for Arduino - Adapt it we end up sending data via blue tooth

# Set up serial baud rate
ser = serial.Serial(xBeeCoordinator, 115200, timeout=1)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

print "Initiated Stage: 1"
# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printJoy(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    

class MotorSpeedSend(object):
    def __init__(self, motorNumber):
        self.motorNumber = motorNumber
        self.speedSeparation = 5
        self.currentSpeed = 128

    def getAngleSeparation(self):
        return self.angleSeparation

    def setSpeedSeparation(self, aSeparation):
        self.angleSeparation = aSeparation

    def setSpeed(self, speed):
        '''Changes the required DC motor to the new speed.
        Arguments:
            speed
              the desired motor speed to change to an integer from 0 to 255'''

        if (0 <= speed <= 255):
            print "About to send 255"
            ser.write(chr(255))
            print "Sending Motor Number"
            ser.write(chr(self.motorNumber))
            print "Sending Motor speed"
            ser.write(chr(speed))
        else:
            print("Motor speed must be an integer between 0 and 255.\n")

    def sendSpeed(self, newSpeed):
        """Function to be called when a motro speed wants to be sent. First of all the function checks to see
        if there is enough difference in the new speed from the current speed"""
        if abs(self.currentSpeed - newSpeed) > self.speedSeparation:
            #Difference found, so send out the new speed, and then update the current speed
            self.setSpeed(newSpeed)
            self.currentSpeed = newSpeed



#NOW we create the MotorSpeedSend classes to calculate the speed for the left and right motors
forwardMotorSpeed = 0 #This is just an indicator for if the motor is going forward or backwards
motorTurn = 0
motorTurnScale = 0.6
finalLeftMotorSpeed = 0
finalRightMotorSpeed = 0
leftMotorSpeed = 0  #Set inital 0 motoro Speed
rightMotorSpeed = 0 #Set intial 0 motor Speed
swivelSpeed = 30 #Set the turn difference for when we swivel on the spot. This accelerates one motor and slows the other


motorLeft = MotorSpeedSend(10) #Maps to pin 10
motorRight = MotorSpeedSend(11) #Maps to pin 11
turnScaleFactor = 0.1 #This value scales the amount that the turn influence values influences the changes in the motor speeds. 0 < Value < 1. Values closer to 1 will produce very sudden turning influences

speedSeparation = 0 #This is the change required in speed before a new speed is sent again
motorLeft.setSpeedSeparation(speedSeparation)
motorRight.setSpeedSeparation(speedSeparation)


def mapAxisToSpeed(axisValue, percentageRange = 100):
    '''Maps an axis value that is being recieved from a joystick (-1 to 1) to a speed (-90 to 90)'''
    returnSpeed = (axisValue*(percentageRange/100.0))
    #print "Return Angle = " + str(returnAngle)
    return returnSpeed

def mapAxisToTurn(axisValue):
    '''Maps an axis value that is being recieved from a joystick (-1 to 1) to a turn (-90 to 90)'''
    returnTurn = (axisValue)
    #print "Return Angle = " + str(returnAngle)
    return returnTurn


def speedLimitCheck(speed):
    '''Function to check that the resulting speed after all turn adjustments lands between 0 and 255'''
    finalSpeed = speed
    if speed > 255:
        finalSpeed =  255
    elif speed < 0:
        finalSpeed =  0
    else:
        finalSpeed = speed
    return finalSpeed 

#####################################################################################################################################
print "PYGAME is about to initialise"
pygame.init()
print "PYGAME has initialised"

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

print "PYGAME is about to initialise joystick"
# Initialize the joysticks
pygame.joystick.init()
print "PYGAME has run Joystick launch Function"

# Get ready to print
textPrint = TextPrint()


# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        """if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            """
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    #print "PYGAME has counted joysticks"
    #textPrint.printJoy(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    #textPrint.printJoy(screen, "moo")
    
    # For each joystick:
    for joy in range(joystick_count):
        joystick = pygame.joystick.Joystick(joy)
        joystick.init()
    
        #textPrint.printJoy(screen, "Joystick {}".format(joy) )
        #textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printJoy(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        #textPrint.printJoy(screen, "Number of axes: {}".format(axes) )
        #textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            #textPrint.printJoy(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            if joy == 0:
                if i == 0 : #We have the left joystick horizontal axis - Hardcode some Servo movements
                    motorTurn = mapAxisToTurn(axis) * motorTurnScale # Calculate the turning influence from the joystick
                elif i == 1 : #We have the left joystick Vertical axis - This is the main speed value, without any factors for turning
                    forwardMotorSpeed = -mapAxisToSpeed(axis)
                    textPrint.printJoy(screen, ("Motor Speed  : " + str(forwardMotorSpeed)))
                elif i == 4 : #We have the right joystick horizontal axis - Hardcode some Servo movements
                    pass
                    #textPrint.printJoy(screen, ("Axis 4: Right Horizontal Stick - Angle : " + str(servoAngle)))
                elif i == 2 : #Trigger
                    pass
            elif joy == 1:
                if i == 0 : #We have the left joystick horizontal axis - Hardcode some Servo movements
                    pass
                elif i == 4 : #We have the right joystick horizontal axis - Hardcode some Servo movements
                    pass

        #Now that we have calculated the joystick axes then we can send the final motor speeds mapped to 0-255
        
        if motorTurn > 0:
            finalLeftMotorSpeed = 128*(forwardMotorSpeed) + 127
            finalRightMotorSpeed = 128*(forwardMotorSpeed * (1 - motorTurn)) + 127
        elif motorTurn <= 0:
            finalLeftMotorSpeed = 128*(forwardMotorSpeed * (1 + motorTurn)) + 127
            finalRightMotorSpeed = 128*(forwardMotorSpeed) + 127
        
        finalLeftMotorSpeed = int(finalLeftMotorSpeed)
        finalRightMotorSpeed = int(finalRightMotorSpeed)
        

            
        buttons = joystick.get_numbuttons()
        #textPrint.printJoy(screen, "Number of buttons: {}".format(buttons) )
        #textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            #textPrint.printJoy(screen, "Button {:>2} value: {}".format(i,button) )
            if i == 0 and button:
                print "Button 'A' Pressed"
                #servoHeadTilt.sendAngle(120) 
            elif i == 1 and button: 
                print "Button 'B' Pressed"
                #servoHeadTilt.sendAngle(80) 
        
        #textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        #textPrint.printJoy(screen, "Number of hats: {}".format(hats) )
        #textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            #print "Hat pressed " + str()
            textPrint.printJoy(screen, "Hat {} value: {}".format(i, str(hat)) )
            x,y = hat
            textPrint.printJoy(screen, "HatX" + str(x))
            if x == -1: #Left hat button is pressed
                finalLeftMotorSpeed = speedLimitCheck(finalLeftMotorSpeed - swivelSpeed)
                finalRightMotorSpeed = speedLimitCheck(finalRightMotorSpeed + swivelSpeed)
            elif x == 1: #Right hat button is pressed
                finalLeftMotorSpeed = speedLimitCheck(finalLeftMotorSpeed + swivelSpeed)
                finalRightMotorSpeed = speedLimitCheck(finalRightMotorSpeed - swivelSpeed)

        #textPrint.unindent()
        
        #textPrint.unindent()
        textPrint.printJoy(screen, ("Motor  Out Loop Speed  : " + str(forwardMotorSpeed)))
        textPrint.printJoy(screen, ("Turn Value : " + str(motorTurn)))
        textPrint.printJoy(screen, ("Final Left Motor Speed  : " + str(finalLeftMotorSpeed)))
        textPrint.printJoy(screen, ("Final Right Motor Speed : " + str(finalRightMotorSpeed)))

        motorLeft.sendSpeed(finalLeftMotorSpeed)
        motorRight.sendSpeed(finalRightMotorSpeed)

        textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
