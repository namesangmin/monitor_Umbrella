#ifndef SERVO_H
#define SERVO_H

#include <ESP32Servo.h>
extern Servo myServo;

void initServo(int servoPin);
void Rental_unlockUmbrella(int ButtonNum);
void Return_unlockUmbrella(int ButtonNum);
#endif