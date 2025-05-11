#ifndef SERVO_H
#define SERVO_H
#include <ESP32Servo.h>

void initServo(int servoPin);
void Rental_unlockUmbrella(int ButtonNum);
void Return_unlockUmbrella(int ButtonNum);

extern Servo myServo;
#endif