#include "SG90.h"

Servo myServo;

void initServo(int servoPin) {
    // put your setup code here, to run once:
    myServo.attach(servoPin);
    myServo.write(0);
  }

  
void unlockUmbrella(int ButtonNum){
    Serial.printf("우산 %d번 모터 작동 중...\n", index);
    myServo.write(90);   // 잠금 해제
    delay(1000);
    myServo.write(0);    // 다시 잠금
}

void close(){
    
}
