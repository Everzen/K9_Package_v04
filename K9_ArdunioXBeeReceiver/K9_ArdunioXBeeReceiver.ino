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
//
//IMPLEMENTATION
//          - Converting this to run DC motors and deciding which way to run them: Forward or in reverse. 

int startbyte;       // start byte, begin reading input
int motorNumber;
int motorSpeed;
int isMotorForward; 
int i;              // for counting
int signatureNumber = 255; //Probably change this to 255 when we start sending stuff from Python

//Adding in definitions to try and 
#define E1 10  // Enable Pin for motor 1
#define E2 11  // Enable Pin for motor 2
 
#define I1 8  // Control pin 1 for motor 1
#define I2 9  // Control pin 2 for motor 1
#define I3 12  // Control pin 1 for motor 2
#define I4 13  // Control pin 2 for motor 2


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); //Highest Rate that the XBees can handle - fast enough to handle 2 or 3 channels of continually changing joystick data at least
  pinMode(motorPinLeft, OUTPUT);
  pinMode(mortorPinRight, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 2) {   //Wait for there to be 3 items in the buffer
    // Read the first byte
    if (Serial.read() == signatureNumber) {    //Read the first one and make sure that it our special character - by reading it we move one character forward in our serial group of 3 characters
      Serial.println("We have a start character now read the next two for motor and speed");  //Character is our signature character so we are good go! 
      for (i=0;i<=1;i++) { //Read the next two characters and process them as the servo number and the servo Angle
        //userInput[i] = Serial.read();   
        if (i == 0) {
          motorNumber = Serial.read();   //Read the servo number
          Serial.println("Printing Motor Number:");
          Serial.println(motorNumber);   //This will print the number relating to the 8 bit ascii character
        }
        else if (i == 1) {
          motorSpeed = Serial.read() - 127;  //Read the motorspeed 0-254 and minus 127 from it to get a number balanced around 0. + is forward - is backwards
          Serial.println("Printing Motor Speed:");
          Serial.println(motorSpeed);   //This will print the number relating to the 8 bit ascii character
        }  
    
    }
    
    //Now that we have established the motor number and speed we need to get the speed and say whether we are going forward or backwards
    if (motorSpeed >= 0) //Motor is driging forward
      {
      isMotorForward = 1
      }
    else  //Motor is driving backwards
      {
      isMotorForward = 0
      motorspeed = abs(motorspeed)
      } 


    if (motorNumber == 7) {
      servo7.write(motorSpeed);      
      } // end of motorNumber 7
    else if (motorNumber == 8){
      servo8.write(motorSpeed); 
      } // end of motorNumber 8
    else if (motorNumber == 9){
      servo9.write(motorSpeed); 
      } // end of motorNumber 9
    else if (motorNumber == 10){
      servo10.write(motorSpeed); 
      } // end of motorNumber 10     
    }
    else {  //The signature character is not correct so print that we are ignoring this character and wait for the buffer to build back to 3 again
      Serial.println("No relevant start character - ignoring"); 
      }
    }// End of serial available
   } // End of Loop 

  

