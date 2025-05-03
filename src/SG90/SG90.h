#ifndef SERVO_H
#define SERVO_H

#include <ESP32Servo.h>
extern Servo myServo;

void initServo(int servoPin);
void unlockUmbrella(int ButtonNum);
#endif