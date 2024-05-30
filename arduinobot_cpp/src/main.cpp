#include <Arduino.h>
#include <Wire.h>
#include <comms.h>
#include <Qwiic_LED_Stick.h>
#include <Adafruit_TCS34725.h>
#include <SPI.h>

void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>"); // Tell PC we are ready

  pinSetup(); // Activate output pins and set default values
  colorMeasSetup(); // Begin LED and RGB Sensor
}

void loop() {
  curMillis = millis();
  getDataFromPC();
  // replyToPC();
}

