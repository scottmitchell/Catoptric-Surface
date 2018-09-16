#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

#define MAGIC_NUM 33
#define NUM_ROWS 2

#define GET_MAGIC_NUM 0
#define GET_KEY 1
#define GET_X 2
#define GET_Y 3
#define GET_M 4
#define GET_D 5
#define GET_COUNT_HIGH 6
#define GET_COUNT_LOW 7

//Adafruit_MotorShield AFMS4 = Adafruit_MotorShield();
//Adafruit_StepperMotor *myMotor1 = AFMS4.getStepper(200, 1);
//Adafruit_StepperMotor *myMotor2 = AFMS.getStepper(200, 2);


Adafruit_MotorShield AFMS[NUM_ROWS];
Adafruit_StepperMotor *motors[NUM_ROWS][2];

int currentState = GET_MAGIC_NUM;
//int key = 0;
int x;
int y;
int m;
int d;
//int countLow;
int countHigh;
//int count; 

//Adafruit_StepperMotor *motor;


// Step a particular motor (x, y, m) 
// by a particular number of steps (d, c)
void stepMotor(int x, int y, int m, int d, int count) {
  int dir = d+1;
  motors[y-1][m]->setSpeed(100); 
  motors[y-1][m]->step(count, dir, DOUBLE);
  ackA(x, y, m);
  motors[y-1][m]->release(); 
}


void ackA(int x, int y, int m) {
  Serial.write(MAGIC_NUM);
  Serial.write('a');
  Serial.write('A');
  Serial.write(x);
  Serial.write(y);
  Serial.write(m);
}

/*
void debug(String message) {
  String prefix = "DEBUG: ";
  message = prefix + message;
  
  unsigned int len = message.length();
  unsigned int iLow;
  unsigned int iHigh;

  iHigh = (len >> 8) && 255;
  iLow = len;

  Serial.write(MAGIC_NUM);
  Serial.write('c');
  Serial.write(iHigh);
  Serial.write(iLow);
  for (int i = 0; i < len; i++) {
    Serial.write(message.charAt(i));
  }
}*/


void nack(String message) { 
  String prefix = "Nack: ";
  message = prefix + message;
  
  int len = message.length();
  int iLow;
  int iHigh;

  iLow = (len >> 8) && 255;
  iHigh = len && 255;

  Serial.write(MAGIC_NUM);
  Serial.write('b');
  Serial.write(iHigh);
  Serial.write(iLow);
  for (int i = 0; i < len; i++) {
    Serial.write(message.charAt(i));
  }
}


void setup() {
  // Open serial connection
  Serial.begin(9600);
  
  Serial.println("Test");
  // Initialize shields and motors
  for (int i = 0; i < NUM_ROWS; i++) {
    AFMS[i] = Adafruit_MotorShield(i + 0x40);
    for (int j = 0; j < 2; j++) {
      motors[i][j] = AFMS[i].getStepper(200, (j+1));
    }
    AFMS[i].begin();
  }
  Serial.println("Test2");
  
  
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() >= 1){
    unsigned char c = Serial.read();
    int nextState = currentState; //Default nextState
    switch (currentState) {

      case GET_MAGIC_NUM:
        if (c == MAGIC_NUM){
          nextState = GET_KEY;
        }
        break;

      case GET_KEY:
        //key = c;
        switch (c) {
          case 65:
            nextState = GET_X;
            break;
          default:
            nack("Invalid Key");
            nextState = GET_MAGIC_NUM;
            break;
        }
        break;

      case GET_X:
        if (c <= 50) {
          x = c;
          nextState = GET_Y;
        }
        else {
          nack("Invalid X");
          nextState = GET_MAGIC_NUM;
        }
        break;

      case GET_Y:
        if (c <= NUM_ROWS) {
          y = c;
          nextState = GET_M;
        }
        else {
          nack("Invalid Y");
          nextState = GET_MAGIC_NUM;
        }
        break;

      case GET_M:
        if (c <= 2) {
          m = c;
          nextState = GET_D;
        }
        else {
          nack("Invalid M");
          nextState = GET_MAGIC_NUM;
        }
        break;

      case GET_D:
        if (c <= 1) {
          d = c;
          nextState = GET_COUNT_HIGH;
        }
        else {
          nack("Invalid D");
          nextState = GET_MAGIC_NUM;
        }
        break;

      case GET_COUNT_HIGH:
        countHigh = c;
        nextState = GET_COUNT_LOW;
        break;

      case GET_COUNT_LOW:
        //countLow = c;
        int count = (countHigh << 8) + c; 

        stepMotor(x, y, m, d, count);
        
        nextState = GET_MAGIC_NUM;
        break;

    }
    currentState = nextState;
  }
}





