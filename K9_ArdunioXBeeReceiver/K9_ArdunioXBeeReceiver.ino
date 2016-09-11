//////////////////////////////////////////////////////////////////////////////////////////
//XBEE READER
//          - This sketch reads 3 byte bundles of data send from the python programme "K9_PyGameXBeeController.py"

////////////////////////////////////////////////////////////
//ISSUES
//           - None at current - BAUDRATE 115200 has fixed the lag situation -need to roll out testing to start moving servos and motors etc.
//          
//
//////////////////////////////////////////////////////////////
//WIRING AND SETUP
//          - The receiver XBee is powered by the XBee adaptor through the 5V USB connection - This also allows limited access to data passing through in XCTU
//          - 3.3v pin is connected to Ardunio 3.3v ouput - NOT 5V! 
//          - Ground is connected to Ardunio
//          - Data Out (DOUT) is connect to Ardunio RX. This is the only attachment. Do not attach TX in this setup, since this stops data somehow working/getting to the serial monitor
//          - Check Wiring diagram on image in the same folder
//          - Ardunio has standard 5V USB supply, which also allows the serial monitor to be opened and for the data to be read through. These print statements might be slowing the system.


int startbyte;       // start byte, begin reading input
int servoNumber;
int servoAngle;
int i;              // for counting
int signatureNumber = 255; //Probably change this to 255 when we start sending stuff from Python

//Setup servos
#include <Servo.h> 

//Create a Servo object for each servo 
Servo servo7;
Servo servo8;
Servo servo9;
Servo servo10;

// Common servo setup values
int minPulse = 1500;   // minimum servo position, us (microseconds)
int maxPulse = 2400;  // maximum servo position, us


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); //Highest Rate that the XBees can handle - fast enough to handle 2 or 3 channels of continually changing joystick data at least

  // Attach each Servo object to a digital pin
  servo7.attach(7, minPulse, maxPulse);
  servo8.attach(8, minPulse, maxPulse);
  servo9.attach(9, minPulse, maxPulse);
  servo10.attach(10, minPulse, maxPulse);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 2) {   //Wait for there to be 3 items in the buffer
    // Read the first byte
    if (Serial.read() == signatureNumber) {    //Read the first one and make sure that it our special character - by reading it we move one character forward in our serial group of 3 characters
      Serial.println("We have a start character now read the next two for servo and Angle");  //Character is our signature character so we are good go! 
      for (i=0;i<=1;i++) { //Read the next two characters and process them as the servo number and the servo Angle
        //userInput[i] = Serial.read();   
        if (i == 0) {
          servoNumber = Serial.read();   //Read the servo number
          Serial.println("Printing Servo Number:");
          Serial.println(servoNumber);   //This will print the number relating to the 8 bit ascii character
        }
        else if (i == 1) {
          servoAngle = Serial.read();  //Read the servo Angle
          Serial.println("Printing Servo Angle:");
          Serial.println(servoAngle);   //This will print the number relating to the 8 bit ascii character
        }  
    
    }
    //Now that we have established the servo number and angle then use if statement to choose the right servo and move it! 
    if (servoNumber == 7) {
      servo7.write(servoAngle);      
      } // end of servoNumber 7
    else if (servoNumber == 8){
      servo8.write(servoAngle); 
      } // end of servoNumber 8
    else if (servoNumber == 9){
      servo9.write(servoAngle); 
      } // end of servoNumber 9
    else if (servoNumber == 10){
      servo10.write(servoAngle); 
      } // end of servoNumber 10     
    }
    else {  //The signature character is not correct so print that we are ignoring this character and wait for the buffer to build back to 3 again
      Serial.println("No relevant start character - ignoring"); 
      }
    }// End of serial available
   } // End of Loop 

  

