#ifndef BUTTON_H
#define BUTTON_H

#include <Arduino.h>
// ESP32 버튼 핀 셋팅값(우산)
// 일단 5개임 더 늘릴 수 있는데 가지고 있는 버튼이 5개 밖에 없음
extern const int Umbrella1Pin;
extern const int Umbrella2Pin;
extern const int Umbrella3Pin;
extern const int ReturnPin;
extern const int RentalPin;

void initButton();
int UmbrellaButton();
int waitForButtonPress();
String waitForAction();
#endif