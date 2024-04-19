#include <digitalWriteFast.h>
#include <Keyboard.h>
#include "Stepper.h"

// This script receives commands from the Rasp-pi txrx.py script and then sends pulse signals to the stepper motor drivers

// GPIO CONFIGURATION----------------
const int STEP1 = 6;
const int DIR1 = 5;

// VARIABLE CONSTANTS----------------
// General
String msg_rx = "";
unsigned long cur_micros;
// Motor 1 (left drive)
unsigned long last_micros_1 = 0;
unsigned long delay_micros_1 = 6000;
unsigned long delay_increment_1 = 26;
boolean is_stopped_1 = true;
// Motor 2 (right drive)
// Motor 3 (yaw)
// Motor 4 (pitch)

// FIXED CONSTANTS----------------
// Drive motors (1 & 2)
const unsigned long MIN_DELAY = 600;  // Fastest speed
const unsigned long MAX_DELAY = 6000; // Slowest speed

//Stepper::Stepper(int step_pin, int dir_pin, int min_delay=600, int max_delay=6000, boolean starting_dir=1)

Stepper stepper1 = Stepper(6, 5);

void setup() {
  // put your setup code here, to run once:
    Serial.begin(115200);

    pinMode(STEP1, OUTPUT);
    pinMode(DIR1, OUTPUT);
    digitalWriteFast(DIR1, HIGH);
    while (!Serial) {  
    }
    Serial.println("Serial initialized");
}


void loop() {
    cur_micros = micros();
    
    if (Serial.available() > 0) {
        msg_rx = Serial.readStringUntil('\n');
        //Serial.println(msg_rx);
    }
    /*
    if (cur_micros < 2000000) {
        stepper1.goForward(cur_micros);
    }
    
    if (cur_micros > 2000000 && cur_micros < 5000000) {
        stepper1.goBackward(cur_micros);
    } else if (cur_micros > 5000000){
        stepper1.goForward(cur_micros);
    }*/

    
    
    // command: up (U), down (D), left (L), right (R), stop (S)
    if (msg_rx == "U") {
        // accel L
        stepper1.goForward(cur_micros);
        // accel R
    } else if (msg_rx == "D"){
        // decel L
        stepper1.goBackward(cur_micros);
        // decel R
    } else if (msg_rx == "L") {
        // accel L
        // decel R
    } else if (msg_rx == "R") {
        // decel L
        // accel R
    } else{
        // both motors go to zero
        stepper1.decelerate(cur_micros);
    }

    //delay(500);
}


void goForward(int step_pin, int dir_pin, unsigned long min_delay, unsigned long &delay_micros, unsigned long &last_micros, unsigned long &delay_increment) {

}

void goBackward() {

}

void stopMotor() {
    
}


/* sending to rpi
void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hello from Arduino");
  delay(5000);
}
*/
