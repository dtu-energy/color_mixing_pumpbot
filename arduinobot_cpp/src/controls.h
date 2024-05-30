#include <Arduino.h>
#include <Wire.h>
#include <Qwiic_LED_Stick.h>
#include <Adafruit_TCS34725.h>
#include <SPI.h>

LED ledStick;  // Define the Qwiic LED Stick

// Define RGB Sensor
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

void pinSetup() {
    // Define Pump PinModes
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);

    pinMode(8, OUTPUT); // Inactive Pin
    pinMode(9, OUTPUT); // Inactive Pin


    // HIGH when RELAY
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);

    // FOR TESTING
    // pinMode(13, OUTPUT);
    // digitalWrite(13, LOW);
}

void colorMeasSetup() {

    // Begin LED and RGB Sensor
    Wire.begin();
    ledStick.begin();
    tcs.begin();
    tcs.setInterrupt(true); // Turn off sensor light
}

void stopPump(int pin) {
    // Deactivate a given pump

    //digitalWrite(pin, LOW); // LOW when LED (FOR TESTING)

    digitalWrite(pin, HIGH); // HIGH when relay
    
}

void runPump(int pin, float duration) {
    // Activate a given pump

    //digitalWrite(pin, HIGH); // HIGH when LED (FOR TESTING)

    digitalWrite(pin, LOW); // LOW when relay
    delay(duration * 1000);
    stopPump(pin);
}

void runMeasurement() {
    ledStick.LEDOff();
    ledStick.setLEDBrightness(31); // Set max brightness

    // Turn on bottom 6 leds to white
    ledStick.setLEDColor(3, 255, 255, 255);
    ledStick.setLEDColor(4, 255, 255, 255);
    ledStick.setLEDColor(5, 255, 255, 255);
    ledStick.setLEDColor(6, 255, 255, 255);
    ledStick.setLEDColor(7, 255, 255, 255);
    ledStick.setLEDColor(8, 255, 255, 255);
    ledStick.setLEDColor(9, 255, 255, 255);

    delay(500); 

    // Take 3 measurements
    float red = 0.0, green =  0.0, blue = 0.0;
    for (int i = 0; i < 3; i++) {
        tcs.getRGB(&red, &green, &blue);
        
        red += red;
        green += green;
        blue += blue;

        delay(100); // Add a short delay between measurements
    }

    delay(500);
    ledStick.LEDOff();

    // Get average of 3 measurements
    red /= 3.0;
    green /= 3.0;
    blue /= 3.0;

    // Send RGB data to PC
    Serial.print("<RGB:");
    Serial.print(int(red));
    Serial.print(",");
    Serial.print(int(green));
    Serial.print(",");
    Serial.print(int(blue));
    Serial.println(">");

}



