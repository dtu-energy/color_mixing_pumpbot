#include <Arduino.h>
#include <controls.h>


const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};
float duration = 0.0;
int pin;

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;

//=============

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
} 

//=============
void parseData() {

    // send data back to PC
    strcpy(messageFromPC, inputBuffer); 
    // replyToPC();

    // split the data into its parts
    
    char * strtokIndx; // used by strtok() as an index
  
    strtokIndx = strtok(inputBuffer,",");  // split the data into parts based on command
    

    if (strcmp(strtokIndx, "Mix") == 0) {
        // Handle Mix command

        // Get activated pin
        strtokIndx = strtok(NULL, ",");
        pin = atoi(strtokIndx);

        // Get and Set Pump Time
        strtokIndx = strtok(NULL, ",");
        duration = atof(strtokIndx);

        runPump(pin, duration);

        replyToPC();

    } else if (strcmp(strtokIndx, "Meas") == 0) {
        replyToPC();
        runMeasurement();
    } else {
        replyToPC();
        // Error handling for wrong main command
    }

    


}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}
 





