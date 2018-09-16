#include <Adafruit_MotorShield.h>

/* 
This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM
control

For use with the Adafruit Motor Shield v2 
---->	http://www.adafruit.com/products/1438
*/


#include <Wire.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
//Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x43); 
// Or, create it with a different I2C address (say for stacking)
//Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x63); 
#define NUM_ROWS 24
Adafruit_MotorShield AFMS[NUM_ROWS];
Adafruit_StepperMotor *motors[NUM_ROWS][2];

Adafruit_StepperMotor *motor;

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
//Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 1);


void setup() {
  // Open serial connection
  Serial.begin(9600);
  
  // Initialize shields and motors
  Serial.println("Before Loop");
  for (int i = 0; i < NUM_ROWS; i++) {
    Serial.print("Trying ");
    Serial.println(i);
    AFMS[i] = Adafruit_MotorShield(i + 0x41);
    for (int j = 0; j < 2; j++) {
      motors[i][j] = AFMS[i].getStepper(200, (j+1));
    }
    AFMS[i].begin();
  }
  Serial.println("After Loop");
  
  
}

void loop() {
  for (int i = 0; i < NUM_ROWS; i++) {
    motor = motors[i][0];
    motor->setSpeed(10);
    Serial.println("Single coil steps");
    motor->step(100, BACKWARD, SINGLE);

    motor = motors[i][1];
    motor->setSpeed(10);
    Serial.println("Single coil steps");
    motor->step(100, BACKWARD, SINGLE);
    motor->step(100, FORWARD, SINGLE);
    motor->release();

    motor = motors[i][0];
    motor->step(100, FORWARD, SINGLE);  
    motor->release();
  
    //Serial.println("Double coil steps");
    //motor->step(100, FORWARD, DOUBLE); 
    //motor->step(100, BACKWARD, DOUBLE);
  }
  
//  Serial.println("Interleave coil steps");
//  myMotor->step(100, FORWARD, INTERLEAVE); 
//  myMotor->step(100, BACKWARD, INTERLEAVE); 
//  
//  Serial.println("Microstep steps");
//  myMotor->step(50, FORWARD, MICROSTEP); 
//  myMotor->step(50, BACKWARD, MICROSTEP);
}
