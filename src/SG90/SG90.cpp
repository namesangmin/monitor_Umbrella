#include "SG90.h"
#include "LCD/LCDSG90.h"
Servo myServo;

void initServo(int servoPin) {
    myServo.attach(servoPin);
    myServo.write(0);
}
 
void Rental_unlockUmbrella(int ButtonNum){
    SG90RentalChoice(ButtonNum);
    // Serial.printf("우산 %d번 모터 작동 중...\n", ButtonNum);
    // Serial.printf("%d번 우산을 빌렸습니다.\n",ButtonNum);
    myServo.write(90);   // 잠금 해제
    delay(3000);
    myServo.write(0);    // 다시 잠금
}

void Return_unlockUmbrella(int ButtonNum){
    SG90ReturnChoice(ButtonNum);
    // Serial.printf("우산 %d번 모터 작동 중...\n", ButtonNum);
    // Serial.printf("%d번에 우산을 반납했습니다.\n",ButtonNum);
    myServo.write(90);   // 잠금 해제
    delay(3000);
    myServo.write(0);    // 다시 잠금
}
