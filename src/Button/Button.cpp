#include "Button.h"

void initButton(){
    pinMode(Umbrella1Pin, INPUT_PULLUP); // 우산 1
    pinMode(Umbrella2Pin, INPUT_PULLUP); // 우산 2
    pinMode(Umbrella3Pin, INPUT_PULLUP); // 우산 3
    pinMode(ReturnPin, INPUT_PULLUP); // 반납
    pinMode(RentalPin, INPUT_PULLUP); // 대여
}

// 반납, 대여 버튼
String waitForAction(){
    while(true){
        if(digitalRead(ReturnPin) == LOW){
            Serial.println("반납 버튼 눌림");
            delay(200);
            return "return";
        }
        else if(digitalRead(RentalPin) == LOW) {
            Serial.println("대여 버튼 눌림");
            delay(200);
            return "rental";
        }
    }
}

// 버튼 누를 때까지 기다림
int waitForButtonPress() {
    int button = -1;
    while (button == -1) button = UmbrellaButton(); 
    return button;
}

int UmbrellaButton(){
    const int NUM_BUTTONS = 3;
    const int buttonPins[NUM_BUTTONS] = {Umbrella1Pin, Umbrella2Pin, Umbrella3Pin};

    for (int i = 0; i < NUM_BUTTONS; i++) {
        if (digitalRead(buttonPins[i]) == LOW) {
          Serial.printf("우산 %d번 버튼 눌림 - 잠금/해제 동작\n", i + 1);
          delay(200);  // 디바운싱(여러 번 누를 수 있으니까)
          return i + 1;  
        }
      }
      return -1; 
}
